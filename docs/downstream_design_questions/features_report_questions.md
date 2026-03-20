# features/report.py Contract

## Purpose

`report.py` builds the **feature run summary**.

It formats counts produced by the feature pipeline into a stable, explicit structure.

This module is **summary-only**:
- no feature computation
- no database access
- no orchestration

---

## Summary inputs

All values are passed in from upstream stages.

`report.py` must not recompute or query anything.

Inputs must include:

- `rows_selected`
- `rows_derived`
- `rows_valid`
- `rows_invalid`
- `rows_inserted`
- `rows_duplicates_skipped`
- `feature_batch_id`

---

## Output format

Primary output is a **machine-friendly dict**:

```text
FeatureRunSummary:
  rows_selected: int
  rows_derived: int
  rows_valid: int
  rows_invalid: int
  rows_inserted: int
  rows_duplicates_skipped: int
  feature_batch_id: str
```

---

## Optional human-readable output

Human-readable printing may be supported, but must be:

- separate from summary construction
- optional
- not required for correctness

---

## Naming rules

Summary field names must:

- match ingestion naming patterns where possible
- remain stable
- be explicit (no abbreviations)

---

## Invariants (completed run)

The following must hold:

```text
rows_selected >= rows_derived
rows_derived >= rows_valid
rows_valid = rows_inserted + rows_duplicates_skipped
rows_invalid >= 0
```

`report.py` does not enforce invariants, but reflects values that must already satisfy them.

---

## Zero-row behavior

A zero-row run is valid.

The summary must:

- include all keys
- use zero values where appropriate
- not raise errors

---

## Responsibility boundaries

`report.py`:
- builds summary object
- optionally formats human-readable output

It does **not**:
- compute features
- validate rows
- query database
- manage pipeline flow

---

## Determinism

Given identical inputs, output must be identical.

---

## Summary

This module answers:

> "What happened during this feature generation run?"

Nothing more.
