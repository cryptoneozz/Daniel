from __future__ import annotations

from dataclasses import dataclass

from hfmm.core.config import RiskConfig


@dataclass
class RiskState:
    daily_pnl: float = 0.0
    consecutive_losses: int = 0
    api_failures: int = 0
    paused: bool = False


class RiskManager:
    def __init__(self, conf: RiskConfig):
        self.conf = conf
        self.state = RiskState()

    def can_place_order(self, notional: float, net_position: float, balance: float) -> tuple[bool, str]:
        if self.state.paused:
            return False, "risk paused"
        if balance < notional:
            return False, "insufficient balance"
        if notional > self.conf.max_order_notional:
            return False, "order too large"
        if abs(net_position) > self.conf.max_net_position:
            return False, "net position limit"
        if self.state.daily_pnl <= -self.conf.max_daily_loss:
            self.state.paused = True
            return False, "daily loss limit"
        if self.state.consecutive_losses >= self.conf.max_consecutive_losses:
            self.state.paused = True
            return False, "loss streak limit"
        if self.state.api_failures >= self.conf.api_failure_threshold:
            self.state.paused = True
            return False, "api fuse triggered"
        return True, "ok"

    def on_trade_result(self, pnl: float) -> None:
        self.state.daily_pnl += pnl
        if pnl < 0:
            self.state.consecutive_losses += 1
        else:
            self.state.consecutive_losses = 0

    def on_api_error(self) -> None:
        self.state.api_failures += 1

    def on_api_recover(self) -> None:
        self.state.api_failures = 0
