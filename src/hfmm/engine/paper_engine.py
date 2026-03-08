from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from loguru import logger

from hfmm.clients.binance_client import BinanceClient
from hfmm.core.config import Settings
from hfmm.core.models import FillEvent, Position, Quote
from hfmm.metrics import MetricsCollector
from hfmm.risk.manager import RiskManager
from hfmm.strategy.market_maker import AdaptiveMarketMaker


class PaperEngine:
    def __init__(self, settings: Settings, client: BinanceClient):
        self.settings = settings
        self.client = client
        self.strategy = AdaptiveMarketMaker(settings.strategy)
        self.risk = RiskManager(settings.risk)
        self.metrics = MetricsCollector()
        self.position = Position(quote_qty=settings.risk.initial_capital)
        self.last_quote: Quote | None = None

    async def _depth_loop(self) -> None:
        async for msg in self.client.stream_depth(self.settings.market.symbol):
            try:
                bid = float(msg["b"][0][0])
                ask = float(msg["a"][0][0])
                bid_qty = float(msg["b"][0][1])
                ask_qty = float(msg["a"][0][1])
                self.last_quote = Quote(bid=bid, ask=ask, bid_qty=bid_qty, ask_qty=ask_qty, ts=datetime.now(timezone.utc))
            except Exception:
                continue

    async def _trade_loop(self) -> None:
        async for msg in self.client.stream_trades(self.settings.market.symbol):
            price = float(msg["p"])
            self.strategy.on_trade(price)

    async def _quote_loop(self) -> None:
        while True:
            await asyncio.sleep(self.settings.strategy.quote_refresh_sec)
            if not self.last_quote:
                continue
            q = self.last_quote
            imbalance = (q.bid_qty - q.ask_qty) / max(q.bid_qty + q.ask_qty, 1e-9)
            trade_bias = 0.0
            buy, sell = self.strategy.build_quotes(q, self.position.base_qty, imbalance, trade_bias)

            for intent in (buy, sell):
                notional = intent.price * intent.qty
                ok, reason = self.risk.can_place_order(notional, self.position.base_qty, self.position.quote_qty)
                if not ok:
                    logger.warning(f"skip order {intent.side}: {reason}")
                    continue
                self.metrics.on_submit()
                # 模拟成交规则：买价 >= ask 或 卖价 <= bid 视为瞬时成交
                filled = (intent.side == "BUY" and intent.price >= q.ask) or (intent.side == "SELL" and intent.price <= q.bid)
                if not filled:
                    continue
                fee_bps = self.settings.fees.maker_fee_bps
                fee = notional * fee_bps / 10_000
                if intent.side == "BUY":
                    self.position.base_qty += intent.qty
                    self.position.quote_qty -= notional + fee
                else:
                    self.position.base_qty -= intent.qty
                    self.position.quote_qty += notional - fee
                fill = FillEvent(intent.side, intent.price, intent.qty, fee, True, datetime.now(timezone.utc))
                self.metrics.on_fill(fill, rebate_bps=self.settings.fees.rebate_bps)
                self.metrics.update_inventory(self.position.base_qty)

    async def run(self) -> None:
        logger.info("启动模拟盘引擎（dry-run）")
        await self.client.connect()
        await self.client.get_exchange_rules(self.settings.market.symbol)
        try:
            await asyncio.gather(self._depth_loop(), self._trade_loop(), self._quote_loop())
        finally:
            await self.client.close()
