import sys
import fire
import pandas as pd 
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import datetime as dt
from pytz import timezone
import numpy as np 

# Import profiler functions.
from include.profiler import get_info
from include.profiler import qualification
from include.profiler import risk_profile

# Import data retrieval.
from include.data_retrieval import import_asset_data
from include.data_retrieval import format_close_price
from include.data_retrieval import import_csv

# Import calculation functions.
from include.calculations import calculate_average_annual_returns
from include.calculations import calculate_average_annual_volatility
from include.calculations import calculate_daily_returns
from include.calculations import calculate_sharpe_ratio
from include.calculations import calculate_portfolio_return
from include.calculations import calculate_portfolio_volatility
from include.calculations import calculate_portfolio_sharpe_ratio

# Import Efficient Frontier functions.
from include.efficient_frontier import generate_random_portfolios
from include.efficient_frontier import determine_optimal_portfolio

# Tickers.
timeframe = "1D"
tickers = ["SPY", "AGG", "BTC"]

# Weights per client risk profile.  
risk_profile_weights = {"conservative" : [0.1, 0.9, 0.0], "moderately conservative" : [0.25, 0.7, 0.05], 
                        "moderate" : [0.6, 0.3, 0.1], "moderately aggressive" : [0.75, 0.2, 0.05],
                        "aggressive" : [0.8, 0.0, 0.2]}
                  
def run():
    """The main function for running the script."""

    # Get investor's information
    cash, assets, income, liquidity = get_info()

    # Determine qualifying investable amount
    net_worth = qualification(cash, assets, income, liquidity)
                  
    # Determine investor's risk profile by determining ability to take risk defined by investment time horizon (age) and willingness to risk defined by comfort level with loss
    risk_prof = risk_profile()

    # Import historical financial data and retrieve closing prices.
    #raw_data_df = import_asset_data(start_date, end_date, tickers, timeframe)
    #raw_data_close_df = format_close_price(raw_data_df, tickers)
    raw_data_close_df = import_csv()   

    # Retrieve average annual returns and average annual volatility.
    daily_returns_df = calculate_daily_returns(raw_data_close_df)
    average_annual_returns_df = calculate_average_annual_returns(daily_returns_df)
    average_annual_volatility_df = calculate_average_annual_volatility(daily_returns_df)
    

    # Calculate portfolio returns, volatility and Sharpe Ratio per risk profile.
    portfolio_return = calculate_portfolio_return(daily_returns_df, risk_profile_weights[risk_prof])
    portfolio_volatility = calculate_portfolio_volatility(daily_returns_df, risk_profile_weights[risk_prof])
    portfolio_sharpe_ratio = calculate_portfolio_sharpe_ratio(portfolio_return, portfolio_volatility)

    # Print portfolio metrics (5-year).
    print("Portfolio Statistics per Client Risk Profile (5-Year)")
    print("=====================================================")
    print(f"Return = {portfolio_return * 100: .2f}%")
    print(f"Volatility = {portfolio_volatility * 100: .2f}%")
    print(f"Sharpe Ratio = {portfolio_sharpe_ratio: .2f}")
    print(f"Weighting = [{risk_profile_weights[risk_prof][0]} (SPY), {risk_profile_weights[risk_prof][1]} (AGG), {risk_profile_weights[risk_prof][2]} (BTC)]")
    print("-----------------------------------------------------")
    print()

    # Determine optimized portfolios.
    portfolio_returns, portfolio_risk, sharpe_ratio_port, portfolio_weights = generate_random_portfolios(100, 3, daily_returns_df)
    portfolio_metrics = [portfolio_returns, portfolio_risk, sharpe_ratio_port, portfolio_weights]
    determine_optimal_portfolio(portfolio_metrics)

    # Exit out of program.
    sys.exit()

if __name__ == "__main__":
    fire.Fire(run)