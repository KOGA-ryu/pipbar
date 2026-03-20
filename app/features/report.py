from __future__ import annotations


def build_feature_run_summary(
    rows_selected: int,
    rows_derived: int,
    rows_valid: int,
    rows_invalid: int,
    rows_inserted: int,
    rows_duplicates_skipped: int,
    feature_batch_id: str,
) -> dict[str, int | str]:
    return {
        "rows_selected": rows_selected,
        "rows_derived": rows_derived,
        "rows_valid": rows_valid,
        "rows_invalid": rows_invalid,
        "rows_inserted": rows_inserted,
        "rows_duplicates_skipped": rows_duplicates_skipped,
        "feature_batch_id": feature_batch_id,
    }


def print_feature_run_summary(summary: dict[str, int | str]) -> None:
    print(summary)
