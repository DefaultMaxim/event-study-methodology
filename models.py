import numpy as np
import pandas as pd
import statsmodels.api as sm

"""

    Model contains utils to run modeling of returns
    there are parameters:
    estimation_size: int (default 120),
    event_window_size: int (default 10),
    
"""


def capm_model(market,
               stock,
               start: int,
               horizon: int,
               estimation_size: int = 120,
               event_window_size: int = 10,
               full_ar: bool = False):

    """

    :param market: market returns
    :param stock: stock returns
    :param start: start idx
    :param horizon: event_idx - event_window // 2
    :param estimation_size: size of lin reg data 120 by default
    :param event_window_size: event window size (-5, event_day, 5) by default
    :param full_ar: bool: True or False: returns ar on whole estimation period for some tests
    :return: ar

    """

    pass


def lin_reg(market,
            stock,
            start: int,
            horizon: int,
            estimation_size: int = 120,
            event_window_size: int = 10,
            full_ar: bool = False):
    """
    Linear regression model
    :param market: market returns
    :param stock: stock returns
    :param start: start idx
    :param horizon: event_idx - event_window // 2
    :param estimation_size: size of lin reg data 120 by default
    :param event_window_size: event window size (-5, event_day, 5) by default
    :param full_ar: bool: True or False: returns ar on whole estimation period for some tests
    :return: ar:abnormal returns,
    df:degrees of freedom,
    var:variance ar,
    std: Mean squared error of the residuals,
    model: model
    """
    X = sm.add_constant(market)

    Y = stock

    model = sm.OLS(Y[start:horizon], X[start:horizon]).fit()

    res = np.array(Y) - (model.predict(X) + np.random.normal(0, 1)/100)

    df = estimation_size - 1

    variance = np.var(res[start:horizon])

    std = np.sqrt(model.mse_resid)

    if full_ar:

        return res, df, variance, std, model

    return res[horizon:horizon + event_window_size], df, variance, std, model


def compute_portfolio_params(portfolio):
    """
    Calculates parameters of portfolio
    $$
    \alpha = J_n^T \cdot \mathbb{V} \cdot J_n^T
    \beta = J_n^T \cdot \mathbb{V}^{-1} \cdot r
    \gamma = r^T \cdot \mathbb{V}^{-1} \cdot r
    \delta = \alpha \gamma - \beta^{2}
    J_n^T - matrix ones (n x n)
    \mathbb{V} - returns covariance matrix
    $$
    :param portfolio: close price portfolio wo market price
    :return: alpha, beta, gamma, delta
    """

    portfolio = portfolio.dropna(axis=1)

    returns = portfolio.pct_change().fillna(0)
    mean_returns = returns.mean()

    r = mean_returns
    v = returns.cov()

    v_shape = np.shape(v)
    r_shape = np.shape(r)

    ones = np.ones(r_shape)

    v_inv = np.linalg.inv(v)

    ones = np.ones(r_shape)

    tmp = np.dot(ones.T, v_inv)
    alpha = np.dot(tmp, ones)

    tmp = np.dot(ones.T, v_inv)
    beta = np.dot(tmp, r)

    tmp = np.dot(r, v_inv)
    gamma = np.dot(tmp, r)

    delta = alpha * gamma - beta ** 2

    return alpha, beta, gamma, delta


def min_risk_portfolio_model(portfolio, keep_shorts: bool = True):
    """
    Compute Markowitz portfolio model
    stay keep_shorts = True, false part is not ready
    :param portfolio: Portfolio pct change
    :param keep_shorts: If True then result portfolio may contains short sales
    :return: portfolio, risk, returns
    """

    portfolio = portfolio.dropna(axis=1)

    alpha, beta, gamma, delta = compute_portfolio_params(portfolio)

    returns = portfolio.pct_change().fillna(0)
    mean_returns = returns.mean()

    r = mean_returns
    v = returns.cov()

    v_shape = np.shape(v)
    r_shape = np.shape(r)

    ones = np.ones(r_shape)

    v_inv = np.linalg.inv(v)

    if keep_shorts:

        x_tmp = 1 / alpha * v_inv
        x = np.dot(x_tmp, ones)
        tmp = np.dot(x.T, v)

        returns = beta/alpha

        risk = 1/np.sqrt(alpha)

        return x, returns, risk, portfolio.columns


def max_sharpe_rate_portfolio(portfolio, keep_shorts: bool = True):

    """
    Calculates portfolio which maximize sharpe ratio = r/sigma
    stay keep_shorts = True, false part is not ready
    :param portfolio: close price portfolio wo market price
    :param keep_shorts: If true then portfolio may contains short sales
    :return: portfolio, risk, returns
    """

    portfolio = portfolio.dropna(axis=1)

    if keep_shorts:

        alpha, beta, gamma, delta = compute_portfolio_params(portfolio)

        returns = portfolio.pct_change().fillna(0)
        mean_returns = returns.mean()

        r = mean_returns
        v = returns.cov()

        v_shape = np.shape(v)
        r_shape = np.shape(r)

        ones = np.ones(r_shape)

        v_inv = np.linalg.inv(v)

        x = 1/beta * v_inv @ r

        returns = gamma/beta

        risk = np.sqrt(gamma)/beta

        return x, returns, risk, portfolio.columns, '213321'


def constant_mean(returns,
                  estimation_size: int = 120,
                  event_window_size: int = 10,
                  full_ar: bool = False):
    """
    Model which calculate abnormal returns by $R - \mathbb{E}(R_{t}$
    :param returns: stock returns wo market returns
    :param estimation_size: estimation_size
    :param event_window_size: event_window_size
    :param full_ar: bool: True or False: returns ar on whole estimation period for some tests
    :return: AR, df, var, mean
    """
    mean = np.mean(returns[:estimation_size])

    res = np.array(returns) - mean

    df = estimation_size - 1

    variance = np.var(res)

    if full_ar:

        return res, df, variance, mean

    return res[-event_window_size:], df, variance, mean
