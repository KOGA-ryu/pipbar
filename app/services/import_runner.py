from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from app.db.connection import get_connection
from app.db.init_db import init_db
from app.db.queries import create_import_run, finalize_import_run
from app.pipeline.discover import discover_csv_files
from app.pipeline.load import load_valid_records, persist_rejected_records
from app.pipeline.normalize import normalize_rows
from app.pipeline.parse import parse_csv_file
from app.pipeline.report import build_run_summary, print_run_summary
from app.pipeline.validate import validate_records


def run_import(
    input_dir: str,
    db_path: str,
    schema_path: str,
    import_batch_id: str | None = None,
    timeframe: str = "1d",
    source: str = "massive_csv",
) -> dict[str, int]:
    # Future optimization note:
    # keep orchestration in Python unless profiling proves coordination overhead matters.
    # that is unlikely relative to parsing, normalization, validation, or DB I/O.
    init_db(db_path, schema_path)
    discovered_files = discover_csv_files(input_dir)
    batch_id = import_batch_id or _generate_batch_id()

    rows_parsed = 0
    rows_valid = 0
    rows_invalid = 0
    rows_inserted = 0
    rows_duplicates_skipped = 0
    completed_at: str | None = None
    current_stage = "run_init"

    with get_connection(db_path) as conn:
        create_import_run(
            conn=conn,
            import_batch_id=batch_id,
            source=source,
            timeframe=timeframe,
            input_path=input_dir,
            status="running",
            started_at=_utc_now(),
        )
        conn.commit()

        try:
            current_stage = "discover"
            for file_path in discovered_files:
                current_stage = "parse"
                raw_rows = parse_csv_file(file_path)
                rows_parsed += len(raw_rows)

                ticker = _extract_ticker_from_filename(file_path)
                current_stage = "normalize"
                normalized_records = normalize_rows(
                    raw_rows,
                    ticker=ticker,
                    import_batch_id=batch_id,
                    timeframe=timeframe,
                    source=source,
                )

                current_stage = "validate"
                valid_records, invalid_records = validate_records(normalized_records)
                rows_valid += len(valid_records)
                rows_invalid += len(invalid_records)

                current_stage = "load"
                load_result = load_valid_records(conn, valid_records)
                rows_inserted += load_result["rows_inserted"]
                rows_duplicates_skipped += load_result["rows_duplicates_skipped"]
                persist_rejected_records(
                    conn,
                    invalid_records,
                    import_batch_id=batch_id,
                    ticker=ticker,
                    file_path=file_path,
                )
                conn.commit()

            completed_at = _utc_now()
            current_stage = "run_finalize"
            finalize_import_run(
                conn=conn,
                import_batch_id=batch_id,
                completed_at=completed_at,
                status="completed",
                failure_reason=None,
                stage_failed=None,
                files_discovered=len(discovered_files),
                rows_parsed=rows_parsed,
                rows_valid=rows_valid,
                rows_invalid=rows_invalid,
                rows_inserted=rows_inserted,
                rows_duplicates_skipped=rows_duplicates_skipped,
            )
            conn.commit()
        except Exception:
            conn.rollback()
            completed_at = _utc_now()
            finalize_import_run(
                conn=conn,
                import_batch_id=batch_id,
                completed_at=completed_at,
                status="failed",
                failure_reason=str(sys.exc_info()[1]),
                stage_failed=current_stage,
                files_discovered=len(discovered_files),
                rows_parsed=rows_parsed,
                rows_valid=rows_valid,
                rows_invalid=rows_invalid,
                rows_inserted=rows_inserted,
                rows_duplicates_skipped=rows_duplicates_skipped,
            )
            conn.commit()
            raise

    summary = build_run_summary(
        files_discovered=len(discovered_files),
        rows_parsed=rows_parsed,
        rows_valid=rows_valid,
        rows_invalid=rows_invalid,
        rows_inserted=rows_inserted,
        rows_duplicates_skipped=rows_duplicates_skipped,
    )
    _assert_summary_invariants(summary)
    print_run_summary(summary)
    return summary


def _extract_ticker_from_filename(file_path: str) -> str:
    return Path(file_path).stem.split("_")[0].upper()


def _utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _generate_batch_id() -> str:
    return f"batch-{uuid4().hex[:12]}"


def _assert_summary_invariants(summary: dict[str, int]) -> None:
    assert summary["rows_parsed"] == summary["rows_valid"] + summary["rows_invalid"]
    assert summary["rows_valid"] == summary["rows_inserted"] + summary["rows_duplicates_skipped"]
