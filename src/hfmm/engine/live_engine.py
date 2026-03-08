from __future__ import annotations

from loguru import logger

from hfmm.engine.paper_engine import PaperEngine


class LiveEngine(PaperEngine):
    async def run(self) -> None:
        logger.warning("[高风险] 实盘模式将发出真实订单。请确认 ENABLE_LIVE_TRADING=true 且充分理解风险。")
        await super().run()
