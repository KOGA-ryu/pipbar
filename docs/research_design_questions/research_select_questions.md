# research/select.py Contract

## Purpose

`select.py` reads **prepared dataset CSV files** and returns structured inputs for research execution.

It selects feature and target columns and ensures data is aligned for modeling.

This module is **data-loading only**:
- no model execution
- no metric computation
- no orchestration

---

## Data sources (first pass)

Reads from dataset export directory:

- `train.csv`
- `validation.csv` (optional)
- `test.csv`

Files are expected to exist under `dataset_path`.

---

## Required files

Minimum requirement:

- `test.csv` must exist

Optional:

- `train.csv`
- `validation.csv`

Missing optional files do not cause failure.

Missing `test.csv` is a failure.

---

## Column requirements

Each file MUST include:

- identifier columns:
  - `ticker`
  - `timeframe`
  - `ts`

- selected feature columns
- selected target column

---

## Feature and target selection

The module receives:

- `feature_columns: list[str]`
- `target_column: str`

Selection is **caller-defined**, not hardcoded.

---

## Missing column behavior

If any required column is missing:

- raise error immediately
- do not attempt partial loading

---

## Type coercion

- numeric columns are parsed as `float`
- blank values are treated as:
  - error for required fields
  - allowed only if contract permits (e.g. None-like values)

First pass behavior:
- blank feature/target values from exported warmup or terminal rows are loaded as `None`
- malformed non-numeric values still raise error

---

## Output structure

Returns a structured object:

```text
ResearchSelection:
  X_train: list[list[float]] | None
  y_train: list[float] | None

  X_validation: list[list[float]] | None
  y_validation: list[float] | None

  X_test: list[list[float]]
  y_test: list[float]
```

---

## Split behavior

- splits are returned separately
- no merging across splits

---

## Ordering guarantee

Rows must preserve CSV order.

No re-sorting occurs in this module.

---

## Empty split behavior

A split is valid if:

- file exists
- header is correct
- contains zero rows

Return empty lists for that split.

---

## Responsibility boundaries

`select.py`:
- reads dataset files
- selects columns
- converts to numeric arrays

It does **not**:
- compute metrics
- run models
- assemble datasets
- modify row ordering

---

## Determinism

Given identical input files, output must be identical.

---

## Summary

This module answers:

> "How do we load and prepare dataset splits for model execution?"

Nothing more.
