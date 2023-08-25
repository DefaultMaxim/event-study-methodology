from get_data import tink_get_data
from format_data import create_df
from get_ticker_by_figi import figi_to_ticker
import pandas as pd


def prepare_data(token, fig_file):
    """ Формирует несколько основных датафреймов по заданным инструментам,
        возвращает closed price, change price, log(change price) ~ Винеровский"""

    shares_list, figis = tink_get_data(token=token,
                                       fig_file=fig_file)

    for i in range(len(shares_list)):

        shares_list[i] = create_df(shares_list[i])

    tickers_list = []

    col_idx = 0

    for i in range(len(shares_list)):

        if shares_list[i] is not None:

            tickers_list.append(figi_to_ticker(figis[i]))

            col_idx = i

            shares_list[i]['ticker'] = figi_to_ticker(figis[i])

    # CLOSE PORTFOLIO

    close_portfolio = pd.DataFrame(data=shares_list[0].close.values, index=shares_list[0].index)

    for i in range(1, len(shares_list)):
        close_portfolio = close_portfolio.join(pd.DataFrame(data=shares_list[i].close.values,
                                                            index=shares_list[i].index),
                                               lsuffix='_left', rsuffix='_right')

    columns = [shares_list[i].ticker[0] for i in range(len(shares_list))]

    close_portfolio.fillna(method='ffill', inplace=True)

    close_portfolio.columns = columns

    # CHANGE PORTFOLIO

    change_portfolio = pd.DataFrame(data=shares_list[0].change.values, index=shares_list[0].index)

    for i in range(1, len(shares_list)):

        change_portfolio = change_portfolio.join(pd.DataFrame(data=shares_list[i].change.values,
                                                              index=shares_list[i].index),
                                                 lsuffix='_left', rsuffix='_right')

    change_portfolio.fillna(0, inplace=True)

    change_portfolio.columns = columns

    # LOG_CHANGE PORTFOLIO

    log_change_portfolio = pd.DataFrame(data=shares_list[0].log_change.values, index=shares_list[0].index)

    for i in range(1, len(shares_list)):

        log_change_portfolio = log_change_portfolio.join(pd.DataFrame(data=shares_list[i].log_change.values,
                                                                      index=shares_list[i].index),
                                                         lsuffix='_left', rsuffix='_right')

    log_change_portfolio.fillna(0, inplace=True)

    log_change_portfolio.columns = columns

    return close_portfolio, change_portfolio, log_change_portfolio, shares_list
