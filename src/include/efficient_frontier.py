# Import required modules.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_random_portfolios(num_portfolios, num_weights, daily_returns_df):
    """
    Generate a set of randomized portfolios and their average annualized returns and average annualized volatilities.

    :param num_portfolios: Number of portfolio samples.
    :param num_weights: Number of weights per portfolio.
    :param daily_returns_df: Pandas DataFrame() containing all daily returns.
    :type num_portfolios: int
    :type num_weights: int
    :type daily_returns_df: Pandas DataFrame().
    """

    RF = 0
    portfolio_returns = []
    portfolio_risk = []
    sharpe_ratio_port = []
    portfolio_weights = []

    for portfolio_sample_i in range(0, num_portfolios):

        # Generate a random sample of weights given num_weights.
        weights = np.random.random_sample(num_weights)

        # Ensure that the sum of our weights is equal to 1.
        weights = weights / np.sum(weights)

        # Calculate the annualized return for this portfolio sample and append to portfolio_returns list.
        annualized_return = np.sum((daily_returns_df.mean() * weights) * 252)
        portfolio_returns.append(annualized_return)

        # Calculate volatility of portfolio sample and append to portfolio_risk list.
        annualized_covariance = (daily_returns_df.cov()) * 252
        annualized_variance = np.dot(weights.T,np.dot(annualized_covariance, weights))
        annualized_volatility = np.sqrt(annualized_variance)
        portfolio_risk.append(annualized_volatility)

        # Calculate Sharpe Ratio of portfolio sample and append to sharpe_ratio_port list.
        sharpe_ratio = ((annualized_return - RF) / annualized_volatility)
        sharpe_ratio_port.append(sharpe_ratio)

        # Append portfolio weight to portfolio_weights list.
        portfolio_weights.append(weights)
    
    # Return portfolio_returns, portfolio_risk, sharpe_ratio_port and portfolio_weights.
    return np.array(portfolio_returns), np.array(portfolio_risk), np.array(sharpe_ratio_port), np.array(portfolio_weights)

def determine_optimal_portfolio(portfolio_metrics):
    """
    Given a sample of N portfolios, determine the optimal portfolio and its respective weights.
    """

    # Create a DataFrame of randomized portfolio metrics.
    portfolios_df = pd.DataFrame(portfolio_metrics)
    portfolios_df = portfolios_df.T
    portfolios_df.columns = ["portfolio_returns", "portfolio_risk", "sharpe_ratio", "portfolio_weights"]

    # Convert from object to float the first three columns.
    for col in ["portfolio_returns", "portfolio_risk",  "sharpe_ratio"]:
        portfolios_df[col] = portfolios_df[col].astype(float)
    
    # Determine the portfolio with the greatest Sharpe Ratio.
    greatest_sharpe_ratio_portfolio = portfolios_df.iloc[portfolios_df["sharpe_ratio"].idxmax()]
    
    # Determine the portfolio with the least risk.
    min_risk = portfolios_df.iloc[portfolios_df["portfolio_risk"].idxmin()]

    # Print out results.
    print("Portfolio with Greatest Sharpe Ratio")
    print("=====================================================")
    print(f"Returns = {greatest_sharpe_ratio_portfolio[0] * 100: .2f}%")
    print(f"Sharpe Ratio = {greatest_sharpe_ratio_portfolio[1]: .2f}")
    print(f"Weighting = [{greatest_sharpe_ratio_portfolio[3][0]: .2f} (SPY), {greatest_sharpe_ratio_portfolio[3][1]: .2f} (AGG), {greatest_sharpe_ratio_portfolio[3][2]:.2f} (BTC)]")
    print("-----------------------------------------------------")
    print()

    print("Portfolio with Least Risk")
    print("=====================================================")
    print(f"Returns = {min_risk[0] * 100: .2f}%")
    print(f"Sharpe Ratio = {min_risk[1]: .2f}")
    print(f"Weighting = [{min_risk[3][0]: .2f} (SPY), {min_risk[3][1]: .2f} (AGG), {min_risk[3][2]:.2f} (BTC)]")
    print("-----------------------------------------------------")
    print()

def plot_efficient_frontier(portfolio_risk, portfolio_returns):
    """
    Plot Efficient Frontier based off of randomized portfolio risk and returns.

    :param porfolio_risk: Randomized portfolio risks.
    :param portfolio_returns: Randomized portfolio returns associated with its respective risk.
    :type portfolio_risk: Numpy array.
    :type portfolio_returns: Numpy array.
    """

    plt.figure(figsize=(10, 5))
    plt.scatter(portfolio_risk, portfolio_returns, c = portfolio_returns / portfolio_risk) 
    plt.xlabel('Volatility')
    plt.ylabel('Returns')
    plt.colorbar(label='Sharpe ratio')