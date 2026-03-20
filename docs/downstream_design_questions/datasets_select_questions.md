# datasets/select.py Questions

- Which trusted tables must dataset selection read on first pass?
- Does it read `price_bars`, `price_bar_features`, and `price_bar_labels` together?
- What filters must it support initially: ticker, timeframe, date range, label presence, feature presence?
- Should selection require fully joined rows, or can missing components pass through to `assemble.py`?
- What ordering contract must be guaranteed?
- Should this module return separate collections per table or a pre-keyed join input?
- How are mismatched keys across bars/features/labels represented?
- What is a normal empty result versus an error?

# datasets/select.py Contract

## Purpose

`select.py` reads **trusted tables** and prepares inputs for dataset assembly.

It gathers data from:
- `price_bars`
- `price_bar_features`
- `price_bar_labels`

This module is **read-only** and returns data needed for assembly.

---

## Data sources (first pass)

Must read from:

- `price_bars`
- `price_bar_features`
- `price_bar_labels`

No other sources.

---

## Supported filters (first pass)

- `ticker: str | None`
- `timeframe: str`
- `start_ts: str | None`
- `end_ts: str | None`

Optional behavior:
- restrict to rows where labels exist (implicitly required by inner-join policy downstream)

---

## Join responsibility

`select.py` does **not** perform final joins.

It returns **keyed collections** that `assemble.py` will join.

---

## Output shape

Return a structure keyed by `(ticker, timeframe, ts)`:

```
SelectedData:
  bars: dict[key, PriceBar]
  features: dict[key, PriceBarFeature]
  labels: dict[key, LabelRow]
```

Where `key = (ticker, timeframe, ts)`.

---

## Ordering contract

- Bars must be **sorted by ts ascending** within each `(ticker, timeframe)` group
- Features and labels do not require ordering but must align by key

---

## Missing data representation

- Missing features or labels are represented by **missing keys** in their dicts
- No placeholder rows
- No partial merging

`assemble.py` decides whether to drop or error on missing keys

---

## Empty result behavior

- Empty selection is **valid**
- Return empty dicts for all collections
- Do not raise errors for empty selections

Errors are only for:
- DB access failure
- schema mismatch

---

## Responsibility boundaries

`select.py`:
- queries trusted tables
- applies filters
- returns keyed collections

It does **not**:
- join rows
- compute features
- compute labels
- validate dataset rows
- export files

---

## Determinism

Given the same DB state and filters, output must be identical.

---

## Summary

This module answers:

> "What trusted rows are available for dataset assembly?"

Nothing more.