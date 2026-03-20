from __future__ import annotations

import json
import math
import sqlite3

from app.models.price_bar import PriceBar
from app.models.price_bar_feature import PriceBarFeature
from app.models.label_row import LabelRow

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
    started_at
) VALUES (?, ?, ?, ?, ?, ?)
"""

FINALIZE_IMPORT_RUN_SQL = """
UPDATE import_runs
SET
    completed_at = ?,
    status = ?,
    failure_reason = ?,
    stage_failed = ?,
    files_discovered = ?,
    rows_parsed = ?,
    rows_valid = ?,
    rows_invalid = ?,
    rows_inserted = ?,
    rows_duplicates_skipped = ?
WHERE import_batch_id = ?
"""

INSERT_REJECTED_ROW_SQL = """
INSERT INTO rejected_rows (
    import_batch_id,
    ticker,
    file_path,
    raw_row_json,
    issues_json,
    created_at
) VALUES (?, ?, ?, ?, ?, ?)
"""

INSERT_PRICE_BAR_FEATURE_SQL = """
INSERT INTO price_bar_features (
    ticker,
    timeframe,
    ts,
    close_1d_return,
    high_low_range,
    close_open_delta,
    feature_batch_id
) VALUES (?, ?, ?, ?, ?, ?, ?)
"""

INSERT_LABEL_ROW_SQL = """
INSERT INTO price_bar_labels (
    ticker,
    timeframe,
    ts,
    next_1d_return,
    label_batch_id
) VALUES (?, ?, ?, ?, ?)
"""


def create_import_run(
    conn: sqlite3.Connection,
    import_batch_id: str,
    source: str,
    timeframe: str,
    input_path: str,
    status: str,
    started_at: str,
) -> None:
    conn.execute(
        INSERT_IMPORT_RUN_SQL,
        (import_batch_id, source, timeframe, input_path, status, started_at),
    )


def finalize_import_run(
    conn: sqlite3.Connection,
    import_batch_id: str,
    completed_at: str,
    status: str,
    failure_reason: str | None,
    stage_failed: str | None,
    files_discovered: int,
    rows_parsed: int,
    rows_valid: int,
    rows_invalid: int,
    rows_inserted: int,
    rows_duplicates_skipped: int,
) -> None:
    conn.execute(
        FINALIZE_IMPORT_RUN_SQL,
        (
            completed_at,
            status,
            failure_reason,
            stage_failed,
            files_discovered,
            rows_parsed,
            rows_valid,
            rows_invalid,
            rows_inserted,
            rows_duplicates_skipped,
            import_batch_id,
        ),
    )


def insert_price_bar(conn: sqlite3.Connection, bar: PriceBar) -> None:
    conn.execute(INSERT_PRICE_BAR_SQL, _price_bar_values(bar))


def insert_price_bars(conn: sqlite3.Connection, bars: list[PriceBar]) -> int:
    conn.executemany(INSERT_PRICE_BAR_SQL, [_price_bar_values(bar) for bar in bars])
    return len(bars)


def is_price_bar_duplicate_error(error: sqlite3.IntegrityError) -> bool:
    message = str(error)
    return (
        "UNIQUE constraint failed:" in message
        and "price_bars.ticker" in message
        and "price_bars.timeframe" in message
        and "price_bars.ts" in message
    )


def count_price_bars(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COUNT(*) FROM price_bars").fetchone()
    return int(row[0])


def insert_rejected_rows(
    conn: sqlite3.Connection,
    rejected_records: list[dict[str, str]],
) -> int:
    # Future optimization note:
    # if rejected-row volume becomes material, keep the current JSON/text contract
    # but move bulk serialization and batched inserts lower in the stack.
    # the hot path belongs below the current explicit SQL boundary, not in the runner.
    conn.executemany(
        INSERT_REJECTED_ROW_SQL,
        [
            (
                rejected_record["import_batch_id"],
                rejected_record["ticker"],
                rejected_record["file_path"],
                rejected_record["raw_row_json"],
                rejected_record["issues_json"],
                rejected_record["created_at"],
            )
            for rejected_record in rejected_records
        ],
    )
    return len(rejected_records)


def count_rejected_rows(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COUNT(*) FROM rejected_rows").fetchone()
    return int(row[0])


def insert_price_bar_feature(conn: sqlite3.Connection, feature: PriceBarFeature) -> None:
    conn.execute(INSERT_PRICE_BAR_FEATURE_SQL, _price_bar_feature_values(feature))


def is_price_bar_feature_duplicate_error(error: sqlite3.IntegrityError) -> bool:
    message = str(error)
    return (
        "UNIQUE constraint failed:" in message
        and "price_bar_features.ticker" in message
        and "price_bar_features.timeframe" in message
        and "price_bar_features.ts" in message
    )


def count_price_bar_features(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COUNT(*) FROM price_bar_features").fetchone()
    return int(row[0])


def insert_label_row(conn: sqlite3.Connection, row: LabelRow) -> None:
    conn.execute(INSERT_LABEL_ROW_SQL, _label_row_values(row))


def is_label_row_duplicate_error(error: sqlite3.IntegrityError) -> bool:
    message = str(error)
    return (
        "UNIQUE constraint failed:" in message
        and "price_bar_labels.ticker" in message
        and "price_bar_labels.timeframe" in message
        and "price_bar_labels.ts" in message
    )


def count_price_bar_labels(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COUNT(*) FROM price_bar_labels").fetchone()
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


def _price_bar_feature_values(
    feature: PriceBarFeature,
) -> tuple[str, str, str, float | None, float, float, str]:
    return (
        feature.ticker,
        feature.timeframe,
        feature.ts,
        _normalize_nullable_float(feature.close_1d_return),
        feature.high_low_range,
        feature.close_open_delta,
        feature.feature_batch_id,
    )


def _label_row_values(row: LabelRow) -> tuple[str, str, str, float | None, str]:
    return (
        row.ticker,
        row.timeframe,
        row.ts,
        _normalize_nullable_float(row.next_1d_return),
        row.label_batch_id,
    )


def build_rejected_record_values(
    *,
    import_batch_id: str,
    ticker: str,
    raw_row: dict[str, str],
    file_path: str,
    issues: list[str],
    created_at: str,
) -> dict[str, str]:
    return {
        "import_batch_id": import_batch_id,
        "ticker": ticker,
        "file_path": file_path,
        "raw_row_json": json.dumps(raw_row),
        "issues_json": json.dumps(issues),
        "created_at": created_at,
    }


def _normalize_nullable_float(value: float | None) -> float | None:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    return value
