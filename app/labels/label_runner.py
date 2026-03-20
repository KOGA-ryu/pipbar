from __future__ import annotations

from app.db.connection import get_connection
from app.labels.derive import compute_labels
from app.labels.load import load_label_rows
from app.labels.report import build_label_run_summary, print_label_run_summary
from app.labels.select import select_bars
from app.labels.validate import validate_label_rows


def run_label_generation(
    db_path: str,
    ticker: str | None,
    timeframe: str,
    start_ts: str | None,
    end_ts: str | None,
    label_batch_id: str,
) -> dict[str, int | str]:
    rows_selected = 0
    rows_derived = 0
    rows_valid = 0
    rows_invalid = 0
    rows_inserted = 0
    rows_duplicates_skipped = 0

    bars = select_bars(
        db_path=db_path,
        ticker=ticker,
        timeframe=timeframe,
        start_ts=start_ts,
        end_ts=end_ts,
    )
    rows_selected = len(bars)

    derived_rows = compute_labels(bars, label_batch_id=label_batch_id)
    rows_derived = len(derived_rows)

    valid_rows, invalid_rows = validate_label_rows(derived_rows)
    rows_valid = len(valid_rows)
    rows_invalid = len(invalid_rows)

    with get_connection(db_path) as conn:
        try:
            load_result = load_label_rows(conn, valid_rows)
            rows_inserted = load_result["rows_inserted"]
            rows_duplicates_skipped = load_result["rows_duplicates_skipped"]
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    summary = build_label_run_summary(
        rows_selected=rows_selected,
        rows_derived=rows_derived,
        rows_valid=rows_valid,
        rows_invalid=rows_invalid,
        rows_inserted=rows_inserted,
        rows_duplicates_skipped=rows_duplicates_skipped,
        label_batch_id=label_batch_id,
    )
    _assert_label_summary_invariants(summary)
    print_label_run_summary(summary)
    return summary


def _assert_label_summary_invariants(summary: dict[str, int | str]) -> None:
    assert summary["rows_selected"] >= summary["rows_derived"]
    assert summary["rows_derived"] >= summary["rows_valid"]
    assert summary["rows_valid"] == summary["rows_inserted"] + summary["rows_duplicates_skipped"]
    assert summary["rows_invalid"] >= 0
