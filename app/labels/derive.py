from __future__ import annotations

from app.models.label_row import LabelRow
from app.models.price_bar import PriceBar


def compute_labels(bars: list[PriceBar], label_batch_id: str) -> list[LabelRow]:
    labels: list[LabelRow] = []

    for index, bar in enumerate(bars):
        next_close = bars[index + 1].close if index + 1 < len(bars) else None
        next_1d_return = None
        if next_close is not None and bar.close != 0:
            next_1d_return = (next_close / bar.close) - 1

        labels.append(
            LabelRow(
                ticker=bar.ticker,
                timeframe=bar.timeframe,
                ts=bar.ts,
                next_1d_return=next_1d_return,
                label_batch_id=label_batch_id,
            )
        )

    return labels
