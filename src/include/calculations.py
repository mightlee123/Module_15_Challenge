"""
Calculations Module
-------------------------------

Financial calculations module which acts upon a Pandas DataFrame object containing information about assets. A set of 
various computations for this data is defined here.

NOTE: All functions within this module will operate under the assumption that the DataFrame instance indicates closing
        prices of assets.
"""

import numpy as np

# Weights per client risk profile.  
risk_profile_weights = {"conservative" : [0.1, 0.9, 0.0], "moderately conservative" : [0.25, 0.7, 0.05], 
                        "moderate" : [0.6, 0.3, 0.1], "moderately aggressive" : [0.75, 0.2, 0.05],
                        "aggressive" : [0.8, 0.0, 0.2]}

def calculate_daily_returns(closing_prices_df):
    """
    Calculates the daily returns on closing prices.

    :param df: Closing prices.
    :type df: Pandas DataFrame.
    """
    daily_returns_df = closing_prices_df.pct_change().dropna()
    return daily_returns_df
    

def calculate_average_annual_returns(daily_returns_df):
    """
    Calculates the annual returns on daily returns.
    Must only be ran after calculate_daily_returns() method has been called.

    :param daily_returns_df: Daily returns.
    :type daily_returns_df: Pandas DataFrame.
    """
    avg_annual_returns_df = (daily_returns_df.mean() * 252)
    return avg_annual_returns_df

def calculate_average_annual_volatility(daily_returns_df):
    """
    Calculates the annual volatility on daily returns. 
    Must only be ran after calculate_daily_returns() method has been called.

    :param daily_returns_df: Daily returns.
    :type daily_returns_df: Pandas DataFrame. 
    """
    avg_annual_volatility_df = daily_returns_df.std() * 252**(1/2)
    return avg_annual_volatility_df

def calculate_sharpe_ratio(avg_annual_returns_df, avg_annual_volatility_df):
    """
    Calculates the Sharpe Ratio of a given portfolio.
    Must only be ran after calculate_daily_returns(), calculate_average_annual_returns()
    calculate_average_annual_volatility() methods have been called. 

    :param avg_annual_returns_df: Average annual returns.
    :param avg_annual_volatility_df: Average annual volatility.
    :type avg_annual_returns_df: Pandas DataFrame.
    :type avg_annual_volatility_df: Pandas DataFrame.
    """
    avg_annual_sharpe_ratio_df = avg_annual_returns_df / avg_annual_volatility_df
    return avg_annual_sharpe_ratio_df

def calculate_portfolio_return(daily_returns_df, weight):
    """
    Calculate the portfolio return per a given weight based off of client risk profile.

    :param average_annual_returns_df: Average annual returns of asset data.
    :param weight: Portfolio weight per client risk profile.
    :type average_annual_returns_df: Pandas DataFrame.
    :type weight: float list
    """
    portfolio_return_df = daily_returns_df.mean().mul(weight).sum() * 252
    return portfolio_return_df

def calculate_portfolio_volatility(daily_returns_df, weight):
    """
    Calculate the volatility of the portfolio.
    Must only be ran after calculate_daily_returns() and risk_profile() methods have been called.
    
    :param daily_returns_df: Daily returns.
    :param risk_prof: client risk profile.
    :type daily_returns_df: Pandas DataFrame.
    :type risk_prof: string
    """
    asset_weights = np.array(weight)
    portfolio_covariance = daily_returns_df.cov() * 252
    portfolio_variance = np.dot(asset_weights.T, np.dot(portfolio_covariance, asset_weights))
    portfolio_volatility = np.sqrt(portfolio_variance)
    return portfolio_volatility

def calculate_portfolio_sharpe_ratio(portfolio_return_df, portfolio_volatility):
    """
    Calculate the sharpe ratio of the portfolio.
    Must only be ran after calculate_portfolio_return() and calculate_portfolio_volatility().
    
    :param portfolio_return_df: Average annual returns of the portfolio.
    :param portfolio_volatility: Portfolio volatility
    :type portfolio_return_df: Pandas DataFrame.
    :type portfolio_volatility: float
    """
    portfolio_sharpe_ratio = portfolio_return_df / portfolio_volatility
    return portfolio_sharpe_ratio
