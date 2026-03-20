from __future__ import annotations

from dataclasses import dataclass

from app.models.price_bar import PriceBar


@dataclass
class CandidateRow:
    raw_row: dict[str, str]
    record: PriceBar | None
    issues: list[str]
