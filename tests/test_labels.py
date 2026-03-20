from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from app.db.connection import get_connection
from app.db.queries import count_price_bar_labels
from app.labels.label_runner import run_label_generation
from app.services.import_runner import run_import


def test_label_generation_end_to_end_and_rerun_duplicates(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    fixture_path = Path("tests/fixtures/valid_daily.csv")
    shutil.copy(fixture_path, input_dir / fixture_path.name)

    db_path = tmp_path / "stock_data.sqlite3"
    run_import(
        input_dir=str(input_dir),
        db_path=str(db_path),
        schema_path="app/db/schema.sql",
        import_batch_id="test-label-import-001",
    )

    first_summary = run_label_generation(
        db_path=str(db_path),
        ticker="VALID",
        timeframe="1d",
        start_ts=None,
        end_ts=None,
        label_batch_id="label-batch-001",
    )
    second_summary = run_label_generation(
        db_path=str(db_path),
        ticker="VALID",
        timeframe="1d",
        start_ts=None,
        end_ts=None,
        label_batch_id="label-batch-002",
    )

    assert first_summary == {
        "rows_selected": 4,
        "rows_derived": 4,
        "rows_valid": 4,
        "rows_invalid": 0,
        "rows_inserted": 4,
        "rows_duplicates_skipped": 0,
        "label_batch_id": "label-batch-001",
    }
    assert second_summary == {
        "rows_selected": 4,
        "rows_derived": 4,
        "rows_valid": 4,
        "rows_invalid": 0,
        "rows_inserted": 0,
        "rows_duplicates_skipped": 4,
        "label_batch_id": "label-batch-002",
    }

    with get_connection(str(db_path)) as conn:
        assert count_price_bar_labels(conn) == 4
        rows = conn.execute(
            """
            SELECT ticker, timeframe, ts, next_1d_return, label_batch_id
            FROM price_bar_labels
            ORDER BY ts
            """
        ).fetchall()

    actual_rows = [dict(row) for row in rows]

    assert [
        {
            "ticker": row["ticker"],
            "timeframe": row["timeframe"],
            "ts": row["ts"],
            "label_batch_id": row["label_batch_id"],
        }
        for row in actual_rows
    ] == [
        {
            "ticker": "VALID",
            "timeframe": "1d",
            "ts": "2024-01-02T00:00:00Z",
            "label_batch_id": "label-batch-001",
        },
        {
            "ticker": "VALID",
            "timeframe": "1d",
            "ts": "2024-01-03T00:00:00Z",
            "label_batch_id": "label-batch-001",
        },
        {
            "ticker": "VALID",
            "timeframe": "1d",
            "ts": "2024-01-04T00:00:00Z",
            "label_batch_id": "label-batch-001",
        },
        {
            "ticker": "VALID",
            "timeframe": "1d",
            "ts": "2024-01-05T00:00:00Z",
            "label_batch_id": "label-batch-001",
        },
    ]

    assert actual_rows[0]["next_1d_return"] == pytest.approx(-0.007487610428786873)
    assert actual_rows[1]["next_1d_return"] == pytest.approx(-0.012700135685210334)
    assert actual_rows[2]["next_1d_return"] == pytest.approx(0.014897476774229146)
    assert actual_rows[3]["next_1d_return"] is None
