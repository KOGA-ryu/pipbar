# research/evaluate.py Contract

## Purpose

`evaluate.py` computes **evaluation metrics** for model predictions against true targets.

It compares predicted values to actual label values and produces a stable, deterministic metric summary.

This module is **metrics-only**:
- no model training
- no dataset loading
- no file I/O
- no orchestration

---

## First-pass metrics (locked)

- `mae = mean(abs(y_true - y_pred))`
- `mse = mean((y_true - y_pred)^2)`
- `rmse = sqrt(mse)`
- `directional_accuracy`

---

## Directional accuracy definition

Defined as:

- proportion of rows where `sign(y_true) == sign(y_pred)`

Rules:
- rows where `y_true == 0` are excluded
- rows where `y_pred == 0` are included

---

## Input contract

The evaluator receives:

```text
y_true: list[float]
y_pred: list[float]
```

Inputs must:
- be equal length
- be aligned by index

---

## Length mismatch behavior

If lengths differ:

- raise error immediately
- do not attempt partial evaluation

---

## Empty input behavior

If input lists are empty:

- return metrics as `None`
- do not raise

---

## Invalid values

If values contain:

- `None`
- non-numeric values
- `NaN`, `inf`, `-inf`

Then:

- raise error
- do not attempt filtering

---

## Output shape

Returns:

```text
EvaluationResult:
  mae: float | None
  mse: float | None
  rmse: float | None
  directional_accuracy: float | None
```

---

## Computation rules

- use only standard library math
- no external dependencies
- calculations must be deterministic

---

## Responsibility boundaries

`evaluate.py`:
- computes metrics only

It does **not**:
- read datasets
- train models
- format reports
- access database

---

## Determinism

Given identical inputs, output must be identical.

---

## Summary

This module answers:

> "How good are the predictions compared to the true targets?"

Nothing more.
