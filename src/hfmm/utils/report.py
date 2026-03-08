from __future__ import annotations

from loguru import logger


def print_report(report: dict[str, float]) -> None:
    logger.info("===== 策略报告 =====")
    for k, v in report.items():
        logger.info(f"{k}: {v:.6f}")
