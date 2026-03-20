from __future__ import annotations

import math

from app.models.price_bar_feature import PriceBarFeature


def validate_feature_rows(
    rows: list[PriceBarFeature],
) -> tuple[list[PriceBarFeature], list[dict[str, object]]]:
    valid_rows: list[PriceBarFeature] = []
    invalid_rows: list[dict[str, object]] = []

    for row in rows:
        issues = _validate_feature_row(row)
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


def _validate_feature_row(row: PriceBarFeature) -> list[str]:
    issues: list[str] = []

    if not row.ticker or not row.timeframe or not row.ts:
        issues.append("missing required field")

    if _is_invalid_number(row.high_low_range):
        issues.append("invalid numeric value")
    if _is_invalid_number(row.close_open_delta):
        issues.append("invalid numeric value")
    if row.close_1d_return is not None and _is_invalid_number(row.close_1d_return):
        issues.append("invalid numeric value")

    return issues


def _is_invalid_number(value: object) -> bool:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return True
    return not math.isfinite(float(value))
