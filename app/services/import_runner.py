from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from app.db.connection import get_connection
from app.db.init_db import init_db
from app.db.queries import create_import_run
from app.pipeline.discover import discover_csv_files
from app.pipeline.load import load_valid_records
from app.pipeline.normalize import normalize_rows
from app.pipeline.parse import parse_csv_file
from app.pipeline.report import build_run_summary, print_run_summary
from app.pipeline.validate import validate_records


def run_import(
    input_dir: str,
    db_path: str,
    schema_path: str,
    import_batch_id: str,
    timeframe: str = "1d",
    source: str = "massive_csv",
) -> dict[str, int]:
    # Future optimization note:
    # keep orchestration in Python unless profiling proves coordination overhead matters.
    # that is unlikely relative to parsing, normalization, validation, or DB I/O.
    init_db(db_path, schema_path)
    discovered_files = discover_csv_files(input_dir)

    rows_parsed = 0
    rows_valid = 0
    rows_invalid = 0
    rows_inserted = 0

    with get_connection(db_path) as conn:
        create_import_run(
            conn=conn,
            import_batch_id=import_batch_id,
            source=source,
            timeframe=timeframe,
            input_path=input_dir,
            status="started",
            created_at=_utc_now(),
        )

        for file_path in discovered_files:
            raw_rows = parse_csv_file(file_path)
            rows_parsed += len(raw_rows)

            ticker = _extract_ticker_from_filename(file_path)
            normalized_records = normalize_rows(
                raw_rows,
                ticker=ticker,
                import_batch_id=import_batch_id,
                timeframe=timeframe,
                source=source,
            )

            valid_records, invalid_records = validate_records(normalized_records)
            rows_valid += len(valid_records)
            rows_invalid += len(invalid_records)
            rows_inserted += load_valid_records(conn, valid_records)

    summary = build_run_summary(
        files_discovered=len(discovered_files),
        rows_parsed=rows_parsed,
        rows_valid=rows_valid,
        rows_invalid=rows_invalid,
        rows_inserted=rows_inserted,
    )
    print_run_summary(summary)
    return summary


def _extract_ticker_from_filename(file_path: str) -> str:
    return Path(file_path).stem.split("_")[0].upper()


def _utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
