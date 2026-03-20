from __future__ import annotations


def build_run_summary(
    files_discovered: int,
    rows_parsed: int,
    rows_valid: int,
    rows_invalid: int,
    rows_inserted: int,
) -> dict[str, int]:
    return {
        "files_discovered": files_discovered,
        "rows_parsed": rows_parsed,
        "rows_valid": rows_valid,
        "rows_invalid": rows_invalid,
        "rows_inserted": rows_inserted,
    }


def print_run_summary(summary: dict[str, int]) -> None:
    print(summary)
