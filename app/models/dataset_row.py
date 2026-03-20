from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DatasetRow:
    ticker: str
    timeframe: str
    ts: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    close_1d_return: float | None
    high_low_range: float | None
    close_open_delta: float | None
    next_1d_return: float | None
