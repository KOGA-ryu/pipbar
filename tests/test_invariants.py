from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

from app.db.connection import get_connection
from app.services.import_runner import run_import


def test_successful_run_summary_and_import_run_obey_count_invariants(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    fixture_path = Path("tests/fixtures/valid_daily.csv")
    shutil.copy(fixture_path, input_dir / fixture_path.name)

    db_path = tmp_path / "stock_data.sqlite3"
    summary = run_import(
        input_dir=str(input_dir),
        db_path=str(db_path),
        schema_path="app/db/schema.sql",
        import_batch_id="test-invariants-success-001",
    )

    _assert_nonnegative_counts(summary)
    _assert_completed_count_invariants(summary)

    with get_connection(str(db_path)) as conn:
        run_row = conn.execute(
            """
            SELECT
                files_discovered,
                rows_parsed,
                rows_valid,
                rows_invalid,
                rows_inserted,
                rows_duplicates_skipped
            FROM import_runs
            WHERE import_batch_id = ?
            """,
            ("test-invariants-success-001",),
        ).fetchone()
        _assert_nonnegative_counts(dict(run_row))
        _assert_completed_count_invariants(dict(run_row))


def test_duplicate_rerun_summary_and_import_run_obey_count_invariants(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    fixture_path = Path("tests/fixtures/valid_daily.csv")
    shutil.copy(fixture_path, input_dir / fixture_path.name)

    db_path = tmp_path / "stock_data.sqlite3"
    run_import(
        input_dir=str(input_dir),
        db_path=str(db_path),
        schema_path="app/db/schema.sql",
        import_batch_id="test-invariants-rerun-001",
    )
    second_summary = run_import(
        input_dir=str(input_dir),
        db_path=str(db_path),
        schema_path="app/db/schema.sql",
        import_batch_id="test-invariants-rerun-002",
    )

    _assert_nonnegative_counts(second_summary)
    _assert_completed_count_invariants(second_summary)

    with get_connection(str(db_path)) as conn:
        run_row = conn.execute(
            """
            SELECT
                files_discovered,
                rows_parsed,
                rows_valid,
                rows_invalid,
                rows_inserted,
                rows_duplicates_skipped
            FROM import_runs
            WHERE import_batch_id = ?
            """,
            ("test-invariants-rerun-002",),
        ).fetchone()
        _assert_nonnegative_counts(dict(run_row))
        _assert_completed_count_invariants(dict(run_row))


def test_failed_run_import_run_obeys_count_invariants(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    broken_file = input_dir / "broken_daily.csv"
    broken_file.write_text(
        "date,open,high,low,close,volume\n"
        "2024-01-02,187.15,188.44,183.89,185.64,82488700\n",
        encoding="utf-8",
    )
    os.chmod(broken_file, 0)

    db_path = tmp_path / "stock_data.sqlite3"

    with pytest.raises(PermissionError):
        run_import(
            input_dir=str(input_dir),
            db_path=str(db_path),
            schema_path="app/db/schema.sql",
            import_batch_id="test-invariants-failed-001",
        )

    with get_connection(str(db_path)) as conn:
        run_row = conn.execute(
            """
            SELECT
                files_discovered,
                rows_parsed,
                rows_valid,
                rows_invalid,
                rows_inserted,
                rows_duplicates_skipped
            FROM import_runs
            WHERE import_batch_id = ?
            """,
            ("test-invariants-failed-001",),
        ).fetchone()
        _assert_nonnegative_counts(dict(run_row))
    os.chmod(broken_file, 0o644)


def _assert_completed_count_invariants(counts: dict[str, int]) -> None:
    assert counts["rows_parsed"] == counts["rows_valid"] + counts["rows_invalid"]
    assert counts["rows_valid"] == counts["rows_inserted"] + counts["rows_duplicates_skipped"]


def _assert_nonnegative_counts(counts: dict[str, int]) -> None:
    for key in (
        "files_discovered",
        "rows_parsed",
        "rows_valid",
        "rows_invalid",
        "rows_inserted",
        "rows_duplicates_skipped",
    ):
        assert counts[key] >= 0
