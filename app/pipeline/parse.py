from __future__ import annotations

import csv
from pathlib import Path


def parse_csv_file(file_path: str) -> list[dict[str, str]]:
    # Future optimization note:
    # if profiling shows CSV parsing is a bottleneck on large imports,
    # this stage is a candidate for a C++ extension or native parser.
    # do not optimize before profiling.
    with Path(file_path).open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)
