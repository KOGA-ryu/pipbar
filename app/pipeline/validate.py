from __future__ import annotations

from app.models.candidate_row import CandidateRow
from app.models.price_bar import PriceBar


def validate_records(
    records: list[CandidateRow],
) -> tuple[list[PriceBar], list[dict[str, object]]]:
    # Future optimization note:
    # if profiling shows record-by-record validation is hot on very large imports,
    # this stage can move to a vectorized or compiled implementation.
    # do not optimize before profiling.
    valid_records: list[PriceBar] = []
    invalid_records: list[dict[str, object]] = []

    for candidate in records:
        if candidate.record is None:
            invalid_records.append(
                {
                    "raw_row": candidate.raw_row,
                    "record": None,
                    "issues": candidate.issues,
                }
            )
            continue

        issues = _validate_record(candidate.record)
        if issues:
            invalid_records.append(
                {
                    "raw_row": candidate.raw_row,
                    "record": candidate.record,
                    "issues": issues,
                }
            )
        else:
            valid_records.append(candidate.record)

    return valid_records, invalid_records


def _validate_record(record: PriceBar) -> list[str]:
    issues: list[str] = []

    if not record.ticker:
        issues.append("ticker is required")
    if not record.timeframe:
        issues.append("timeframe is required")
    if not record.ts:
        issues.append("ts is required")
    if not record.source:
        issues.append("source is required")
    if not record.import_batch_id:
        issues.append("import_batch_id is required")

    numeric_fields = {
        "open": record.open,
        "high": record.high,
        "low": record.low,
        "close": record.close,
        "volume": record.volume,
    }
    numeric_field_errors = False
    for field_name, value in numeric_fields.items():
        if value is None:
            issues.append(f"{field_name} is required")
            numeric_field_errors = True
        elif not _is_valid_number(value):
            issues.append(f"{field_name} must be numeric")
            numeric_field_errors = True
        elif value < 0:
            issues.append(f"{field_name} must be >= 0")
            numeric_field_errors = True

    if not numeric_field_errors:
        if record.high < record.low:
            issues.append("high must be >= low")
        if not (record.low <= record.open <= record.high):
            issues.append("open must be between low and high")
        if not (record.low <= record.close <= record.high):
            issues.append("close must be between low and high")

    return issues


def _is_valid_number(value: object) -> bool:
    if isinstance(value, bool):
        return False
    return isinstance(value, (int, float))
