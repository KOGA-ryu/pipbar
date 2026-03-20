from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ResearchResult:
    dataset_batch_id: str
    target_column: str
    feature_columns: list[str]
    baseline_name: str
    rows_train: int
    rows_validation: int
    rows_test: int
    mae: float | None
    mse: float | None
    rmse: float | None
    directional_accuracy: float | None
