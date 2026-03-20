from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from app.db.connection import get_connection
from app.db.queries import count_price_bar_features
from app.features.feature_runner import run_feature_generation
from app.services.import_runner import run_import


def test_feature_generation_end_to_end_and_rerun_duplicates(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    fixture_path = Path("tests/fixtures/valid_daily.csv")
    shutil.copy(fixture_path, input_dir / fixture_path.name)

    db_path = tmp_path / "stock_data.sqlite3"
    run_import(
        input_dir=str(input_dir),
        db_path=str(db_path),
        schema_path="app/db/schema.sql",
        import_batch_id="test-feature-import-001",
    )

    first_summary = run_feature_generation(
        db_path=str(db_path),
        ticker="VALID",
        timeframe="1d",
        start_ts=None,
        end_ts=None,
        feature_batch_id="feature-batch-001",
    )
    second_summary = run_feature_generation(
        db_path=str(db_path),
        ticker="VALID",
        timeframe="1d",
        start_ts=None,
        end_ts=None,
        feature_batch_id="feature-batch-002",
    )

    assert first_summary == {
        "rows_selected": 4,
        "rows_derived": 4,
        "rows_valid": 4,
        "rows_invalid": 0,
        "rows_inserted": 4,
        "rows_duplicates_skipped": 0,
        "feature_batch_id": "feature-batch-001",
    }
    assert second_summary == {
        "rows_selected": 4,
        "rows_derived": 4,
        "rows_valid": 4,
        "rows_invalid": 0,
        "rows_inserted": 0,
        "rows_duplicates_skipped": 4,
        "feature_batch_id": "feature-batch-002",
    }

    with get_connection(str(db_path)) as conn:
        assert count_price_bar_features(conn) == 4
        rows = conn.execute(
            """
            SELECT ticker, timeframe, ts, close_1d_return, high_low_range, close_open_delta, feature_batch_id
            FROM price_bar_features
            ORDER BY ts
            """
        ).fetchall()

    actual_rows = [dict(row) for row in rows]

    assert [
        {
            "ticker": row["ticker"],
            "timeframe": row["timeframe"],
            "ts": row["ts"],
            "feature_batch_id": row["feature_batch_id"],
        }
        for row in actual_rows
    ] == [
        {
            "ticker": "VALID",
            "timeframe": "1d",
            "ts": "2024-01-02T00:00:00Z",
            "feature_batch_id": "feature-batch-001",
        },
        {
            "ticker": "VALID",
            "timeframe": "1d",
            "ts": "2024-01-03T00:00:00Z",
            "feature_batch_id": "feature-batch-001",
        },
        {
            "ticker": "VALID",
            "timeframe": "1d",
            "ts": "2024-01-04T00:00:00Z",
            "feature_batch_id": "feature-batch-001",
        },
        {
            "ticker": "VALID",
            "timeframe": "1d",
            "ts": "2024-01-05T00:00:00Z",
            "feature_batch_id": "feature-batch-001",
        },
    ]

    assert actual_rows[0]["close_1d_return"] is None
    assert actual_rows[0]["high_low_range"] == pytest.approx(4.55)
    assert actual_rows[0]["close_open_delta"] == pytest.approx(-1.51)

    assert actual_rows[1]["close_1d_return"] == pytest.approx(-0.007487610428786955)
    assert actual_rows[1]["high_low_range"] == pytest.approx(2.45)
    assert actual_rows[1]["close_open_delta"] == pytest.approx(0.03)

    assert actual_rows[2]["close_1d_return"] == pytest.approx(-0.012700135685210266)
    assert actual_rows[2]["high_low_range"] == pytest.approx(2.21)
    assert actual_rows[2]["close_open_delta"] == pytest.approx(-0.24)

    assert actual_rows[3]["close_1d_return"] == pytest.approx(0.014897477873674844)
    assert actual_rows[3]["high_low_range"] == pytest.approx(3.43)
    assert actual_rows[3]["close_open_delta"] == pytest.approx(2.63)
