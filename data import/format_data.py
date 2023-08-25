import pandas as pd
import numpy as np


def quotation_to_float(quot):
    return quot.units + quot.nano / 1_000_000_000


def data_to_floats(share):
    """переводит тип данных тинькова в нормальный флоат"""

    CLOSE = []

    for i in range(len(share)):
        CLOSE.append(quotation_to_float(share[i].close))

    CLOSE = np.array(CLOSE)

    RAW_CHANGE = [((quotation_to_float(share[i].close) - quotation_to_float(share[i - 1].close)) /
                  quotation_to_float(share[i - 1].close) +
                  (quotation_to_float(share[i].close) - quotation_to_float(share[i - 1].close))
                  / quotation_to_float(share[i].close)) / 2
                  for i in range(1, len(share))]
    RAW_CHANGE.insert(0, 0)

    CHANGE = []
    CHANGE.append(0)

    for i in range(1, len(share)):
        CHANGE.append(RAW_CHANGE[i])

    RAW_LOG_CHANGE = [(np.log(quotation_to_float(share[i].close) / quotation_to_float(share[i - 1].close)))
                      for i in range(1, len(share))]

    RAW_LOG_CHANGE.insert(0, 0)

    LOG_CHANGE = [0]

    for i in range(1, len(share)):
        LOG_CHANGE.append(RAW_LOG_CHANGE[i])

    VOLUME, TIME = [], []

    for i in range(len(share)):
        VOLUME.append(share[i].volume)

        TIME.append(share[i].time)

    TIME = pd.to_datetime(TIME)
    VOLUME = np.array(VOLUME)

    return [TIME, CLOSE, VOLUME, CHANGE, LOG_CHANGE]


def create_df(share):
    """"создает датасет для выбранной акции"""
    TIME, CLOSE, VOLUME, CHANGE, LOG_CHANGE = data_to_floats(share)

    if len(TIME) != 0:

        DATA = {'time': TIME, 'close': CLOSE, 'volume': VOLUME, 'change': CHANGE, 'log_change': LOG_CHANGE}

        df = pd.DataFrame(data=DATA)
        df.index = df.time
        df.drop(columns='time', inplace=True)

        return df
