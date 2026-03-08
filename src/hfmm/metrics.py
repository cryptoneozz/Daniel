from __future__ import annotations

from dataclasses import dataclass, field

from hfmm.core.models import FillEvent


@dataclass
class MetricsCollector:
    """统计成交量、手续费、返佣、收益。"""

    gross_pnl: float = 0.0
    fee: float = 0.0
    rebate_estimate: float = 0.0
    turnover: float = 0.0
    maker_turnover: float = 0.0
    taker_turnover: float = 0.0
    filled_orders: int = 0
    submitted_orders: int = 0
    inventory_history: list[float] = field(default_factory=list)

    def on_submit(self) -> None:
        self.submitted_orders += 1

    def on_fill(self, fill: FillEvent, rebate_bps: float) -> None:
        signed = fill.qty if fill.side == "SELL" else -fill.qty
        self.gross_pnl += signed * fill.price
        notional = fill.price * fill.qty
        self.turnover += notional
        self.fee += fill.fee
        self.rebate_estimate += notional * rebate_bps / 10_000
        if fill.maker:
            self.maker_turnover += notional
        else:
            self.taker_turnover += notional
        self.filled_orders += 1

    def update_inventory(self, qty: float) -> None:
        self.inventory_history.append(qty)

    def summary(self) -> dict[str, float]:
        fill_ratio = self.filled_orders / self.submitted_orders if self.submitted_orders else 0.0
        net_pnl = self.gross_pnl - self.fee + self.rebate_estimate
        maker_ratio = self.maker_turnover / self.turnover if self.turnover else 0.0
        exposure = max((abs(x) for x in self.inventory_history), default=0.0)
        return {
            "turnover": self.turnover,
            "gross_pnl": self.gross_pnl,
            "net_pnl": net_pnl,
            "fee": self.fee,
            "rebate_estimate": self.rebate_estimate,
            "maker_ratio": maker_ratio,
            "inventory_exposure": exposure,
            "fill_ratio": fill_ratio,
        }
