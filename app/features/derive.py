from __future__ import annotations

from app.models.price_bar import PriceBar
from app.models.price_bar_feature import PriceBarFeature


def compute_features(bars: list[PriceBar], feature_batch_id: str) -> list[PriceBarFeature]:
    features: list[PriceBarFeature] = []

    for index, bar in enumerate(bars):
        previous_close = bars[index - 1].close if index > 0 else None
        close_1d_return = None
        if previous_close not in (None, 0):
            close_1d_return = (bar.close / previous_close) - 1

        features.append(
            PriceBarFeature(
                ticker=bar.ticker,
                timeframe=bar.timeframe,
                ts=bar.ts,
                close_1d_return=close_1d_return,
                high_low_range=bar.high - bar.low,
                close_open_delta=bar.close - bar.open,
                feature_batch_id=feature_batch_id,
            )
        )

    return features
