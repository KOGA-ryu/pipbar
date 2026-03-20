from __future__ import annotations

from app.features.select import select_bars as _select_bars
from app.models.price_bar import PriceBar


def select_bars(
    db_path: str,
    ticker: str | None,
    timeframe: str,
    start_ts: str | None,
    end_ts: str | None,
) -> list[PriceBar]:
    return _select_bars(
        db_path=db_path,
        ticker=ticker,
        timeframe=timeframe,
        start_ts=start_ts,
        end_ts=end_ts,
    )
