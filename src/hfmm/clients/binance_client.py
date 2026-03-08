from __future__ import annotations

import asyncio
from decimal import Decimal, ROUND_DOWN
from typing import Any, AsyncIterator

from binance import AsyncClient, BinanceSocketManager
from loguru import logger


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str, testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.testnet = testnet
        self.client: AsyncClient | None = None
        self.bsm: BinanceSocketManager | None = None
        self.symbol_rules: dict[str, Any] = {}

    async def connect(self) -> None:
        self.client = await AsyncClient.create(api_key=self.api_key, api_secret=self.api_secret, testnet=self.testnet)
        self.client.API_URL = self.base_url
        self.bsm = BinanceSocketManager(self.client)

    async def close(self) -> None:
        if self.client:
            await self.client.close_connection()

    async def get_account_info(self) -> dict[str, Any]:
        assert self.client
        return await self.client.get_account()

    async def get_balance(self, asset: str = "USDT") -> float:
        assert self.client
        res = await self.client.get_asset_balance(asset=asset)
        return float(res["free"])

    async def get_exchange_rules(self, symbol: str) -> dict[str, Any]:
        assert self.client
        info = await self.client.get_symbol_info(symbol)
        self.symbol_rules[symbol] = info
        return info

    def _quantize(self, symbol: str, price: float, qty: float) -> tuple[float, float]:
        info = self.symbol_rules.get(symbol)
        if not info:
            return price, qty
        tick = next(f["tickSize"] for f in info["filters"] if f["filterType"] == "PRICE_FILTER")
        step = next(f["stepSize"] for f in info["filters"] if f["filterType"] == "LOT_SIZE")
        price_q = float(Decimal(str(price)).quantize(Decimal(tick), rounding=ROUND_DOWN))
        qty_q = float(Decimal(str(qty)).quantize(Decimal(step), rounding=ROUND_DOWN))
        return price_q, qty_q

    async def place_limit_order(self, symbol: str, side: str, price: float, qty: float) -> dict[str, Any]:
        assert self.client
        p, q = self._quantize(symbol, price, qty)
        return await self.client.create_order(symbol=symbol, side=side, type="LIMIT", timeInForce="GTC", quantity=q, price=p)

    async def cancel_order(self, symbol: str, order_id: int) -> dict[str, Any]:
        assert self.client
        return await self.client.cancel_order(symbol=symbol, orderId=order_id)

    async def get_order(self, symbol: str, order_id: int) -> dict[str, Any]:
        assert self.client
        return await self.client.get_order(symbol=symbol, orderId=order_id)

    async def get_position(self, symbol: str) -> float:
        # Spot账号无独立持仓接口，示例中由策略本地维护。
        _ = symbol
        return 0.0

    async def stream_depth(self, symbol: str) -> AsyncIterator[dict[str, Any]]:
        assert self.bsm
        while True:
            try:
                async with self.bsm.depth_socket(symbol.lower()) as stream:
                    while True:
                        yield await stream.recv()
            except Exception as exc:
                logger.warning(f"depth stream reconnect: {exc}")
                await asyncio.sleep(1)

    async def stream_trades(self, symbol: str) -> AsyncIterator[dict[str, Any]]:
        assert self.bsm
        while True:
            try:
                async with self.bsm.trade_socket(symbol.lower()) as stream:
                    while True:
                        yield await stream.recv()
            except Exception as exc:
                logger.warning(f"trade stream reconnect: {exc}")
                await asyncio.sleep(1)
