from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PriceBarFeature:
    ticker: str
    timeframe: str
    ts: str
    close_1d_return: float | None
    high_low_range: float
    close_open_delta: float
    feature_batch_id: str
