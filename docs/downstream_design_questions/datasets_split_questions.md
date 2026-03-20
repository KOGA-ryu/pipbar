# datasets/split.py Questions

- What is the first split policy: train/test only, or train/validation/test?
- Must splits be strictly time-ordered?
- What date boundaries or percentage rules define each split?
- Should split logic operate on sorted dataset rows only?
- How are tiny datasets handled?
- What invariants must hold across splits?
- Are overlapping splits ever allowed?
- Should this file return named collections, dicts, or a dataclass?
- What leakage-prevention guarantees belong here?

# datasets/split.py Contract

## Purpose

`split.py` partitions assembled dataset rows into research splits.

It takes fully assembled `DatasetRow` objects and divides them into:
- train
- validation
- test

This module is **split-only**:
- no assembly
- no export
- no model work

---

## First-pass split policy

First pass uses:

- `train / validation / test`

Not train/test only.

---

## Ordering requirement

Splits must operate on rows sorted by:

- `ts` ascending

If rows are not already sorted, `split.py` must sort them before applying split logic.

---

## Time-order rule

Splits must be **strictly time-ordered**.

Allowed order:

```text
train -> validation -> test
```

No future rows may appear in earlier splits.

---

## First-pass split rule

First pass uses simple percentage-based splits on sorted rows:

- train: first 70%
- validation: next 15%
- test: final 15%

Rounding policy must be deterministic and documented in code.

---

## Tiny dataset handling

Tiny datasets are valid.

Rules:
- do not fail only because one or more splits become empty
- preserve ordering
- produce honest counts

A zero-row split is allowed.

---

## Invariants

The following must always hold:

- every input row appears in exactly one split
- no row duplication across splits
- no overlap between splits
- total rows across splits equals input row count
- split order preserves original time ordering

---

## Overlap policy

Overlapping splits are **not allowed**.

This is a hard leakage-prevention rule.

---

## Return type

This module returns a typed structure:

```text
DatasetSplits:
  train: list[DatasetRow]
  validation: list[DatasetRow]
  test: list[DatasetRow]
```

Do not return loose dicts in first pass.

---

## Leakage prevention guarantees

`split.py` guarantees:

- no future rows leak backward into earlier splits
- no overlap between train/validation/test
- no reordering that breaks time structure

This module does **not** guarantee label correctness or feature correctness.
Those must already be true before splitting.

---

## Responsibility boundaries

`split.py`:
- sorts rows if needed
- partitions rows into time-ordered splits
- returns typed split collections

It does **not**:
- assemble dataset rows
- export files
- train models
- score models

---

## Determinism

Given identical input rows, `split.py` must always produce the same split boundaries and row assignments.

---

## Summary

This module answers:

> "How do we partition assembled rows into leakage-safe research splits?"

Nothing more.