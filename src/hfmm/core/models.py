from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass(slots=True)
class Quote:
    bid: float
    ask: float
    bid_qty: float
    ask_qty: float
    ts: datetime


@dataclass(slots=True)
class OrderIntent:
    side: Literal["BUY", "SELL"]
    price: float
    qty: float
    tif: str = "GTC"


@dataclass(slots=True)
class FillEvent:
    side: Literal["BUY", "SELL"]
    price: float
    qty: float
    fee: float
    maker: bool
    ts: datetime


@dataclass(slots=True)
class Position:
    base_qty: float = 0.0
    quote_qty: float = 1000.0

    def notional(self, mid: float) -> float:
        return self.base_qty * mid + self.quote_qty
