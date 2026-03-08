from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


@dataclass
class EnvSettings:
    """环境变量配置。"""

    binance_api_key: str = ""
    binance_api_secret: str = ""
    base_url: str = "https://api.binance.com"
    testnet: bool = True
    enable_live_trading: bool = False
    symbol: str = "BTCUSDT"

    @classmethod
    def from_env(cls) -> "EnvSettings":
        def b(name: str, default: bool) -> bool:
            return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}

        return cls(
            binance_api_key=os.getenv("BINANCE_API_KEY", ""),
            binance_api_secret=os.getenv("BINANCE_API_SECRET", ""),
            base_url=os.getenv("BASE_URL", "https://api.binance.com"),
            testnet=b("TESTNET", True),
            enable_live_trading=b("ENABLE_LIVE_TRADING", False),
            symbol=os.getenv("SYMBOL", "BTCUSDT"),
        )


@dataclass
class AppConfig:
    name: str = "crypto-hfmm"
    mode: Literal["backtest", "paper", "live"] = "paper"


@dataclass
class MarketConfig:
    symbol: str = "BTCUSDT"
    kline_interval: str = "1m"
    depth_levels: int = 10


@dataclass
class StrategyConfig:
    base_spread_bps: float = 4.0
    min_spread_bps: float = 2.0
    max_spread_bps: float = 20.0
    order_size_usdt: float = 30.0
    quote_refresh_sec: float = 2.0
    order_ttl_sec: int = 12
    max_open_orders: int = 6
    inventory_target: float = 0.0
    inventory_skew: float = 0.15
    momentum_weight: float = 0.2


@dataclass
class RiskConfig:
    initial_capital: float = 1000.0
    max_daily_loss: float = 60.0
    max_order_notional: float = 50.0
    max_net_position: float = 0.01
    max_consecutive_losses: int = 5
    max_slippage_bps: float = 15.0
    api_failure_threshold: int = 8
    ws_stale_seconds: int = 5
    abnormal_vol_multiplier: float = 4.0


@dataclass
class FeesConfig:
    maker_fee_bps: float = 1.0
    taker_fee_bps: float = 2.5
    rebate_bps: float = 0.0


@dataclass
class BacktestConfig:
    csv_path: str = "data/sample_klines.csv"
    slippage_bps: float = 2.0
    latency_ms: int = 100


@dataclass
class Settings:
    app: AppConfig = field(default_factory=AppConfig)
    market: MarketConfig = field(default_factory=MarketConfig)
    strategy: StrategyConfig = field(default_factory=StrategyConfig)
    risk: RiskConfig = field(default_factory=RiskConfig)
    fees: FeesConfig = field(default_factory=FeesConfig)
    backtest: BacktestConfig = field(default_factory=BacktestConfig)


def _parse_scalar(value: str):
    v = value.strip()
    if v in {"true", "false"}:
        return v == "true"
    try:
        if "." in v:
            return float(v)
        return int(v)
    except ValueError:
        return v.strip('"').strip("'")


def _simple_yaml_load(path: str) -> dict:
    data: dict = {}
    current: dict | None = None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line:
            continue
        if not raw.startswith(" ") and line.endswith(":"):
            key = line[:-1].strip()
            data[key] = {}
            current = data[key]
            continue
        if current is not None and ":" in line:
            k, v = line.strip().split(":", 1)
            current[k.strip()] = _parse_scalar(v)
    return data


def load_settings(path: str = "config.yaml") -> tuple[Settings, EnvSettings]:
    raw = _simple_yaml_load(path)
    settings = Settings(
        app=AppConfig(**raw.get("app", {})),
        market=MarketConfig(**raw.get("market", {})),
        strategy=StrategyConfig(**raw.get("strategy", {})),
        risk=RiskConfig(**raw.get("risk", {})),
        fees=FeesConfig(**raw.get("fees", {})),
        backtest=BacktestConfig(**raw.get("backtest", {})),
    )
    env = EnvSettings.from_env()
    settings.market.symbol = env.symbol or settings.market.symbol
    return settings, env
