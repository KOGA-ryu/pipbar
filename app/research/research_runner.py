from __future__ import annotations

from app.models.research_result import ResearchResult
from app.research.baseline import BASELINE_NAME, predict
from app.research.evaluate import evaluate_predictions
from app.research.report import build_research_result, print_research_result
from app.research.select import select_research_inputs


def run_research(
    dataset_path: str,
    target_column: str,
    feature_columns: list[str],
    dataset_batch_id: str,
) -> ResearchResult:
    selected = select_research_inputs(
        dataset_path=dataset_path,
        feature_columns=feature_columns,
        target_column=target_column,
    )

    y_pred = predict(selected.X_test)
    y_true_evaluated: list[float] = []
    y_pred_evaluated: list[float] = []
    for actual, predicted in zip(selected.y_test, y_pred, strict=True):
        if actual is None:
            continue
        y_true_evaluated.append(actual)
        y_pred_evaluated.append(predicted)

    metrics = evaluate_predictions(y_true_evaluated, y_pred_evaluated)

    result = build_research_result(
        dataset_batch_id=dataset_batch_id,
        target_column=target_column,
        feature_columns=feature_columns,
        baseline_name=BASELINE_NAME,
        rows_train=0 if selected.X_train is None else len(selected.X_train),
        rows_validation=0 if selected.X_validation is None else len(selected.X_validation),
        rows_test=len(selected.X_test),
        mae=metrics["mae"],
        mse=metrics["mse"],
        rmse=metrics["rmse"],
        directional_accuracy=metrics["directional_accuracy"],
    )
    _assert_research_result_invariants(result)
    print_research_result(result)
    return result


def _assert_research_result_invariants(result: ResearchResult) -> None:
    assert result.rows_train >= 0
    assert result.rows_validation >= 0
    assert result.rows_test >= 0
    if result.rows_test == 0:
        assert result.mae is None
        assert result.mse is None
        assert result.rmse is None
    if result.mae is None:
        assert result.mae is None
        assert result.mse is None
        assert result.rmse is None
        assert result.directional_accuracy is None
