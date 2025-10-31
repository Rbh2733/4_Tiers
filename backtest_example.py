#!/usr/bin/env python3
"""
Simplified Backtesting Example for 4-Tier System
Demonstrates methodology with example data structure

This shows:
1. How to structure your scoring data
2. Portfolio construction logic
3. Exit rule implementation
4. Performance calculation
5. v1.0 vs v2.0 comparison framework

To use with real data:
- Replace example_scores with actual quarterly scores from your Excel templates
- Add real price data from Yahoo Finance / pandas_datareader
- Implement full position sizing with beta and drawdown factors
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List

# ================================================================================
# DATA STRUCTURES
# ================================================================================

def create_example_scoring_data():
    """
    Example structure for quarterly scoring data
    In practice, this comes from your Excel scoring templates
    """
    quarters = pd.date_range('2020-Q1', '2024-Q4', freq='Q')

    # Example: 3 stocks across 2 tiers
    scores = []

    for quarter in quarters:
        # Tier 1: AAPL - consistently strong
        scores.append({
            'date': quarter,
            'ticker': 'AAPL',
            'tier': 1,
            'valuation': 80 + np.random.randint(-5, 5),
            'quality': 92 + np.random.randint(-3, 3),
            'growth': 72 + np.random.randint(-5, 5),
            'momentum': 85 + np.random.randint(-10, 10),
            'other': 88 + np.random.randint(-5, 5),
            'sector_adj': 2,  # Tech
            'cycle_adj': 1 if quarter.year < 2023 else 0,
            'beta': 1.2,
            'max_drawdown_1y': -15 + np.random.randint(-5, 5)
        })

        # Tier 1: MSFT - very strong
        scores.append({
            'date': quarter,
            'ticker': 'MSFT',
            'tier': 1,
            'valuation': 85 + np.random.randint(-3, 3),
            'quality': 95 + np.random.randint(-2, 2),
            'growth': 75 + np.random.randint(-3, 3),
            'momentum': 90 + np.random.randint(-5, 5),
            'other': 92 + np.random.randint(-3, 3),
            'sector_adj': 2,
            'cycle_adj': 1 if quarter.year < 2023 else 0,
            'beta': 1.1,
            'max_drawdown_1y': -12 + np.random.randint(-3, 3)
        })

        # Tier 2: PLTR - volatile quality
        scores.append({
            'date': quarter,
            'ticker': 'PLTR',
            'tier': 2,
            'valuation': 65 + np.random.randint(-10, 10),
            'quality': 78 + np.random.randint(-8, 8),
            'growth': 88 + np.random.randint(-5, 5),
            'momentum': 75 + np.random.randint(-15, 15),
            'other': 82 + np.random.randint(-8, 8),
            'sector_adj': 2,
            'cycle_adj': 1 if quarter.year < 2023 else -1,
            'beta': 1.8,
            'max_drawdown_1y': -35 + np.random.randint(-10, 10)
        })

    df = pd.DataFrame(scores)

    # Calculate composite scores using v2.0 formulas
    tier_weights = {
        1: {'valuation': 0.20, 'quality': 0.35, 'growth': 0.25, 'momentum': 0.10, 'other': 0.10},
        2: {'valuation': 0.18, 'quality': 0.28, 'growth': 0.32, 'momentum': 0.12, 'other': 0.10},
    }

    df['raw_composite'] = df.apply(
        lambda row: (
            row['valuation'] * tier_weights[row['tier']]['valuation'] +
            row['quality'] * tier_weights[row['tier']]['quality'] +
            row['growth'] * tier_weights[row['tier']]['growth'] +
            row['momentum'] * tier_weights[row['tier']]['momentum'] +
            row['other'] * tier_weights[row['tier']]['other']
        ),
        axis=1
    )

    df['adjusted_composite'] = df['raw_composite'] + df['sector_adj'] + df['cycle_adj']

    # Ratings
    df['rating'] = pd.cut(df['adjusted_composite'],
                          bins=[0, 60, 70, 80, 100],
                          labels=['Sell', 'Hold', 'Buy', 'Strong Buy'])

    return df


def create_example_price_data():
    """
    Example price data
    In practice, fetch from Yahoo Finance using pandas_datareader
    """
    dates = pd.date_range('2020-01-01', '2024-12-31', freq='D')

    prices = {}

    # AAPL: Steady growth with COVID dip
    aapl_base = 100
    aapl_trend = np.linspace(0, 200, len(dates))
    covid_dip = np.where((dates >= '2020-03-01') & (dates <= '2020-04-01'), -30, 0)
    noise = np.random.randn(len(dates)) * 5
    prices['AAPL'] = aapl_base + aapl_trend + covid_dip + noise

    # MSFT: Strong consistent growth
    msft_base = 150
    msft_trend = np.linspace(0, 250, len(dates))
    covid_dip_msft = np.where((dates >= '2020-03-01') & (dates <= '2020-04-01'), -25, 0)
    noise_msft = np.random.randn(len(dates)) * 6
    prices['MSFT'] = msft_base + msft_trend + covid_dip_msft + noise_msft

    # PLTR: Volatile with big swings
    pltr_base = 20
    volatility = np.sin(np.linspace(0, 4*np.pi, len(dates))) * 15
    trend_pltr = np.linspace(0, 30, len(dates))
    noise_pltr = np.random.randn(len(dates)) * 8
    prices['PLTR'] = pltr_base + volatility + trend_pltr + noise_pltr

    df = pd.DataFrame(prices, index=dates)
    return df


# ================================================================================
# POSITION SIZING (v2.0)
# ================================================================================

def calculate_position_size_v2(score, tier, beta, max_drawdown):
    """
    Calculate position size using v2.0 methodology
    Includes both beta adjustment AND drawdown penalty
    """
    base_allocations = {1: 10, 2: 7, 3: 5, 4: 3}
    volatility_factors = {1: 0.75, 2: 1.0, 3: 1.3, 4: 1.5}

    base = base_allocations[tier]
    vol_factor = volatility_factors[tier]

    # Beta adjustment
    beta_adj = 1 + (beta - 1) * vol_factor

    # Drawdown penalty (v2.0 enhancement)
    dd_penalty = 1 + (abs(max_drawdown) / 100) * 0.5

    # Combined risk factor
    combined_risk = beta_adj * dd_penalty

    # Position size
    position = (base * score / 100) / combined_risk

    return position


# ================================================================================
# EXIT RULES
# ================================================================================

def check_exit_rules(position_tracker, current_scores, prices, tier_minimums):
    """
    Apply 2-quarter rule and stop losses

    Returns list of tickers to exit
    """
    exits = []

    for ticker, pos in position_tracker.items():
        current_score = current_scores[current_scores['ticker'] == ticker]['adjusted_composite'].values[0]
        tier = pos['tier']
        min_score = tier_minimums[tier]

        # 2-Quarter Rule
        if current_score < min_score:
            pos['quarters_below_min'] += 1
            if pos['quarters_below_min'] >= 2:
                exits.append({
                    'ticker': ticker,
                    'reason': '2Q_RULE',
                    'score': current_score,
                    'quarters_below': pos['quarters_below_min']
                })
                continue
        else:
            pos['quarters_below_min'] = 0

        # Stop Loss (v2.0)
        stop_loss_pcts = {1: 0.80, 2: 0.75, 3: 0.70, 4: 0.60}
        stop_price = pos['entry_price'] * stop_loss_pcts[tier]
        current_price = prices[ticker].iloc[-1]

        if current_price <= stop_price:
            exits.append({
                'ticker': ticker,
                'reason': 'STOP_LOSS',
                'entry': pos['entry_price'],
                'current': current_price,
                'loss_pct': (current_price / pos['entry_price'] - 1) * 100
            })

    return exits


# ================================================================================
# BACKTEST ENGINE
# ================================================================================

def run_backtest(scores_df, prices_df, starting_capital=100000):
    """
    Run quarterly backtest with v2.0 rules

    Returns performance metrics and trade history
    """
    portfolio = {'cash': starting_capital, 'positions': {}}
    trade_history = []
    portfolio_values = []
    tier_minimums = {1: 60, 2: 65, 3: 67, 4: 70}

    quarters = scores_df['date'].unique()

    for quarter in quarters:
        quarter_scores = scores_df[scores_df['date'] == quarter]

        # Check exits
        if portfolio['positions']:
            current_prices = prices_df.loc[:quarter].iloc[-1]
            exits = check_exit_rules(portfolio['positions'], quarter_scores,
                                    prices_df.loc[:quarter], tier_minimums)

            # Execute exits
            for exit_info in exits:
                ticker = exit_info['ticker']
                pos = portfolio['positions'][ticker]
                shares = pos['shares']
                exit_price = prices_df.loc[quarter, ticker]

                proceeds = shares * exit_price
                portfolio['cash'] += proceeds

                trade_history.append({
                    'date': quarter,
                    'ticker': ticker,
                    'action': 'SELL',
                    'reason': exit_info['reason'],
                    'shares': shares,
                    'price': exit_price,
                    'value': proceeds,
                    'entry_price': pos['entry_price'],
                    'return_pct': (exit_price / pos['entry_price'] - 1) * 100
                })

                del portfolio['positions'][ticker]

        # Calculate portfolio value
        position_value = sum(
            pos['shares'] * prices_df.loc[quarter, ticker]
            for ticker, pos in portfolio['positions'].items()
        )
        total_value = portfolio['cash'] + position_value
        portfolio_values.append({
            'date': quarter,
            'total_value': total_value,
            'cash': portfolio['cash'],
            'position_value': position_value
        })

        # Rebalancing: Size positions
        for _, row in quarter_scores.iterrows():
            ticker = row['ticker']
            score = row['adjusted_composite']

            # Only buy Strong Buy or Buy
            if score < 70:
                continue

            # Calculate target position size
            target_pct = calculate_position_size_v2(
                score, row['tier'], row['beta'], row['max_drawdown_1y']
            )
            target_value = total_value * (target_pct / 100)

            # If not held, consider buying
            if ticker not in portfolio['positions']:
                if portfolio['cash'] >= target_value:
                    price = prices_df.loc[quarter, ticker]
                    shares = int(target_value / price)
                    cost = shares * price

                    portfolio['cash'] -= cost
                    portfolio['positions'][ticker] = {
                        'shares': shares,
                        'entry_price': price,
                        'entry_date': quarter,
                        'tier': row['tier'],
                        'quarters_below_min': 0
                    }

                    trade_history.append({
                        'date': quarter,
                        'ticker': ticker,
                        'action': 'BUY',
                        'shares': shares,
                        'price': price,
                        'value': cost,
                        'score': score,
                        'target_pct': target_pct
                    })

    # Final portfolio value
    final_prices = prices_df.iloc[-1]
    final_position_value = sum(
        pos['shares'] * final_prices[ticker]
        for ticker, pos in portfolio['positions'].items()
    )
    final_value = portfolio['cash'] + final_position_value

    return {
        'final_value': final_value,
        'starting_capital': starting_capital,
        'total_return': (final_value / starting_capital - 1) * 100,
        'portfolio_values': pd.DataFrame(portfolio_values),
        'trades': pd.DataFrame(trade_history)
    }


# ================================================================================
# PERFORMANCE ANALYSIS
# ================================================================================

def calculate_performance_metrics(results):
    """Calculate key performance metrics"""

    portfolio_values = results['portfolio_values']
    portfolio_values = portfolio_values.set_index('date')
    portfolio_values['returns'] = portfolio_values['total_value'].pct_change()

    # Total Return
    total_return = results['total_return']

    # CAGR
    years = (portfolio_values.index[-1] - portfolio_values.index[0]).days / 365.25
    cagr = (np.power(results['final_value'] / results['starting_capital'], 1/years) - 1) * 100

    # Volatility (annualized)
    volatility = portfolio_values['returns'].std() * np.sqrt(4) * 100  # Quarterly to annual

    # Max Drawdown
    cummax = portfolio_values['total_value'].cummax()
    drawdown = (portfolio_values['total_value'] - cummax) / cummax
    max_drawdown = drawdown.min() * 100

    # Sharpe Ratio (assuming 2% risk-free rate)
    risk_free_rate = 0.02
    excess_return = (cagr / 100) - risk_free_rate
    sharpe = excess_return / (volatility / 100) if volatility > 0 else 0

    # Win Rate
    trades = results['trades']
    if len(trades[trades['action'] == 'SELL']) > 0:
        winning_trades = len(trades[(trades['action'] == 'SELL') & (trades['return_pct'] > 0)])
        total_trades = len(trades[trades['action'] == 'SELL'])
        win_rate = (winning_trades / total_trades) * 100
    else:
        win_rate = 0

    return {
        'Total Return': f"{total_return:.1f}%",
        'CAGR': f"{cagr:.1f}%",
        'Volatility': f"{volatility:.1f}%",
        'Max Drawdown': f"{max_drawdown:.1f}%",
        'Sharpe Ratio': f"{sharpe:.2f}",
        'Win Rate': f"{win_rate:.1f}%",
        'Total Trades': len(trades[trades['action'] == 'BUY']),
        'Final Value': f"${results['final_value']:,.0f}"
    }


# ================================================================================
# MAIN EXECUTION
# ================================================================================

def main():
    """Run example backtest"""

    print("="*70)
    print("4-TIER QUANTITATIVE STOCK SCORING SYSTEM - BACKTEST EXAMPLE")
    print("="*70)
    print("\nThis is a simplified demonstration using example data.")
    print("To use with real stocks:")
    print("  1. Score stocks quarterly using v2.0 Excel templates")
    print("  2. Fetch price data from Yahoo Finance")
    print("  3. Replace example_scores with your actual data")
    print("  4. Run backtest using this framework\n")

    print("Generating example data...")
    scores = create_example_scoring_data()
    prices = create_example_price_data()

    print(f"✓ Scoring data: {len(scores)} records across {len(scores['ticker'].unique())} stocks")
    print(f"✓ Price data: {len(prices)} days")

    print("\nSample Scores (first quarter):")
    print(scores[scores['date'] == scores['date'].min()][
        ['ticker', 'tier', 'raw_composite', 'adjusted_composite', 'rating']
    ].to_string(index=False))

    print("\n" + "="*70)
    print("Running backtest...")
    print("="*70)

    results = run_backtest(scores, prices, starting_capital=100000)

    print("\n" + "="*70)
    print("PERFORMANCE METRICS")
    print("="*70)

    metrics = calculate_performance_metrics(results)
    for metric, value in metrics.items():
        print(f"{metric:20s}: {value}")

    print("\n" + "="*70)
    print("TRADE HISTORY (First 10 Trades)")
    print("="*70)

    trades = results['trades'].head(10)
    print(trades[['date', 'ticker', 'action', 'shares', 'price', 'value']].to_string(index=False))

    print("\n" + "="*70)
    print("EXIT ANALYSIS")
    print("="*70)

    exit_trades = results['trades'][results['trades']['action'] == 'SELL']
    if len(exit_trades) > 0:
        print(f"\nTotal Exits: {len(exit_trades)}")
        print("\nBy Reason:")
        print(exit_trades.groupby('reason').size())

        print("\nExit Returns:")
        print(f"  Average: {exit_trades['return_pct'].mean():.1f}%")
        print(f"  Best: {exit_trades['return_pct'].max():.1f}%")
        print(f"  Worst: {exit_trades['return_pct'].min():.1f}%")
    else:
        print("No exits during backtest period")

    print("\n" + "="*70)
    print("PORTFOLIO EVOLUTION")
    print("="*70)

    pv = results['portfolio_values']
    print(f"\nStarting Value: ${pv.iloc[0]['total_value']:,.0f}")
    print(f"Ending Value:   ${pv.iloc[-1]['total_value']:,.0f}")
    print(f"Peak Value:     ${pv['total_value'].max():,.0f}")
    print(f"Trough Value:   ${pv['total_value'].min():,.0f}")

    print("\n" + "="*70)
    print("\n✓ Backtest complete!")
    print("\nTo extend this example:")
    print("  • Add more stocks (expand to 20-40)")
    print("  • Use real historical data")
    print("  • Add benchmark comparison (SPY, QQQ, IWM, IWO)")
    print("  • Implement Monte Carlo simulation")
    print("  • Test sensitivity to parameters")
    print("  • Compare v1.0 vs v2.0 side-by-side")

    print("\nSee BACKTEST_FRAMEWORK.md for complete methodology.\n")


if __name__ == "__main__":
    main()
