from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

from app.db.connection import get_connection
from app.services.import_runner import run_import


def test_completed_run_has_completed_status_and_timestamps(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    fixture_path = Path("tests/fixtures/valid_daily.csv")
    shutil.copy(fixture_path, input_dir / fixture_path.name)

    db_path = tmp_path / "stock_data.sqlite3"
    run_import(
        input_dir=str(input_dir),
        db_path=str(db_path),
        schema_path="app/db/schema.sql",
        import_batch_id="test-lifecycle-completed-001",
    )

    with get_connection(str(db_path)) as conn:
        run_row = conn.execute(
            """
            SELECT status, started_at, completed_at, failure_reason, stage_failed
            FROM import_runs
            WHERE import_batch_id = ?
            """,
            ("test-lifecycle-completed-001",),
        ).fetchone()

        assert dict(run_row) == {
            "status": "completed",
            "started_at": run_row["started_at"],
            "completed_at": run_row["completed_at"],
            "failure_reason": None,
            "stage_failed": None,
        }
        assert run_row["started_at"]
        assert run_row["completed_at"]


def test_failed_run_has_failed_status_and_timestamps(tmp_path: Path) -> None:
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
            import_batch_id="test-lifecycle-failed-001",
        )

    with get_connection(str(db_path)) as conn:
        run_row = conn.execute(
            """
            SELECT status, started_at, completed_at, failure_reason, stage_failed
            FROM import_runs
            WHERE import_batch_id = ?
            """,
            ("test-lifecycle-failed-001",),
        ).fetchone()

        assert dict(run_row) == {
            "status": "failed",
            "started_at": run_row["started_at"],
            "completed_at": run_row["completed_at"],
            "failure_reason": run_row["failure_reason"],
            "stage_failed": "parse",
        }
        assert run_row["started_at"]
        assert run_row["completed_at"]
        assert run_row["failure_reason"]
    os.chmod(broken_file, 0o644)


def test_completed_test_paths_do_not_persist_running_as_final_status(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    fixture_path = Path("tests/fixtures/valid_daily.csv")
    shutil.copy(fixture_path, input_dir / fixture_path.name)

    db_path = tmp_path / "stock_data.sqlite3"
    run_import(
        input_dir=str(input_dir),
        db_path=str(db_path),
        schema_path="app/db/schema.sql",
        import_batch_id="test-lifecycle-final-state-001",
    )

    with get_connection(str(db_path)) as conn:
        statuses = [
            row[0]
            for row in conn.execute(
                "SELECT status FROM import_runs WHERE import_batch_id = ?",
                ("test-lifecycle-final-state-001",),
            ).fetchall()
        ]

    assert statuses == ["completed"]
