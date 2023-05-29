import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from constants import MAX_HALF_LIFE, WINDOW

# Calculate Half Life
# https://www.pythonforfinance.net/2016/05/09/python-backtesting-mean-reversion-part-2/


def calculate_half_life(spread):
    """
    Calculates the half-life of the provided time series `spread` using an OLS model.

    Parameters:
    spread (Series, array-like): The time series for which the half-life is to be computed.

    Returns:
    halflife (float): The computed half-life value.
    """
    df_spread = pd.DataFrame(spread, columns=["spread"])
    spread_lag = df_spread.spread.shift(1)
    spread_lag.iloc[0] = spread_lag.iloc[1]
    spread_ret = df_spread.spread - spread_lag
    spread_ret.iloc[0] = spread_ret.iloc[1]
    spread_lag2 = sm.add_constant(spread_lag)
    model = sm.OLS(spread_ret, spread_lag2)
    res = model.fit()
    halflife = round(-np.log(2) / res.params[1], 0)
    return halflife

# Calculate ZScore


def calculate_zscore(spread):
    """
    Calculates the Z-score for the time series `spread`.

    Parameters:
    spread (Series, array-like): The time series for which the Z-score is to be computed.

    Returns:
    zscore (Series): The series of computed Z-scores.
    """
    spread_series = pd.Series(spread)
    mean = spread_series.rolling(center=False, window=WINDOW).mean()
    std = spread_series.rolling(center=False, window=WINDOW).std()
    x = spread_series.rolling(center=False, window=1).mean()
    zscore = (x - mean) / std
    return zscore

# Calculate cointegration


def calculate_cointegration(series_1, series_2):
    """
    Tests for cointegration between two time series.

    Parameters:
    series_1, series_2 (Series, array-like): The time series to be tested for cointegration.

    Returns:
    coint_flag (int): Cointegration flag. Equals 1 if the series are cointegrated, 0 otherwise.
    hedge_ratio (float): The slope coefficient from the OLS regression model.
    half_life (float): The half-life computed for the spread between the two series.
    """
    series_1 = np.array(series_1).astype(np.float)
    series_2 = np.array(series_2).astype(np.float)
    coint_flag = 0
    coint_res = coint(series_1, series_2)
    coint_t = coint_res[0]
    p_value = coint_res[1]
    critical_value = coint_res[2][1]
    model = sm.OLS(series_1, series_2).fit()
    hedge_ratio = model.params[0]
    spread = series_1 - (hedge_ratio * series_2)
    half_life = calculate_half_life(spread)
    t_check = coint_t < critical_value
    coint_flag = 1 if p_value < 0.05 and t_check else 0
    return coint_flag, hedge_ratio, half_life
