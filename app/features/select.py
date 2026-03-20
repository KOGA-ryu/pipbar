from __future__ import annotations

from app.db.connection import get_connection
from app.models.price_bar import PriceBar


def select_bars(
    db_path: str,
    ticker: str | None,
    timeframe: str,
    start_ts: str | None,
    end_ts: str | None,
    limit: int | None = None,
) -> list[PriceBar]:
    if not timeframe:
        raise ValueError("timeframe is required")

    query = """
    SELECT ticker, timeframe, ts, open, high, low, close, volume, source, import_batch_id
    FROM price_bars
    WHERE timeframe = ?
    """
    parameters: list[object] = [timeframe]

    if ticker is not None:
        query += " AND ticker = ?"
        parameters.append(ticker.upper())
    if start_ts is not None:
        query += " AND ts >= ?"
        parameters.append(start_ts)
    if end_ts is not None:
        query += " AND ts <= ?"
        parameters.append(end_ts)

    query += " ORDER BY ts ASC"

    if limit is not None:
        query += " LIMIT ?"
        parameters.append(limit)

    with get_connection(db_path) as conn:
        rows = conn.execute(query, parameters).fetchall()

    return [
        PriceBar(
            ticker=row["ticker"],
            timeframe=row["timeframe"],
            ts=row["ts"],
            open=row["open"],
            high=row["high"],
            low=row["low"],
            close=row["close"],
            volume=row["volume"],
            source=row["source"],
            import_batch_id=row["import_batch_id"],
        )
        for row in rows
    ]
