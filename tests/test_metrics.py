from datetime import datetime, timezone

from hfmm.core.models import FillEvent
from hfmm.metrics import MetricsCollector


def test_metrics_summary() -> None:
    m = MetricsCollector()
    m.on_submit()
    m.on_fill(FillEvent("SELL", 100, 0.1, 0.01, True, datetime.now(timezone.utc)), rebate_bps=1.0)
    summary = m.summary()
    assert summary["turnover"] > 0
    assert summary["fill_ratio"] == 1.0
