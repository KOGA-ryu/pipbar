# research/research_runner.py Contract

## Purpose

`research_runner.py` orchestrates the **research execution pipeline**.

It runs a single baseline experiment on a prepared dataset and returns a structured result.

This module is **orchestration-only**:
- no model math
- no metric computation
- no dataset assembly
- no file I/O

---

## Stage order

First-pass stage order is:

```text
select -> baseline -> evaluate -> report
```

No additional stages in first pass.

---

## First-pass inputs

The runner must accept:

- `dataset_path: str`
- `target_column: str`
- `feature_columns: list[str]`
- `dataset_batch_id: str`

Optional:
- `split_policy: str | None` (if needed to choose train/val/test files)

---

## Data sources

- reads **dataset CSV files only** (train/validation/test)
- does NOT read raw DB tables
- does NOT build datasets

---

## Output

Returns a typed result:

```
ResearchResult
```

---

## First-pass behavior

- load dataset splits from `dataset_path`
- select columns (`feature_columns`, `target_column`)
- run baseline predictions on test split (and optionally validation)
- compute metrics
- build result via `report.py`

---

## Zero-row behavior

A zero-row run is **successful** if:

- no system errors occur
- splits load correctly
- result is returned with `None` metrics

Zero rows in test split is not a failure.

---

## Failure conditions

The runner should fail on:

- missing dataset files
- malformed CSV structure
- missing required columns
- length mismatch between `y_true` and `y_pred`
- invariant violation

Failures must:
- raise exception
- not be swallowed

---

## Responsibility boundaries

`research_runner.py`:
- orchestrates research stages
- passes data between modules
- returns final result

It does **not**:
- read raw DB tables
- derive features
- derive labels
- assemble datasets
- train complex models

---

## Split usage policy

- train split: unused by first-pass baseline
- validation split: optional / may be unused
- test split: used for evaluation

No requirement to use all splits in first pass.

---

## Run tracking (first pass)

No persisted run tracking required.

Reason:
- research layer is exploratory
- results are returned, not stored

---

## Determinism

Given identical dataset files and inputs, the runner must produce identical results.

---

## Invariants (completed run)

```text
rows_train >= 0
rows_validation >= 0
rows_test >= 0
```

Metrics must be `None` if required inputs are absent.

---

## First end-to-end test

The first test must prove:

- dataset CSVs are loaded
- feature/target columns are selected correctly
- baseline produces predictions
- evaluation metrics are computed correctly
- result object is constructed correctly
- zero-row case returns valid result

---

## Summary

This module answers:

> "How do we run a complete baseline research experiment on prepared datasets?"

Nothing more.
