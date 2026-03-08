from __future__ import annotations

import argparse
import asyncio

from loguru import logger

from hfmm.backtest.engine import BacktestEngine
from hfmm.clients.binance_client import BinanceClient
from hfmm.core.config import load_settings
from hfmm.core.logger import setup_logger
from hfmm.engine.live_engine import LiveEngine
from hfmm.engine.paper_engine import PaperEngine
from hfmm.utils.report import print_report


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["paper", "live", "backtest"], default=None)
    return p.parse_args()


async def run_realtime(mode: str) -> None:
    settings, env = load_settings()
    settings.app.mode = mode
    client = BinanceClient(env.binance_api_key, env.binance_api_secret, env.base_url, env.testnet)
    if mode == "live":
        if not env.enable_live_trading:
            logger.error("ENABLE_LIVE_TRADING=false，已拒绝实盘下单。")
            return
        engine = LiveEngine(settings, client)
    else:
        engine = PaperEngine(settings, client)
    await engine.run()


def run_backtest() -> None:
    settings, _ = load_settings()
    engine = BacktestEngine(settings)
    report = engine.run(settings.backtest.csv_path)
    print_report(report)


def main() -> None:
    setup_logger()
    args = parse_args()
    settings, _ = load_settings()
    mode = args.mode or settings.app.mode
    if mode == "backtest":
        run_backtest()
        return
    asyncio.run(run_realtime(mode))


if __name__ == "__main__":
    main()
