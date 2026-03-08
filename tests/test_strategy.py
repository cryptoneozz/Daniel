from datetime import datetime, timezone

from hfmm.core.config import StrategyConfig
from hfmm.core.models import Quote
from hfmm.strategy.market_maker import AdaptiveMarketMaker


def test_quotes_are_ordered() -> None:
    s = AdaptiveMarketMaker(StrategyConfig())
    q = Quote(100.0, 100.1, 5.0, 4.0, datetime.now(timezone.utc))
    buy, sell = s.build_quotes(q, inventory=0.0, imbalance=0.1, trade_bias=0.0)
    assert buy.price < sell.price
    assert buy.qty > 0
