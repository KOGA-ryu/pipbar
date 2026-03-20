from __future__ import annotations

import sqlite3
from datetime import UTC, datetime

from app.db.queries import (
    build_rejected_record_values,
    insert_price_bar,
    insert_rejected_rows,
    is_price_bar_duplicate_error,
)
from app.models.price_bar import PriceBar


def load_valid_records(conn: sqlite3.Connection, records: list[PriceBar]) -> dict[str, int]:
    # Future optimization note:
    # batched prepared inserts are the first optimization path here.
    # consider a native extension only if profiling justifies it.
    inserted_count = 0
    duplicate_count = 0

    for record in records:
        try:
            insert_price_bar(conn, record)
            inserted_count += 1
        except sqlite3.IntegrityError as error:
            if is_price_bar_duplicate_error(error):
                duplicate_count += 1
                continue
            raise

    return {
        "rows_inserted": inserted_count,
        "rows_duplicates_skipped": duplicate_count,
    }


def persist_rejected_records(
    conn: sqlite3.Connection,
    invalid_records: list[dict[str, object]],
    import_batch_id: str,
    ticker: str,
    file_path: str,
) -> int:
    created_at = _utc_now()
    rejected_records = [
        build_rejected_record_values(
            import_batch_id=import_batch_id,
            ticker=ticker,
            raw_row=invalid_record["raw_row"],
            file_path=file_path,
            issues=invalid_record["issues"],
            created_at=created_at,
        )
        for invalid_record in invalid_records
    ]
    inserted_count = insert_rejected_rows(conn, rejected_records)
    return inserted_count


def _utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
