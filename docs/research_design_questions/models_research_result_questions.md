# models/research_result.py Contract

## Purpose

`research_result.py` defines the **typed result shape** for a single research run.

It represents the outcome of one baseline experiment over a specific dataset.

This model is a **plain typed container**:
- no SQL
- no file I/O
- no orchestration logic

---

## First-pass requirement

A typed model is **required** for first pass.

Reason:
- stabilizes result shape across runs
- prevents ad hoc dict drift in research code

---

## Required fields (first pass)

Every `ResearchResult` MUST include:

- `dataset_batch_id: str`
- `target_column: str`
- `feature_columns: list[str]`
- `baseline_name: str`

- `rows_train: int`
- `rows_validation: int`
- `rows_test: int`

- `mae: float | None`
- `mse: float | None`
- `rmse: float | None`
- `directional_accuracy: float | None`

---

## Field semantics

- `dataset_batch_id` → identifies dataset used
- `target_column` → name of supervised target (e.g. `next_1d_return`)
- `feature_columns` → exact list of features used
- `baseline_name` → identifier for experiment method (e.g. `linear_regression`, `naive_zero`)

- `rows_*` → counts used in each split

- metrics:
  - `mae` → mean absolute error
  - `mse` → mean squared error
  - `rmse` → root mean squared error
  - `directional_accuracy` → optional; proportion of correct sign predictions

---

## Nullability rules

- `mae`, `mse`, `rmse`, and `directional_accuracy` may be `None` when no evaluation rows are available
- all other fields must be non-null

---

## Method policy

`ResearchResult` must remain method-free.

No helpers like:
- serialization
- formatting
- persistence

---

## Width policy

First pass keeps this model minimal:

- identifiers (dataset + config)
- row counts
- core metrics

Do not add:
- model parameters
- hyperparameters
- prediction arrays
- per-row outputs
- experiment history

---

## Output role

`ResearchResult` is produced by:
- `research/report.py`

It may be returned by:
- `research/research_runner.py`

---

## Responsibility boundaries

`research_result.py`:
- defines result shape only

It does **not**:
- compute metrics
- run models
- load datasets
- persist results

---

## Determinism

Given identical inputs and model behavior, identical `ResearchResult` values must be produced.

---

## Summary

This model answers:

> "What is the exact structured output of a single research run?"

Nothing more.
