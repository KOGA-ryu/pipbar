from __future__ import annotations

from app.models.candidate_row import CandidateRow
from app.models.price_bar import PriceBar


def normalize_rows(
    raw_rows: list[dict[str, str]],
    ticker: str,
    import_batch_id: str,
    timeframe: str = "1d",
    source: str = "massive_csv",
) -> list[CandidateRow]:
    # Future optimization note:
    # if profiling shows bulk row conversion is hot on large imports,
    # this stage can be replaced with a compiled/native implementation.
    # do not optimize before profiling.
    normalized_rows: list[CandidateRow] = []

    for raw_row in raw_rows:
        try:
            record = PriceBar(
                ticker=ticker.upper(),
                timeframe=timeframe,
                ts=_normalize_date(raw_row["date"]),
                open=float(raw_row["open"]),
                high=float(raw_row["high"]),
                low=float(raw_row["low"]),
                close=float(raw_row["close"]),
                volume=int(raw_row["volume"]),
                source=source,
                import_batch_id=import_batch_id,
            )
            normalized_rows.append(
                CandidateRow(
                    raw_row=raw_row,
                    record=record,
                    issues=[],
                )
            )
        except (KeyError, TypeError, ValueError) as error:
            normalized_rows.append(
                CandidateRow(
                    raw_row=raw_row,
                    record=None,
                    issues=[str(error)],
                )
            )

    return normalized_rows


def _normalize_date(raw_date: str) -> str:
    return f"{raw_date}T00:00:00Z"
