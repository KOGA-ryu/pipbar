from __future__ import annotations

from app.db.connection import get_connection
from app.db.init_db import init_db
from app.db.queries import count_price_bars
from app.models.candidate_row import CandidateRow
from app.models.price_bar import PriceBar
from app.pipeline.load import load_valid_records
from app.pipeline.normalize import normalize_rows
from app.pipeline.parse import parse_csv_file
from app.pipeline.validate import validate_records


def test_invalid_ohlc_rows_are_rejected_with_issues_and_not_inserted(tmp_path) -> None:
    db_path = tmp_path / "stock_data.sqlite3"
    init_db(str(db_path), "app/db/schema.sql")

    raw_rows = parse_csv_file("tests/fixtures/invalid_ohlc.csv")
    records = normalize_rows(raw_rows, ticker="INVALID", import_batch_id="test-batch-invalid")
    valid_records, invalid_records = validate_records(records)

    assert len(valid_records) == 0
    assert len(invalid_records) == 1
    assert invalid_records[0]["raw_row"] == raw_rows[0]
    assert invalid_records[0]["issues"] == [
        "high must be >= low",
        "open must be between low and high",
        "close must be between low and high",
    ]

    with get_connection(str(db_path)) as conn:
        load_result = load_valid_records(conn, valid_records)

        assert load_result == {
            "rows_inserted": 0,
            "rows_duplicates_skipped": 0,
        }
        assert count_price_bars(conn) == 0


def test_negative_numeric_rows_are_rejected_with_issues_and_not_inserted(tmp_path) -> None:
    db_path = tmp_path / "stock_data.sqlite3"
    init_db(str(db_path), "app/db/schema.sql")

    raw_rows = parse_csv_file("tests/fixtures/invalid_negative_values.csv")
    records = normalize_rows(raw_rows, ticker="INVALID", import_batch_id="test-batch-negative")
    valid_records, invalid_records = validate_records(records)

    assert len(valid_records) == 0
    assert len(invalid_records) == 1
    assert invalid_records[0]["raw_row"] == raw_rows[0]
    assert invalid_records[0]["issues"] == [
        "open must be >= 0",
        "volume must be >= 0",
    ]

    with get_connection(str(db_path)) as conn:
        load_result = load_valid_records(conn, valid_records)

        assert load_result == {
            "rows_inserted": 0,
            "rows_duplicates_skipped": 0,
        }
        assert count_price_bars(conn) == 0


def test_missing_required_fields_are_rejected_with_issues_and_not_inserted(tmp_path) -> None:
    db_path = tmp_path / "stock_data.sqlite3"
    init_db(str(db_path), "app/db/schema.sql")

    raw_rows = parse_csv_file("tests/fixtures/invalid_missing_fields.csv")
    records = [
        CandidateRow(
            raw_row=raw_rows[0],
            record=PriceBar(
                ticker="INVALID",
                timeframe="1d",
                ts="",
                open=None,
                high=188.44,
                low=183.89,
                close=185.64,
                volume=None,
                source="",
                import_batch_id="",
            ),
            issues=[],
        )
    ]
    valid_records, invalid_records = validate_records(records)

    assert len(valid_records) == 0
    assert len(invalid_records) == 1
    assert invalid_records[0]["raw_row"] == raw_rows[0]
    assert invalid_records[0]["issues"] == [
        "ts is required",
        "source is required",
        "import_batch_id is required",
        "open is required",
        "volume is required",
    ]


def test_normalization_failures_become_invalid_records_with_raw_row_preserved() -> None:
    raw_rows = [
        {
            "date": "2024-01-02",
            "open": "bad-float",
            "high": "188.44",
            "low": "183.89",
            "close": "185.64",
            "volume": "82488700",
        }
    ]

    records = normalize_rows(raw_rows, ticker="aapl", import_batch_id="batch-001")
    valid_records, invalid_records = validate_records(records)

    assert len(valid_records) == 0
    assert len(invalid_records) == 1
    assert invalid_records[0]["raw_row"] == raw_rows[0]
    assert invalid_records[0]["record"] is None
    assert invalid_records[0]["issues"] == ["could not convert string to float: 'bad-float'"]
