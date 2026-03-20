# labels/load.py Contract

## Purpose

`load.py` persists **validated label rows** into the label table.

It is responsible for writing accepted label data and handling duplicates.

This module is **write-only**:
- no label derivation
- no validation logic
- no orchestration

---

## Target table

Accepted label rows are inserted into:

```
price_bar_labels
```

---

## Row identity

Label row identity is:

```
(ticker, timeframe, ts)
```

This must match the grain of `price_bars`.

---

## Duplicate policy (first pass)

- duplicates are **skipped**, not overwritten
- duplicates are **counted**
- duplicates are **not treated as invalid data**

---

## Input contract

This module accepts only:

```
list[LabelRow]
```

All rows must already be validated.

---

## Output summary

Loader must return:

- `rows_inserted`
- `rows_duplicates_skipped`

Counts must be explicit and nonnegative.

---

## Insert strategy

First pass uses:

- simple loop with individual inserts

Batch insert optimization is deferred.

---

## Transaction ownership

- `load.py` does NOT own transactions
- commit is controlled by the runner

---

## Error handling

Loader must distinguish:

Duplicate errors:
- unique constraint violation on `(ticker, timeframe, ts)`
- counted as duplicates
- do not fail the run

Real failures:
- DB connection failure
- schema mismatch
- unexpected constraint violation

Real failures must:
- raise exception
- not be swallowed

---

## Column order

Insert SQL must follow exact schema order:

- `ticker`
- `timeframe`
- `ts`
- label columns
- `label_batch_id`
- `created_at`

Order must be explicit and stable.

---

## Determinism

Given identical input rows, the loader must produce identical DB state.

---

## Responsibility boundaries

`load.py`:
- inserts validated label rows
- handles duplicate detection
- returns insertion counts

It does **not**:
- derive labels
- validate rows
- query source data
- manage transactions
- report results

---

## Summary

This module answers:

> "How do we persist validated label rows into the label table correctly?"

Nothing more.
