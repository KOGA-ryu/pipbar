# models/dataset_row.py Questions

- What exact fields must `DatasetRow` contain on first pass?
- Should it include raw bar fields, selected features, and selected labels together?
- Which identifier fields are mandatory?
- Should a split designation live in the row model or remain outside until export?
- Does this model need to support export helpers, or should it stay a plain typed container?
- How wide is too wide for the first-pass row contract?
- Which fields are guaranteed present versus optional?

# models/dataset_row.py Contract

## Purpose

`dataset_row.py` defines the **typed assembled row shape** used by the dataset pipeline.

It is the in-memory representation of one research-ready row after bars, features, and labels have been aligned.

This model is a **plain typed container**:
- no SQL
- no export helpers
- no orchestration logic

---

## First-pass row grain

Each `DatasetRow` represents exactly:

```text
one (ticker, timeframe, ts)
```

This matches the grain of:
- `price_bars`
- `price_bar_features`
- `price_bar_labels`

---

## First-pass required fields

Every `DatasetRow` MUST include:

- `ticker: str`
- `timeframe: str`
- `ts: str`

These identifiers are mandatory and non-null.

---

## First-pass bar fields

Include these canonical bar fields:

- `open: float`
- `high: float`
- `low: float`
- `close: float`
- `volume: int`

These are required.

---

## First-pass feature fields

Include these feature fields:

- `close_1d_return: float | None`
- `high_low_range: float | None`
- `close_open_delta: float | None`

These may be `None` only where upstream feature contract allows it.

---

## First-pass label fields

Include these label fields:

- `next_1d_return: float | None`

This may be `None` only where upstream label contract allows it.

---

## Split designation

Split designation does **not** belong in `DatasetRow` on first pass.

Reason:
- split membership is pipeline context
- row identity should remain independent of train/validation/test usage

Split assignment belongs in `split.py` and export flow, not the base row model.

---

## Optional vs guaranteed fields

Guaranteed present:
- identifiers
- canonical bar fields

Optional by contract:
- warmup-sensitive feature fields
- tail-sensitive label fields

Optionality must come from upstream contracts, not ad hoc usage.

---

## Width policy

First pass keeps `DatasetRow` intentionally narrow:

- identifiers
- core OHLCV bar fields
- first-pass features
- first-pass label

Do not add:
- raw CSV fields
- duplicate feature aliases
- split flags
- export metadata
- model predictions

---

## Output role

`DatasetRow` is the canonical in-memory row used by:
- `assemble.py`
- `split.py`
- `export.py`

It should be stable enough that downstream code does not invent alternative row shapes.

---

## Responsibility boundaries

`dataset_row.py`:
- defines row shape only

It does **not**:
- export itself
- derive fields
- validate itself
- know about database persistence
- know about train/test usage

---

## Determinism

Given the same assembled inputs, the same `DatasetRow` values must be produced.

---

## Summary

This model answers:

> "What is the exact typed row shape that downstream dataset assembly produces for research use?"

Nothing more.