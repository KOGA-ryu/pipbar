from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PriceBar:
    ticker: str
    timeframe: str
    ts: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    source: str
    import_batch_id: str
