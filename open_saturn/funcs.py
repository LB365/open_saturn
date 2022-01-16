from datetime import datetime

import pandas as pd
import numpy as np

from tshistory_formula.registry import (
    func,
)

def _time_arrow(
        values: np.ndarray,
        today: datetime,
        freq: str,
        offset: int) -> pd.DatetimeIndex:

    length = values.shape[0] + offset
    date = pd.date_range(start=today, periods=length, freq=freq)
    return date[offset:]


@func('concat_futures')
def concat_futures(
        *serieslist: pd.Series,
        freq: str = 'M',
        offset: int = 1) -> pd.Series:
    futures = pd.concat(serieslist, axis=1)
    today = futures.index[-1]
    # The series are updated each day, with one value
    # and one date corresponding at the current day
    history = futures.iloc[:, 0]
    current = futures.iloc[-1, 1:].values
    date = _time_arrow(current, today, freq, offset)
    forward_curve = pd.Series(
        data=current,
        index=date
    )
    return history.append(forward_curve)