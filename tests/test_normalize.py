from __future__ import annotations

from app.pipeline.normalize import normalize_rows
from app.pipeline.parse import parse_csv_file


def test_normalize_rows_converts_fixture_row_to_candidate_with_canonical_record() -> None:
    raw_rows = parse_csv_file("tests/fixtures/valid_daily.csv")

    candidates = normalize_rows(raw_rows[:1], ticker="aapl", import_batch_id="batch-001")

    assert len(candidates) == 1
    assert candidates[0].raw_row == raw_rows[0]
    assert candidates[0].issues == []
    assert candidates[0].record is not None
    assert candidates[0].record.ticker == "AAPL"
    assert candidates[0].record.timeframe == "1d"
    assert candidates[0].record.ts == "2024-01-02T00:00:00Z"
    assert candidates[0].record.open == 187.15
    assert isinstance(candidates[0].record.open, float)
    assert candidates[0].record.high == 188.44
    assert isinstance(candidates[0].record.high, float)
    assert candidates[0].record.low == 183.89
    assert isinstance(candidates[0].record.low, float)
    assert candidates[0].record.close == 185.64
    assert isinstance(candidates[0].record.close, float)
    assert candidates[0].record.volume == 82488700
    assert isinstance(candidates[0].record.volume, int)
    assert candidates[0].record.source == "massive_csv"
    assert candidates[0].record.import_batch_id == "batch-001"


def test_normalize_rows_returns_candidate_failure_on_malformed_numeric_value() -> None:
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

    candidates = normalize_rows(raw_rows, ticker="aapl", import_batch_id="batch-001")

    assert len(candidates) == 1
    assert candidates[0].raw_row == raw_rows[0]
    assert candidates[0].record is None
    assert candidates[0].issues == ["could not convert string to float: 'bad-float'"]
