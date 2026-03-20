from __future__ import annotations

from pathlib import Path

from app.db.connection import get_connection
from app.db.init_db import init_db
from app.db.queries import count_price_bars, create_import_run
from app.models.price_bar import PriceBar
from app.pipeline.load import load_valid_records


def test_load_valid_records_inserts_expected_rows_and_values(tmp_path: Path) -> None:
    db_path = tmp_path / "stock_data.sqlite3"
    init_db(str(db_path), "app/db/schema.sql")

    records = [
        PriceBar(
            ticker="AAPL",
            timeframe="1d",
            ts="2024-01-02T00:00:00Z",
            open=187.15,
            high=188.44,
            low=183.89,
            close=185.64,
            volume=82488700,
            source="massive_csv",
            import_batch_id="test-batch-load",
        ),
        PriceBar(
            ticker="AAPL",
            timeframe="1d",
            ts="2024-01-03T00:00:00Z",
            open=184.22,
            high=185.88,
            low=183.43,
            close=184.25,
            volume=58414500,
            source="massive_csv",
            import_batch_id="test-batch-load",
        ),
    ]

    with get_connection(str(db_path)) as conn:
        create_import_run(
            conn=conn,
            import_batch_id="test-batch-load",
            source="massive_csv",
            timeframe="1d",
            input_path="tests/fixtures/valid_daily.csv",
            status="running",
            started_at="2026-03-20T00:00:00Z",
        )

        load_result = load_valid_records(conn, records)

        assert load_result == {
            "rows_inserted": len(records),
            "rows_duplicates_skipped": 0,
        }
        assert count_price_bars(conn) == len(records)

        rows = conn.execute(
            """
            SELECT ticker, timeframe, ts, open, high, low, close, volume, source, import_batch_id
            FROM price_bars
            ORDER BY ts
            """
        ).fetchall()

    assert [dict(row) for row in rows] == [
        {
            "ticker": "AAPL",
            "timeframe": "1d",
            "ts": "2024-01-02T00:00:00Z",
            "open": 187.15,
            "high": 188.44,
            "low": 183.89,
            "close": 185.64,
            "volume": 82488700,
            "source": "massive_csv",
            "import_batch_id": "test-batch-load",
        },
        {
            "ticker": "AAPL",
            "timeframe": "1d",
            "ts": "2024-01-03T00:00:00Z",
            "open": 184.22,
            "high": 185.88,
            "low": 183.43,
            "close": 184.25,
            "volume": 58414500,
            "source": "massive_csv",
            "import_batch_id": "test-batch-load",
        },
    ]
