# labels/derive.py Questions

- What exact first-pass labels belong here?
- Should the first label be `next_bar_return`, `next_day_up_down`, or both?
- What timestamp does a label row attach to: the source bar being labeled or the future outcome bar?
- How is lookahead defined exactly?
- How many future bars are required for the first label slice?
- What happens at the end of a series where the future bar does not exist?
- Are unlabeled tail rows dropped or marked with issues?
- Should labels be computed from `price_bars` only on first pass?
- Must labels remain independent of features initially?
- What formulas should be locked exactly?
- Is label math deterministic and free of side effects by contract?
- What output container should derive produce?
- Which leakage risks must be documented before coding?

# labels/derive.py Contract

## Purpose

`derive.py` computes **supervised target labels** from trusted bar data.

It produces label rows keyed to the current bar so downstream datasets can join features and targets without ambiguity.

This module is **math-only**:
- no SQL
- no file I/O
- no orchestration
- no side effects

---

## First-pass labels (locked)

First pass includes only:

- `next_1d_return = (close_t+1 / close_t) - 1`

No classification labels in the first slice.

---

## Timestamp attachment

Each label row is attached to the **current source bar timestamp (`ts`)**.

Meaning:
- the row at `ts = t` stores the future outcome derived from bar `t+1`
- labels are keyed to the bar being labeled, not the future bar

---

## Lookahead definition

First-pass lookahead is:

- exactly 1 future bar in the same `(ticker, timeframe)` series

No multi-step lookahead yet.

---

## Input requirements

- input is ordered bars per `(ticker, timeframe)` by `ts` ascending
- labels are computed from `price_bars` only
- labels remain independent of features in first pass

---

## End-of-series behavior

If the required future bar does not exist (tail row):

- emit row with `next_1d_return = None`
- do not drop row
- do not raise

---

## Output type

Returns:

```text
list[LabelRow]
```

Each label row includes:
- `ticker`
- `timeframe`
- `ts`
- `next_1d_return`

---

## Determinism

Label derivation MUST be:

- deterministic
- pure
- repeatable

Same input → same output.

---

## Leakage rules

The following are hard rules:

- label rows are keyed to current bar timestamp
- future outcome values must never change the key to future `ts`
- no feature values are used to derive labels in first pass
- no rows may use information beyond the defined 1-bar lookahead

---

## Responsibility boundaries

`derive.py`:
- computes target labels from ordered bars

It does **not**:
- query SQL
- derive features
- validate rows
- persist data
- split datasets
- train models

---

## Minimal function signature

```python
compute_labels(bars: list[PriceBar]) -> list[LabelRow]
```

No extra parameters in first pass.

---

## Explicitly out of scope (first slice)

- next-day up/down classification labels
- multi-bar forward returns
- volatility targets
- regime labels
- feature-dependent labels

---

## Summary

This module answers:

> "Given ordered bars, what future outcome should be attached to each current bar as supervised target truth?"

Nothing more.