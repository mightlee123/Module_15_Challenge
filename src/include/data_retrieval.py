"""
Data Retrieval Module
-------------------------------
Data retrieval module which imports up-to-date financial data via Alpaca API. This information will be used to carry out
a series of financial calculations.
"""

import os
import requests
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import numpy as np
from pathlib import Path

def import_asset_data(start, end, tickers, timeframe):
    """
    Import asset data via Alpaca API.

    :param start: Start date of stock data.
    :param end: End date of stock data.
    :param tickers: List of stock tickers.
    :param timeframe: Timeframe of analysis.
    :type start: str as "YYYY-MM-DD" format.
    :type end: str as "YYYY-MM-DD" format.
    :type tickers: List of str values.
    :type timeframe: str of timeframe (i.e., "1D").
    :rtype stock_df: Pandas DataFrame. 
    """

    # Load .env environment variables.
    load_dotenv("./API_KEYS.env")

    # Retrieve ALPACA_API_KEY and ALPACA_SECRET_KEY.
    alpaca_api_key = os.getenv("ALPACA_API_KEY")
    alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

    # Create Alpaca API object.
    alpaca = tradeapi.REST(
        alpaca_api_key,
        alpaca_secret_key,
        api_version = "v2"
    )
    
    # Format dates as ISO.
    start_date = pd.Timestamp(start, tz="America/New_York").isoformat()
    end_date = pd.Timestamp(end, tz="America/New_York").isoformat()

    # Set timeframe to one day (1D)
    timeframe = "1D"
    
    # Retrieve and closing prices data frame of assets.
    close_df = alpaca.get_barset(
        tickers,
        timeframe,
        start = start_date,
        end = end_date
    ).df

    return close_df

def import_asset_data_jupyter(start, end, tickers, timeframe):
    """
    Import asset data via Alpaca API (to be ran in Jupyter Notebook).

    :param start: Start date of stock data.
    :param end: End date of stock data.
    :param tickers: List of stock tickers.
    :param timeframe: Timeframe of analysis.
    :type start: str as "YYYY-MM-DD" format.
    :type end: str as "YYYY-MM-DD" format.
    :type tickers: List of str values.
    :type timeframe: str of timeframe (i.e., "1D").
    :rtype stock_df: Pandas DataFrame. 
    """

    # Load .env environment variables.
    load_dotenv("API_KEYS.env")

    # Retrieve ALPACA_API_KEY and ALPACA_SECRET_KEY.
    alpaca_api_key = os.getenv("ALPACA_API_KEY")
    alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
    
    # Create Alpaca API object.
    alpaca = tradeapi.REST(
        alpaca_api_key,
        alpaca_secret_key,
        api_version = "v2"
    )
    
    # Format dates as ISO.
    start_date = pd.Timestamp(start, tz="America/New_York").isoformat()
    end_date = pd.Timestamp(end, tz="America/New_York").isoformat()

    # Set timeframe to one day (1D)
    timeframe = "1D"
    
    # Retrieve and closing prices data frame of assets.
    close_df = alpaca.get_barset(
        tickers,
        timeframe,
        start = start_date,
        end = end_date
    ).df

    return close_df

def format_close_price(close_df, tickers):
    """
    Formats a Pandas DataFrame such that only closing prices of assets are displayed.

    :param df: Numerical asset information.
    :param tickers: Tickers to extract closing price from.
    :type df: Pandas DataFrame.
    :type tickers: List of tickers as str data type.
    :rtype closing_prices_df: Modified Pandas DataFrame.
    """

    # Create an empty DataFrame to hold closing prices.
    closing_prices_df = pd.DataFrame()
    
    # For each ticker, retrieve closing prices and append to closing_prices_df.
    for ticker in tickers:
        closing_prices_df[ticker] = close_df[ticker]["close"]

    # Drop the time component of row date.
    closing_prices_df.index = closing_prices_df.index.date

    # Return closing prices.
    return closing_prices_df

def import_csv():
    spy_df = pd.read_csv("./Resources/SPY.csv")
    agg_df = pd.read_csv("./Resources/AGG.csv")
    btc_df = pd.read_csv("./Resources/BTC.csv")

    joined_df = pd.concat([spy_df, agg_df, btc_df], join = "inner", axis = 1)
    main_df = pd.DataFrame()
    main_df["SPY"] = joined_df.iloc[:, 3]
    main_df["AGG"] = joined_df.iloc[:, 1]
    main_df["BTC"] = joined_df.iloc[:, 5]
    # main_df = pd.DataFrame()
    # main_df["AGG"] = agg_df["Close"]
    # main_df["SPY"] = spy_df["Close"]
    # main_df["BTC"] = btc_df["Close"]
    return main_df

def jupyter_import_csv():
    
    csv_path_spy = Path("../Resources/SPY.csv")
    csv_path_agg = Path("../Resources/AGG.csv")
    csv_path_btc = Path("../Resources/BTC.csv")

    spy_df = pd.read_csv(csv_path_spy,index_col='Date', parse_dates=True, infer_datetime_format=True)
    agg_df = pd.read_csv(csv_path_agg,index_col='Date', parse_dates=True, infer_datetime_format=True)
    btc_df = pd.read_csv(csv_path_btc,index_col='Date', parse_dates=True, infer_datetime_format=True)
    
    joined_df = pd.concat([spy_df, agg_df, btc_df], axis=1)
    joined_df.columns = ['SPY', 'AGG', 'BTC']
    
    # main_df = pd.DataFrame()
    # main_df["AGG"] = agg_df["Close"]
    # main_df["SPY"] = spy_df["Close"]
    # main_df["BTC"] = btc_df["Close"]
    return joined_df