from __future__ import annotations

import shutil
from pathlib import Path

from app.db.connection import get_connection
from app.db.queries import count_price_bars, count_rejected_rows
from app.services.import_runner import run_import


def test_invalid_rows_are_persisted_to_rejected_rows_and_not_price_bars(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    fixture_path = Path("tests/fixtures/invalid_ohlc.csv")
    shutil.copy(fixture_path, input_dir / fixture_path.name)

    db_path = tmp_path / "stock_data.sqlite3"
    summary = run_import(
        input_dir=str(input_dir),
        db_path=str(db_path),
        schema_path="app/db/schema.sql",
        import_batch_id="test-branching-invalid-001",
    )

    assert summary == {
        "files_discovered": 1,
        "rows_parsed": 1,
        "rows_valid": 0,
        "rows_invalid": 1,
        "rows_inserted": 0,
        "rows_duplicates_skipped": 0,
    }

    with get_connection(str(db_path)) as conn:
        assert count_price_bars(conn) == 0
        assert count_rejected_rows(conn) == 1
        rejected_row = conn.execute(
            """
            SELECT ticker, file_path, raw_row_json, issues_json
            FROM rejected_rows
            WHERE import_batch_id = ?
            """,
            ("test-branching-invalid-001",),
        ).fetchone()
        assert dict(rejected_row) == {
            "ticker": "INVALID",
            "file_path": str(input_dir / fixture_path.name),
            "raw_row_json": '{"date": "2024-01-02", "open": "187.15", "high": "180.00", "low": "183.89", "close": "185.64", "volume": "82488700"}',
            "issues_json": '["high must be >= low", "open must be between low and high", "close must be between low and high"]',
        }


def test_duplicate_rerun_does_not_use_rejected_rows_or_increase_price_bars(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    fixture_path = Path("tests/fixtures/valid_daily.csv")
    shutil.copy(fixture_path, input_dir / fixture_path.name)

    db_path = tmp_path / "stock_data.sqlite3"
    run_import(
        input_dir=str(input_dir),
        db_path=str(db_path),
        schema_path="app/db/schema.sql",
        import_batch_id="test-branching-duplicate-001",
    )
    second_summary = run_import(
        input_dir=str(input_dir),
        db_path=str(db_path),
        schema_path="app/db/schema.sql",
        import_batch_id="test-branching-duplicate-002",
    )

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
        assert count_rejected_rows(conn) == 0
