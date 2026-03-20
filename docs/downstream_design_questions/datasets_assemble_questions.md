# datasets/assemble.py Questions

- What is the exact first-pass assembled row shape?
- Which identifier fields must every dataset row include?
- Which feature columns are included initially?
- Which label columns are included initially?
- How should missing joins be handled?
- Should assembly require inner joins only on first pass?
- Does this file own column naming conventions for exported datasets?
- Must assembled rows be fully deterministic and side-effect free?
- Should this module output `DatasetRow` dataclasses immediately?
- What assumptions about time alignment must be written down before coding?

# datasets/assemble.py Contract

## Purpose

`assemble.py` constructs **research-ready dataset rows** by combining:

- canonical bars (`price_bars`)
- derived features (`price_bar_features`)
- labels (`price_bar_labels`)

It produces a **single, aligned row shape** for downstream research or ML use.

This module is **pure transformation**:
- no SQL reads
- no writes
- no side effects

---

## First-pass assembled row shape

Each dataset row represents:

```
one (ticker, timeframe, ts)
```

Output shape:

```
DatasetRow:
  ticker: str
  timeframe: str
  ts: str

  # features
  close_1d_return: float | None
  high_low_range: float | None
  close_open_delta: float | None

  # labels
  next_1d_return: float | None
```

All rows must include identifiers + selected features + selected labels.

---

## Required identifier fields

Every dataset row MUST include:

- `ticker`
- `timeframe`
- `ts`

These define the row grain and are non-null.

---

## Initial feature columns

First pass includes only:

- `close_1d_return`
- `high_low_range`
- `close_open_delta`

No rolling features, indicators, or derived windows yet.

---

## Initial label columns

First pass includes only:

- `next_1d_return`

No classification labels yet.

---

## Join policy

First pass uses **inner join semantics**:

A row is included only if:
- bar exists
- feature row exists
- label row exists

Reason:
- ensures complete rows
- avoids silent NaNs
- simplifies early research

---

## Missing join handling

- Missing feature OR label → row is excluded
- No partial rows allowed in first pass

Future versions may relax this, but not now.

---

## Column naming ownership

`assemble.py` owns the **final dataset column names**.

Rules:
- stable
- explicit
- no renaming downstream

This prevents naming drift across research code.

---

## Determinism

This module MUST be:

- deterministic
- side-effect free
- order-preserving (sorted by ts)

Same input → same output always.

---

## Output type

This module outputs:

```
list[DatasetRow]
```

No raw dicts.

---

## Time alignment assumptions

Must hold before assembly:

- features are computed at same `(ticker, timeframe, ts)`
- labels are aligned to the same timestamp (not future timestamp keys)
- no lookahead leakage
- data is pre-sorted or explicitly sorted here

If alignment is violated, rows must be dropped or raise errors.

---

## Responsibility boundaries

assemble.py:
- combines inputs into dataset rows

Does NOT:
- compute features
- compute labels
- query database
- split datasets
- export files
- train models

---

## Summary

This module answers:

> "Given trusted bars, features, and labels, what is the exact row we train on?"

Nothing more.