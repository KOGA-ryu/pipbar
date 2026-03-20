from __future__ import annotations

import shutil
from pathlib import Path

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

    assert db_path.exists()
    assert summary["files_discovered"] == 1
    assert summary["rows_parsed"] == 4
    assert summary["rows_valid"] == 4
    assert summary["rows_invalid"] == 0
    assert summary["rows_inserted"] == 4

    with get_connection(str(db_path)) as conn:
        assert count_price_bars(conn) == 4
        ticker = conn.execute("SELECT ticker FROM price_bars ORDER BY ts LIMIT 1").fetchone()[0]
        assert ticker == "VALID"
