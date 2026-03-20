from __future__ import annotations

import math

from app.models.label_row import LabelRow


def validate_label_rows(
    rows: list[LabelRow],
) -> tuple[list[LabelRow], list[dict[str, object]]]:
    valid_rows: list[LabelRow] = []
    invalid_rows: list[dict[str, object]] = []

    for row in rows:
        issues = _validate_label_row(row)
        if issues:
            invalid_rows.append(
                {
                    "row": row,
                    "issues": issues,
                }
            )
        else:
            valid_rows.append(row)

    return valid_rows, invalid_rows


def _validate_label_row(row: LabelRow) -> list[str]:
    issues: list[str] = []

    if not row.ticker or not row.timeframe or not row.ts:
        issues.append("missing required field")

    if row.next_1d_return is not None and _is_invalid_number(row.next_1d_return):
        issues.append("invalid numeric value")

    return issues


def _is_invalid_number(value: object) -> bool:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return True
    return not math.isfinite(float(value))
