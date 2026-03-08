from __future__ import annotations

import math

import numpy as np
import pandas as pd

from hfmm.core.config import Settings
from hfmm.metrics import MetricsCollector


class BacktestEngine:
    """简化回测：基于K线估计挂单成交，不等价真实撮合。"""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.metrics = MetricsCollector()

    def run(self, csv_path: str) -> dict[str, float]:
        df = pd.read_csv(csv_path)
        cash = self.settings.risk.initial_capital
        pos = 0.0
        pnl_series = []
        wins = 0
        trades = 0
        for _, row in df.iterrows():
            mid = float(row["close"])
            spread = self.settings.strategy.base_spread_bps / 10_000 * mid
            bid = mid - spread / 2
            ask = mid + spread / 2
            qty = self.settings.strategy.order_size_usdt / mid

            hit_bid = float(row["low"]) <= bid
            hit_ask = float(row["high"]) >= ask
            if hit_bid:
                notional = bid * qty
                fee = notional * self.settings.fees.maker_fee_bps / 10_000
                pos += qty
                cash -= notional + fee
                self.metrics.turnover += notional
                self.metrics.fee += fee
                trades += 1
            if hit_ask and pos >= qty:
                notional = ask * qty
                fee = notional * self.settings.fees.maker_fee_bps / 10_000
                pos -= qty
                cash += notional - fee
                trade_pnl = (ask - bid) * qty - 2 * fee
                wins += 1 if trade_pnl > 0 else 0
                self.metrics.turnover += notional
                self.metrics.fee += fee
                self.metrics.gross_pnl += trade_pnl
                trades += 1
            equity = cash + pos * mid
            pnl_series.append(equity - self.settings.risk.initial_capital)

        arr = np.array(pnl_series) if pnl_series else np.array([0.0])
        peak = np.maximum.accumulate(arr)
        dd = peak - arr
        ret = np.diff(arr, prepend=0)
        sharpe = float(ret.mean() / (ret.std() + 1e-9) * math.sqrt(252))
        return {
            "total_return": float(arr[-1]),
            "max_drawdown": float(dd.max()),
            "sharpe": sharpe,
            "win_rate": wins / max(trades, 1),
            "turnover": self.metrics.turnover,
            "fee": self.metrics.fee,
            "rebate_estimate": self.metrics.turnover * self.settings.fees.rebate_bps / 10_000,
        }
