# features/feature_runner.py Contract

## Purpose

`feature_runner.py` orchestrates the feature generation pipeline.

It executes feature stages in order and produces a summary of the feature run.

It does **not** compute features itself or perform database queries directly.

---

## Stage order

First-pass stage order is:

```text
select -> derive -> validate -> load -> report
```

This order is fixed for the first version.

---

## First-pass inputs

The runner must accept:

- `db_path: str`
- `ticker: str | None`
- `timeframe: str`
- `start_ts: str | None`
- `end_ts: str | None`
- `feature_batch_id: str`

Notes:
- `feature_batch_id` is passed in, not generated inside the runner

---

## Output

The runner returns a summary describing the feature run.

---

## First-pass summary fields

The summary must include at minimum:

- `rows_selected`
- `rows_derived`
- `rows_valid`
- `rows_invalid`
- `rows_inserted`
- `rows_duplicates_skipped`
- `feature_batch_id`

All counts must be explicit and nonnegative.

---

## Zero-row behavior

A zero-row run is **successful** if:

- no system errors occur
- stages execute correctly
- summary reflects zero rows

Zero selected bars is not a failure.

---

## Failure conditions

The runner should fail on:

- database access failure
- invalid stage output shape
- feature derivation contract breach
- validation contract failure
- load failure (excluding duplicates)
- invariant violation

Failures must:
- mark run as failed if tracking exists
- re-raise exception

---

## Responsibility boundaries

`feature_runner.py`:
- orchestrates stages
- aggregates counts
- returns summary

It does **not**:
- compute feature formulas
- perform SQL queries directly
- derive labels
- assemble datasets
- train models

---

## Transaction boundaries

First pass uses:

- commit per selection batch (typically per ticker/timeframe slice)

Not per row, not full-run atomic.

---

## Run tracking (first pass)

Feature run tracking is **not required** in SQLite for first pass.

`feature_batch_id` is sufficient for traceability.

---

## Determinism

Given identical DB state and inputs, the runner must produce identical results and summary.

---

## Invariants (completed run)

Must hold for completed runs:

```text
rows_selected >= rows_derived
rows_derived >= rows_valid
rows_valid = rows_inserted + rows_duplicates_skipped
rows_invalid >= 0
```

---

## First end-to-end test

The first test must prove:

- bars are selected from `price_bars`
- features are derived correctly
- valid rows are inserted into `price_bar_features`
- duplicates are skipped correctly
- summary counts are correct
- rerun produces duplicate-only behavior

---

## Summary

This module answers:

> "How do we run feature generation end-to-end on trusted bars?"

Nothing more.
