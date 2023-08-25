import pandas as pd
import numpy as np


def quotation_to_float(quot):
    return quot.units + quot.nano / 1_000_000_000


def create_df(share):
    """"создает датасет для выбранной акции"""
    TIME, CLOSE, VOLUME, CHANGE, LOG_CHANGE = data_to_floats(share)

    if len(TIME) != 0:

        DATA = {'time': TIME, 'close': CLOSE, 'volume': VOLUME, 'change': CHANGE, 'log_change': LOG_CHANGE}

        df = pd.DataFrame(data=DATA)
        df.index = df.time
        df.drop(columns='time', inplace=True)

        return df