from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LabelRow:
    ticker: str
    timeframe: str
    ts: str
    next_1d_return: float | None
    label_batch_id: str
