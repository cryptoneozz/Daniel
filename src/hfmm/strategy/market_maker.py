from __future__ import annotations

from collections import deque
from statistics import pstdev

from hfmm.core.config import StrategyConfig
from hfmm.core.models import OrderIntent, Quote


class AdaptiveMarketMaker:
    """中性准做市策略原型。"""

    def __init__(self, conf: StrategyConfig):
        self.conf = conf
        self.trades: deque[float] = deque(maxlen=50)

    def on_trade(self, price: float) -> None:
        self.trades.append(price)

    def _volatility_bps(self) -> float:
        if len(self.trades) < 5:
            return 0.0
        vol = pstdev(self.trades)
        mid = sum(self.trades) / len(self.trades)
        return (vol / mid) * 10_000 if mid else 0.0

    def build_quotes(self, quote: Quote, inventory: float, imbalance: float, trade_bias: float) -> tuple[OrderIntent, OrderIntent]:
        mid = (quote.bid + quote.ask) / 2
        vol_bps = self._volatility_bps()
        spread_bps = self.conf.base_spread_bps + 0.6 * vol_bps + 2.0 * abs(imbalance) + self.conf.momentum_weight * abs(trade_bias)
        spread_bps = max(self.conf.min_spread_bps, min(spread_bps, self.conf.max_spread_bps))

        # 库存偏移：库存为正时，提高卖价吸引卖出，降低买价减少继续买入
        skew = (inventory - self.conf.inventory_target) * self.conf.inventory_skew
        half = spread_bps / 20_000 * mid
        bid = mid - half - skew
        ask = mid + half - skew
        if bid >= ask:  # 防脏数据与潜在自成交
            ask = bid * 1.0002

        qty = self.conf.order_size_usdt / mid
        return (
            OrderIntent(side="BUY", price=bid, qty=qty),
            OrderIntent(side="SELL", price=ask, qty=qty),
        )
