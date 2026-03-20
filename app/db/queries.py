from __future__ import annotations

import sqlite3

from app.models.price_bar import PriceBar

PRICE_BAR_INSERT_COLUMNS = (
    "ticker",
    "timeframe",
    "ts",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "source",
    "import_batch_id",
)

INSERT_PRICE_BAR_SQL = """
INSERT INTO price_bars (
    ticker,
    timeframe,
    ts,
    open,
    high,
    low,
    close,
    volume,
    source,
    import_batch_id
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

INSERT_IMPORT_RUN_SQL = """
INSERT INTO import_runs (
    import_batch_id,
    source,
    timeframe,
    input_path,
    status,
    created_at
) VALUES (?, ?, ?, ?, ?, ?)
"""


def create_import_run(
    conn: sqlite3.Connection,
    import_batch_id: str,
    source: str,
    timeframe: str,
    input_path: str,
    status: str,
    created_at: str,
) -> None:
    conn.execute(
        INSERT_IMPORT_RUN_SQL,
        (import_batch_id, source, timeframe, input_path, status, created_at),
    )


def insert_price_bar(conn: sqlite3.Connection, bar: PriceBar) -> None:
    conn.execute(INSERT_PRICE_BAR_SQL, _price_bar_values(bar))


def insert_price_bars(conn: sqlite3.Connection, bars: list[PriceBar]) -> int:
    conn.executemany(INSERT_PRICE_BAR_SQL, [_price_bar_values(bar) for bar in bars])
    return len(bars)


def count_price_bars(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COUNT(*) FROM price_bars").fetchone()
    return int(row[0])


def _price_bar_values(bar: PriceBar) -> tuple[str, str, str, float, float, float, float, int, str, str]:
    return (
        bar.ticker,
        bar.timeframe,
        bar.ts,
        bar.open,
        bar.high,
        bar.low,
        bar.close,
        bar.volume,
        bar.source,
        bar.import_batch_id,
    )
