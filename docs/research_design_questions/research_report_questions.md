# research/report.py Contract

## Purpose

`report.py` builds the **research run summary**.

It converts evaluation outputs and run metadata into a stable, structured result.

This module is **summary-only**:
- no model execution
- no metric computation
- no dataset loading
- no file I/O

---

## Summary inputs

All values are passed in from upstream stages:

- model predictions already computed
- evaluation metrics already computed
- dataset metadata already known

`report.py` must not recompute anything.

---

## Required fields (first pass)

Every research run summary MUST include:

- `dataset_batch_id: str`
- `baseline_name: str`
- `target_column: str`
- `feature_columns: list[str]`

- `rows_train: int`
- `rows_validation: int`
- `rows_test: int`

- `mae: float | None`
- `mse: float | None`
- `rmse: float | None`
- `directional_accuracy: float | None`

---

## Output type

Primary output is a **typed object**:

```
ResearchResult
```

A dict representation may be produced secondarily if needed.

---

## Zero-row and missing metric behavior

If `rows_test == 0`:

- metrics must be `None`
- no exception is raised
- summary is still valid

---

## Naming ownership

`report.py` owns final naming of:

- `baseline_name`
- `target_column`
- `feature_columns`

Names must be:
- stable
- explicit
- not recomputed elsewhere

---

## Invariants

For completed runs:

```text
rows_train >= 0
rows_validation >= 0
rows_test >= 0
```

No metric should exist if its required inputs are missing.

---

## Optional human-readable output

Human-readable formatting may exist, but must:

- be separate from result construction
- not affect returned data

---

## Responsibility boundaries

`report.py`:
- builds the research result object
- formats summary data

It does **not**:
- compute metrics
- train models
- read datasets
- write files

---

## Determinism

Given identical inputs, output must be identical.

---

## Summary

This module answers:

> "What is the final structured result of this research run?"

Nothing more.
