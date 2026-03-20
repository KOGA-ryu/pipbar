from __future__ import annotations

from app.models.research_result import ResearchResult


def build_research_result(
    dataset_batch_id: str,
    target_column: str,
    feature_columns: list[str],
    baseline_name: str,
    rows_train: int,
    rows_validation: int,
    rows_test: int,
    mae: float | None,
    mse: float | None,
    rmse: float | None,
    directional_accuracy: float | None,
) -> ResearchResult:
    return ResearchResult(
        dataset_batch_id=dataset_batch_id,
        target_column=target_column,
        feature_columns=feature_columns,
        baseline_name=baseline_name,
        rows_train=rows_train,
        rows_validation=rows_validation,
        rows_test=rows_test,
        mae=mae,
        mse=mse,
        rmse=rmse,
        directional_accuracy=directional_accuracy,
    )


def print_research_result(result: ResearchResult) -> None:
    print(result)
