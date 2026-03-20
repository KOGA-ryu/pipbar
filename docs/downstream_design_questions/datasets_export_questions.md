# datasets/export.py Questions

- What is the first export target: CSV only?
- What exact output artifacts should export produce on first pass?
- Should splits export as separate files or one file with a split column?
- What naming convention should output files follow?
- Does export own directory creation?
- Should export return file paths, counts, or both?
- What belongs in file headers?
- Must export preserve deterministic column ordering?
- What output formats are explicitly deferred?

# datasets/export.py Contract

## Purpose

`export.py` is responsible for writing assembled dataset rows to disk.

It converts in-memory `DatasetRow` objects into a stable, deterministic file format for downstream research.

This module is **output-only**:
- no data derivation
- no dataset assembly
- no splitting logic

---

## First-pass export format

First pass supports:

- CSV only

Other formats (parquet, feather, database export) are explicitly deferred.

---

## Output artifacts

On first pass, export produces:

- one file per split

Expected files:

- `train.csv`
- `validation.csv`
- `test.csv`

Files are written to the provided `output_path`.

---

## Split handling

Splits are exported as **separate files**, not as a single file with a split column.

Reason:
- simpler downstream usage
- avoids accidental mixing of training and evaluation data

---

## File naming convention

First-pass naming is fixed:

```text
train.csv
validation.csv
test.csv
```

No dynamic naming yet.

---

## Directory ownership

`export.py` owns directory creation.

Requirements:
- create `output_path` if it does not exist
- do not delete existing contents
- fail only on true filesystem errors

---

## Return value

Export must return a summary containing:

- `files_written: int`
- `file_paths: list[str]`
- `rows_per_file: dict[str, int]`

This feeds directly into `dataset_runner` summary.

---

## File contents

Each CSV must include:

- header row
- all dataset columns in fixed order
- no index column

---

## Column ordering

Column ordering must be:

- deterministic
- consistent across runs
- defined by `assemble.py`

`export.py` must not reorder columns.

---

## Empty dataset behavior

If a split has zero rows:

- file is still created
- file contains header only
- counts reflect zero rows

This is a successful outcome, not a failure.

---

## Responsibility boundaries

`export.py`:
- writes dataset rows to disk
- enforces file format
- returns export summary

It does **not**:
- assemble rows
- compute splits
- query database
- train models
- validate dataset logic

---

## Determinism

Given identical input rows and output path, export must produce identical file contents.

---

## Summary

This module answers:

> "How do we reliably write dataset rows to disk in a reproducible format?"

Nothing more.