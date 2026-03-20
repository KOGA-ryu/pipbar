# datasets/dataset_runner.py Questions

- What is the exact stage order for dataset assembly?
- Should it be `select -> assemble -> split -> export -> report`?
- What inputs must the dataset runner accept on first pass?
- Does it need output directory, ticker/timeframe/date range, split policy, and selected columns?
- What counts/shapes must it summarize?
- What is a successful zero-row dataset run versus a failure?
- Which errors should fail the run immediately?
- Should this runner ever derive features or labels? If not, state that explicitly.
- Does dataset assembly need its own persisted run tracking now, or can it remain file-output only at first?

# datasets/dataset_runner.py Contract

## Purpose

`dataset_runner.py` orchestrates the first-pass dataset assembly pipeline.

It is responsible for running dataset stages in order and producing a final summary.

It does **not** derive features, derive labels, or perform model work.

---

## Stage order

First-pass stage order is:

```text
select -> assemble -> split -> export -> report
```

This order is fixed for the first version.

---

## First-pass inputs

The runner must accept only the inputs needed to assemble a research-ready dataset.

Required first-pass inputs:

- `db_path: str`
- `output_path: str`
- `ticker: str | None`
- `timeframe: str`
- `start_ts: str | None`
- `end_ts: str | None`
- `split_policy: str`
- `selected_feature_columns: list[str] | None`
- `selected_label_columns: list[str] | None`
- `dataset_batch_id: str`

Notes:
- `ticker` may be optional for later multi-ticker work, but first pass may still use one ticker.
- `selected_feature_columns` and `selected_label_columns` may default to the first-pass contract if omitted.

---

## Output

The runner returns a summary object describing the dataset build.

It may also write one or more output files depending on split/export behavior.

---

## First-pass summary fields

The summary must include at minimum:

- `rows_selected`
- `rows_assembled`
- `rows_train`
- `rows_validation`
- `rows_test`
- `files_written`
- `output_path`
- `dataset_batch_id`

These counts must be explicit and nonnegative.

---

## Successful zero-row run vs failure

A zero-row run is **successful** if:

- stages execute correctly
- no system error occurs
- output summary is honest
- split/export behavior remains valid for zero rows

A zero-row run is **not** automatically a failure.

Failure means:
- stage contract breaks
- database read fails
- assembly fails
- split logic fails
- export fails
- report assembly fails

---

## Immediate-failure conditions

The runner should fail immediately on:

- unreadable or missing database
- invalid stage output shape
- assembly contract breach
- invalid split policy
- export write failure
- explicit internal invariant failure

The runner should not fail merely because the selected dataset is empty.

---

## Responsibility boundaries

`dataset_runner.py`:
- orchestrates dataset pipeline stages
- passes inputs to each stage
- returns final summary

It does **not**:
- derive features
- derive labels
- query raw CSV files
- train models
- score models
- run backtests

Feature and label generation must already be completed before dataset assembly begins.

---

## Persisted run tracking

First pass does **not** require dataset-run persistence in SQLite.

For first pass, file-output + returned summary is sufficient.

A persisted `dataset_runs` table may be added later if dataset production becomes operationally important.

---

## Determinism

Given the same database contents, runner inputs, split policy, and selected columns, the runner must produce the same assembled dataset and the same summary.

---

## Summary

This runner answers:

> "How do we build and deliver a research-ready dataset from trusted bars, features, and labels?"

Nothing more.