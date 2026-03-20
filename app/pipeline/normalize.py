from __future__ import annotations

from app.models.price_bar import PriceBar


def normalize_rows(
    raw_rows: list[dict[str, str]],
    ticker: str,
    import_batch_id: str,
    timeframe: str = "1d",
    source: str = "massive_csv",
) -> list[PriceBar]:
    # Future optimization note:
    # if profiling shows bulk row conversion is hot on large imports,
    # this stage can be replaced with a compiled/native implementation.
    # do not optimize before profiling.
    return [
        PriceBar(
            ticker=ticker.upper(),
            timeframe=timeframe,
            ts=_normalize_date(row["date"]),
            open=float(row["open"]),
            high=float(row["high"]),
            low=float(row["low"]),
            close=float(row["close"]),
            volume=int(row["volume"]),
            source=source,
            import_batch_id=import_batch_id,
        )
        for row in raw_rows
    ]


def _normalize_date(raw_date: str) -> str:
    return f"{raw_date}T00:00:00Z"
