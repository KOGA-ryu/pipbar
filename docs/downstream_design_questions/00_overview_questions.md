# Overview Questions

## Downstream Intent

- What is the first concrete downstream outcome this repo must support: feature table, label table, or exportable research dataset?
- Which downstream slice produces the highest leverage right now?
- What is explicitly out of scope for the next session?
- What downstream decisions must be locked before any new code or schema is created?

## Grain And Identity

- What is the canonical grain for features: one row per `(ticker, timeframe, ts)`?
- What is the canonical grain for labels: one row per `(ticker, timeframe, ts)` or future-anchor timestamp?
- What is the canonical grain for dataset rows?
- Must all downstream tables align exactly to `price_bars` identity `(ticker, timeframe, ts)`?
- Are there any downstream rows allowed to exist without a matching `price_bars` row?

## Table Strategy

- Which downstream tables should exist first: `price_bar_features`, `price_bar_labels`, both, or neither yet?
- Should features and labels use their own batch IDs, or reuse `import_batch_id` indirectly through joins?
- Do downstream runs need their own run-tracking tables now, or can existing `import_runs` be left ingestion-only?
- Which tables need uniqueness constraints on first pass?
- Which tables can safely defer duplicate policy until after the first vertical slice?

## Contracts

- Which feature columns are required for the first slice?
- Which label columns are required for the first slice?
- Which dataset columns are required for the first slice?
- Which values are nullable and why?
- Which stage outputs must be stable enough to become public internal contracts now?

## Operational Rules

- Should downstream pipelines be rerunnable and duplicate-safe from day one?
- What should count as a rejected downstream row versus a failed downstream run?
- What counts should every downstream summary include?
- Which invariants must hold for every completed downstream run?
- Which failure metadata rules from ingestion should carry over unchanged?

## Build Order

- Which folder should get the first real vertical slice: `features/`, `labels/`, or `datasets/`?
- What is the exact first-pass build order across schema, model, stages, runner, and tests?
- Which fixtures or temp-data builders are needed before coding begins?
- Which success criteria prove the first downstream slice is real?

# Downstream Overview Contract

## Purpose

This document defines the **first-pass downstream direction** for the pipbar system.

It converts open design questions into explicit, enforceable decisions that guide:

- feature pipeline
- label pipeline
- dataset assembly

No new downstream code should be written without alignment to this contract.

---

## Downstream Intent (locked)

First concrete downstream outcome:

```
exportable research dataset
```

This requires building, in order:

1. feature pipeline
2. label pipeline
3. dataset pipeline

---

## Out of scope (first slice)

Explicitly NOT included:

- ML models
- backtesting
- signal generation
- experiment tracking
- feature engineering beyond first-pass features

---

## Canonical grain

All downstream data MUST use:

```
(ticker, timeframe, ts)
```

Applies to:

- `price_bar_features`
- `price_bar_labels`
- `DatasetRow`

No alternate grain is allowed in first pass.

---

## Table alignment rule

All downstream rows MUST align to an existing `price_bars` row.

No downstream row may exist without a matching canonical bar.

---

## First-pass tables

The following tables must exist:

- `price_bar_features`
- `price_bar_labels`

Dataset rows are **not persisted** in first pass.

---

## Batch ID policy

Each downstream layer uses its own batch ID:

- `feature_batch_id`
- `label_batch_id`

Do NOT reuse `import_batch_id`.

---

## Run tracking policy

Downstream pipelines do NOT require dedicated run tables in first pass.

Returned summaries + batch IDs are sufficient.

---

## Required columns (first slice)

### Features

- `close_1d_return`
- `high_low_range`
- `close_open_delta`

### Labels

- `next_1d_return`

### Dataset

- identifiers
- OHLCV
- first-pass features
- first-pass label

---

## Nullability rules

Allowed nulls:

- feature warmup (`close_1d_return` first row)
- label tail (`next_1d_return` last row)

Disallowed nulls:

- identifiers
- OHLCV values

---

## Rerun policy

All downstream pipelines must be:

- deterministic
- duplicate-safe

Duplicate behavior:

- skip
- count
- do not overwrite

---

## Row fate rules

Every downstream row must result in exactly one of:

- inserted
- duplicate (skipped)
- rejected (invalid structure only)

System failure is separate from row rejection.

---

## Summary requirements

Every downstream runner must report:

- rows_selected
- rows_derived
- rows_valid
- rows_invalid
- rows_inserted
- rows_duplicates_skipped
- batch_id

---

## Core invariants

For completed runs:

```text
rows_selected >= rows_derived
rows_derived >= rows_valid
rows_valid = rows_inserted + rows_duplicates_skipped
rows_invalid >= 0
```

---

## Build order (locked)

First downstream vertical slice must follow:

1. features schema
2. feature model
3. feature pipeline stages
4. feature runner
5. feature tests

Then:

6. labels schema
7. label model
8. label pipeline stages
9. label runner
10. label tests

Then:

11. dataset models
12. dataset pipeline
13. dataset runner
14. dataset tests

---

## Success criteria

The downstream system is considered real when:

- features are computed from `price_bars`
- labels are computed from `price_bars`
- dataset rows are assembled from all three tables
- dataset splits are deterministic and leakage-safe
- dataset is exported as CSV

---

## Summary

This document answers:

> "What are we building next, and what rules must not be violated while doing it?"

Everything downstream must conform to this contract.