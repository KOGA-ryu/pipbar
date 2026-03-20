from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

from app.db.connection import get_connection
from app.db.queries import count_price_bars
from app.services.import_runner import run_import


def test_import_valid_daily_csv_end_to_end(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    fixture_path = Path("tests/fixtures/valid_daily.csv")
    shutil.copy(fixture_path, input_dir / fixture_path.name)

    db_path = tmp_path / "stock_data.sqlite3"
    schema_path = "app/db/schema.sql"

    summary = run_import(
        input_dir=str(input_dir),
        db_path=str(db_path),
        schema_path=schema_path,
        import_batch_id="test-batch-001",
    )

    expected_summary = {
        "files_discovered": 1,
        "rows_parsed": 4,
        "rows_valid": 4,
        "rows_invalid": 0,
        "rows_inserted": 4,
        "rows_duplicates_skipped": 0,
    }

    assert db_path.exists()
    assert summary == expected_summary
    assert summary["rows_parsed"] == summary["rows_valid"] + summary["rows_invalid"]
    assert summary["rows_valid"] == summary["rows_inserted"] + summary["rows_duplicates_skipped"]

    with get_connection(str(db_path)) as conn:
        assert count_price_bars(conn) == summary["rows_inserted"]
        ticker = conn.execute("SELECT ticker FROM price_bars ORDER BY ts LIMIT 1").fetchone()[0]
        assert ticker == "VALID"
        run_row = conn.execute(
            """
            SELECT
                import_batch_id,
                status,
                started_at,
                completed_at,
                failure_reason,
                stage_failed,
                files_discovered,
                rows_parsed,
                rows_valid,
                rows_invalid,
                rows_inserted,
                rows_duplicates_skipped
            FROM import_runs
            WHERE import_batch_id = ?
            """,
            ("test-batch-001",),
        ).fetchone()
        assert dict(run_row) == {
            "import_batch_id": "test-batch-001",
            "status": "completed",
            "started_at": run_row["started_at"],
            "completed_at": run_row["completed_at"],
            "failure_reason": None,
            "stage_failed": None,
            "files_discovered": 1,
            "rows_parsed": 4,
            "rows_valid": 4,
            "rows_invalid": 0,
            "rows_inserted": 4,
            "rows_duplicates_skipped": 0,
        }
        assert run_row["started_at"]
        assert run_row["completed_at"]


def test_import_valid_daily_csv_rerun_counts_duplicates_without_new_inserts(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    fixture_path = Path("tests/fixtures/valid_daily.csv")
    shutil.copy(fixture_path, input_dir / fixture_path.name)

    db_path = tmp_path / "stock_data.sqlite3"
    schema_path = "app/db/schema.sql"

    first_summary = run_import(
        input_dir=str(input_dir),
        db_path=str(db_path),
        schema_path=schema_path,
        import_batch_id="test-batch-rerun-001",
    )
    second_summary = run_import(
        input_dir=str(input_dir),
        db_path=str(db_path),
        schema_path=schema_path,
        import_batch_id="test-batch-rerun-002",
    )

    assert first_summary == {
        "files_discovered": 1,
        "rows_parsed": 4,
        "rows_valid": 4,
        "rows_invalid": 0,
        "rows_inserted": 4,
        "rows_duplicates_skipped": 0,
    }
    assert second_summary == {
        "files_discovered": 1,
        "rows_parsed": 4,
        "rows_valid": 4,
        "rows_invalid": 0,
        "rows_inserted": 0,
        "rows_duplicates_skipped": 4,
    }

    with get_connection(str(db_path)) as conn:
        assert count_price_bars(conn) == 4
        run_rows = conn.execute(
            """
            SELECT import_batch_id, status, rows_inserted, rows_duplicates_skipped
            FROM import_runs
            ORDER BY import_batch_id
            """
        ).fetchall()
        assert [dict(row) for row in run_rows] == [
            {
                "import_batch_id": "test-batch-rerun-001",
                "status": "completed",
                "rows_inserted": 4,
                "rows_duplicates_skipped": 0,
            },
            {
                "import_batch_id": "test-batch-rerun-002",
                "status": "completed",
                "rows_inserted": 0,
                "rows_duplicates_skipped": 4,
            },
        ]


def test_import_run_marks_failed_when_execution_errors_after_run_start(tmp_path: Path) -> None:
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
    schema_path = "app/db/schema.sql"

    with pytest.raises(PermissionError):
        run_import(
            input_dir=str(input_dir),
            db_path=str(db_path),
            schema_path=schema_path,
            import_batch_id="test-batch-failed-001",
        )

    with get_connection(str(db_path)) as conn:
        run_row = conn.execute(
            """
            SELECT
                import_batch_id,
                status,
                started_at,
                completed_at,
                failure_reason,
                stage_failed,
                files_discovered,
                rows_parsed,
                rows_valid,
                rows_invalid,
                rows_inserted,
                rows_duplicates_skipped
            FROM import_runs
            WHERE import_batch_id = ?
            """,
            ("test-batch-failed-001",),
        ).fetchone()

        assert dict(run_row) == {
            "import_batch_id": "test-batch-failed-001",
            "status": "failed",
            "started_at": run_row["started_at"],
            "completed_at": run_row["completed_at"],
            "failure_reason": run_row["failure_reason"],
            "stage_failed": "parse",
            "files_discovered": 1,
            "rows_parsed": 0,
            "rows_valid": 0,
            "rows_invalid": 0,
            "rows_inserted": 0,
            "rows_duplicates_skipped": 0,
        }
        assert run_row["started_at"]
        assert run_row["completed_at"]
        assert run_row["failure_reason"]
        assert count_price_bars(conn) == 0
    os.chmod(broken_file, 0o644)


def test_failed_second_file_preserves_first_file_commit_and_marks_run_failed(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    valid_fixture = Path("tests/fixtures/valid_daily.csv")
    shutil.copy(valid_fixture, input_dir / "a_valid_daily.csv")

    broken_file = input_dir / "z_broken_daily.csv"
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
            import_batch_id="test-batch-failed-second-file-001",
        )

    with get_connection(str(db_path)) as conn:
        assert count_price_bars(conn) == 4
        run_row = conn.execute(
            """
            SELECT
                status,
                failure_reason,
                stage_failed,
                files_discovered,
                rows_parsed,
                rows_valid,
                rows_invalid,
                rows_inserted,
                rows_duplicates_skipped
            FROM import_runs
            WHERE import_batch_id = ?
            """,
            ("test-batch-failed-second-file-001",),
        ).fetchone()
        assert dict(run_row) == {
            "status": "failed",
            "failure_reason": run_row["failure_reason"],
            "stage_failed": "parse",
            "files_discovered": 2,
            "rows_parsed": 4,
            "rows_valid": 4,
            "rows_invalid": 0,
            "rows_inserted": 4,
            "rows_duplicates_skipped": 0,
        }
        assert run_row["failure_reason"]

    os.chmod(broken_file, 0o644)
