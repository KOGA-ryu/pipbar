# research/baseline.py Contract

## Purpose

`baseline.py` defines the **first-pass baseline model** for research experiments.

It produces predictions given feature inputs and does not perform data loading, evaluation, or reporting.

This module is **model-only**:
- no CSV I/O
- no SQL
- no metrics
- no orchestration

---

## First-pass baseline (locked)

Baseline: **zero_return_baseline**

- predicts `0.0` return for every row

Reason:
- simple, deterministic reference
- establishes lower-bound performance

---

## Fit policy

First pass has **no fit phase**.

- model is stateless
- no training required

---

## Inputs

Baseline receives:

- `X: list[DatasetRow]` (or extracted feature matrix)

It does **not** require target values to generate predictions.

---

## Outputs

Returns predictions aligned to input order:

```text
list[float]
```

- one prediction per input row
- preserves ordering

---

## Naming

`baseline_name` must be:

```text
zero_return_baseline
```

Used in `ResearchResult`.

---

## Determinism

Baseline must be:

- deterministic
- side-effect free
- repeatable

Same input → same predictions.

---

## Responsibility boundaries

`baseline.py`:
- generates predictions only

It does **not**:
- read datasets
- compute metrics
- format reports
- know about splits
- access databases

---

## Minimal API

```python
predict(rows: list[DatasetRow]) -> list[float]
```

No extra parameters in first pass.

---

## Future compatibility (not implemented now)

Next likely baseline:

- simple linear regression

Do **not** shape current API around future models.

---

## Dependencies

First pass should be **dependency-free** (standard library only).

---

## Summary

This module answers:

> "Given dataset rows, what baseline predictions do we produce?"

Nothing more.
