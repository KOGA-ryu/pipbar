from __future__ import annotations

from app.models.dataset_row import DatasetRow


BASELINE_NAME = "zero_return_baseline"


def predict(rows: list[DatasetRow] | list[list[float]]) -> list[float]:
    return [0.0 for _ in rows]
