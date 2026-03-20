from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from app.datasets.dataset_runner import run_dataset_build
from app.features.feature_runner import run_feature_generation
from app.labels.label_runner import run_label_generation
from app.research.research_runner import run_research
from app.services.import_runner import run_import


def test_research_zero_baseline_end_to_end(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    fixture_path = Path("tests/fixtures/valid_daily.csv")
    shutil.copy(fixture_path, input_dir / fixture_path.name)

    db_path = tmp_path / "stock_data.sqlite3"
    dataset_dir = tmp_path / "dataset_output"

    run_import(
        input_dir=str(input_dir),
        db_path=str(db_path),
        schema_path="app/db/schema.sql",
        import_batch_id="test-research-import-001",
    )
    run_feature_generation(
        db_path=str(db_path),
        ticker="VALID",
        timeframe="1d",
        start_ts=None,
        end_ts=None,
        feature_batch_id="feature-batch-research-001",
    )
    run_label_generation(
        db_path=str(db_path),
        ticker="VALID",
        timeframe="1d",
        start_ts=None,
        end_ts=None,
        label_batch_id="label-batch-research-001",
    )
    run_dataset_build(
        db_path=str(db_path),
        output_path=str(dataset_dir),
        ticker="VALID",
        timeframe="1d",
        start_ts=None,
        end_ts=None,
        split_policy="time_70_15_15",
        selected_feature_columns=None,
        selected_label_columns=None,
        dataset_batch_id="dataset-batch-research-001",
    )

    result = run_research(
        dataset_path=str(dataset_dir),
        target_column="next_1d_return",
        feature_columns=["close_1d_return", "high_low_range", "close_open_delta"],
        dataset_batch_id="dataset-batch-research-001",
    )

    assert result.dataset_batch_id == "dataset-batch-research-001"
    assert result.target_column == "next_1d_return"
    assert result.feature_columns == ["close_1d_return", "high_low_range", "close_open_delta"]
    assert result.baseline_name == "zero_return_baseline"
    assert result.rows_train == 2
    assert result.rows_validation == 0
    assert result.rows_test == 2
    assert result.mae == pytest.approx(0.014897, rel=1e-6)
    assert result.mse == pytest.approx(0.000221920609, rel=1e-6)
    assert result.rmse == pytest.approx(0.014897, rel=1e-6)
    assert result.directional_accuracy == pytest.approx(0.0)
