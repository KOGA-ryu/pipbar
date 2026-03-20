from __future__ import annotations

import math


def evaluate_predictions(y_true: list[float], y_pred: list[float]) -> dict[str, float | None]:
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have equal length")

    if not y_true:
        return {
            "mae": None,
            "mse": None,
            "rmse": None,
            "directional_accuracy": None,
        }

    for value in [*y_true, *y_pred]:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("all metric inputs must be numeric")
        if not math.isfinite(float(value)):
            raise ValueError("all metric inputs must be finite")

    absolute_errors = [abs(actual - predicted) for actual, predicted in zip(y_true, y_pred, strict=True)]
    squared_errors = [(actual - predicted) ** 2 for actual, predicted in zip(y_true, y_pred, strict=True)]
    mse = sum(squared_errors) / len(squared_errors)

    directional_pairs = [
        (_sign(actual), _sign(predicted))
        for actual, predicted in zip(y_true, y_pred, strict=True)
        if actual != 0
    ]
    directional_accuracy = None
    if directional_pairs:
        matches = sum(1 for actual_sign, predicted_sign in directional_pairs if actual_sign == predicted_sign)
        directional_accuracy = matches / len(directional_pairs)

    return {
        "mae": sum(absolute_errors) / len(absolute_errors),
        "mse": mse,
        "rmse": math.sqrt(mse),
        "directional_accuracy": directional_accuracy,
    }


def _sign(value: float) -> int:
    if value < 0:
        return -1
    if value > 0:
        return 1
    return 0
