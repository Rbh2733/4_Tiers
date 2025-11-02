#!/usr/bin/env python3
"""
Enhanced Backtest with Realistic Historical Patterns
Simulates 5-year backtest (2019-2024) with realistic stock behavior
Compares v1.0 vs v2.0 system performance
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

np.random.seed(42)  # Reproducible results

# ================================================================================
# REALISTIC STOCK DATA GENERATION
# ================================================================================

def generate_realistic_stock_data(ticker, start_year=2019, end_year=2024):
    """
    Generate realistic quarterly scores and prices based on actual stock characteristics
    """
    quarters = pd.date_range(f'{start_year}-Q1', f'{end_year}-Q4', freq='QE')

    # Define realistic characteristics per stock
    stock_profiles = {
        'AAPL': {
            'tier': 1,
            'base_scores': {'valuation': 85, 'quality': 95, 'growth': 70, 'momentum': 85, 'other': 90},
            'volatility': 0.05,
            'price_start': 60,
            'price_trend': 3.5,  # Dollars per quarter
            'beta': 1.2,
            'has_covid_dip': True
        },
        'MSFT': {
            'tier': 1,
            'base_scores': {'valuation': 88, 'quality': 96, 'growth': 75, 'momentum': 90, 'other': 92},
            'volatility': 0.04,
            'price_start': 120,
            'price_trend': 4.0,
            'beta': 1.1,
            'has_covid_dip': True
        },
        'GOOGL': {
            'tier': 1,
            'base_scores': {'valuation': 82, 'quality': 93, 'growth': 68, 'momentum': 80, 'other': 88},
            'volatility': 0.06,
            'price_start': 90,
            'price_trend': 3.2,
            'beta': 1.15,
            'has_covid_dip': True
        },
        'PLTR': {
            'tier': 2,
            'base_scores': {'valuation': 60, 'quality': 75, 'growth': 90, 'momentum': 70, 'other': 80},
            'volatility': 0.15,
            'price_start': 10,
            'price_trend': 1.2,
            'beta': 2.0,
            'has_covid_dip': False  # IPO'd later
        },
        'SNOW': {
            'tier': 2,
            'base_scores': {'valuation': 55, 'quality': 78, 'growth': 92, 'momentum': 75, 'other': 82},
            'volatility': 0.18,
            'price_start': 200,
            'price_trend': 2.5,
            'beta': 1.9,
            'has_covid_dip': False
        },
        'CRWD': {
            'tier': 2,
            'base_scores': {'valuation': 65, 'quality': 82, 'growth': 88, 'momentum': 80, 'other': 85},
            'volatility': 0.14,
            'price_start': 50,
            'price_trend': 3.8,
            'beta': 1.7,
            'has_covid_dip': True
        },
        'RKLB': {
            'tier': 3,
            'base_scores': {'valuation': 58, 'quality': 70, 'growth': 85, 'momentum': 65, 'other': 75},
            'volatility': 0.25,
            'price_start': 8,
            'price_trend': 0.8,
            'beta': 2.2,
            'has_covid_dip': False
        },
        'PATH': {
            'tier': 3,
            'base_scores': {'valuation': 62, 'quality': 73, 'growth': 82, 'momentum': 68, 'other': 77},
            'volatility': 0.22,
            'price_start': 30,
            'price_trend': 1.0,
            'beta': 2.0,
            'has_covid_dip': False
        }
    }

    if ticker not in stock_profiles:
        return None

    profile = stock_profiles[ticker]

    # Generate quarterly scores
    scores = []
    prices = []

    for i, quarter in enumerate(quarters):
        # Score evolution (slight improvement over time with noise)
        score_trend = i * 0.5  # Gradual improvement

        # COVID impact (Q1-Q2 2020)
        covid_penalty = 0
        if profile['has_covid_dip'] and quarter >= pd.Timestamp('2020-03-31') and quarter <= pd.Timestamp('2020-06-30'):
            covid_penalty = 10  # Scores drop during COVID

        # Calculate component scores with realistic variation
        components = {}
        for component, base in profile['base_scores'].items():
            noise = np.random.randn() * profile['volatility'] * 100
            components[component] = np.clip(base + score_trend + noise - covid_penalty, 40, 100)

        # Sector adjustment (Tech gets +2)
        sector_adj = 2

        # Economic cycle (expansion until 2023, then neutral)
        cycle_adj = 1 if quarter.year < 2023 else 0

        # Calculate composites using tier weights
        if profile['tier'] == 1:
            raw_composite = (
                components['valuation'] * 0.20 +
                components['quality'] * 0.35 +
                components['growth'] * 0.25 +
                components['momentum'] * 0.10 +
                components['other'] * 0.10
            )
        elif profile['tier'] == 2:
            raw_composite = (
                components['valuation'] * 0.18 +
                components['quality'] * 0.28 +
                components['growth'] * 0.32 +
                components['momentum'] * 0.12 +
                components['other'] * 0.10
            )
        else:  # tier 3
            raw_composite = (
                components['valuation'] * 0.15 +
                components['quality'] * 0.22 +
                components['growth'] * 0.38 +
                components['momentum'] * 0.15 +
                components['other'] * 0.10
            )

        adjusted_composite = raw_composite + sector_adj + cycle_adj

        # Max drawdown (realistic values)
        max_dd = -15 - np.random.rand() * profile['volatility'] * 100

        scores.append({
            'date': quarter,
            'ticker': ticker,
            'tier': profile['tier'],
            **components,
            'sector_adj': sector_adj,
            'cycle_adj': cycle_adj,
            'raw_composite': raw_composite,
            'adjusted_composite': adjusted_composite,
            'beta': profile['beta'],
            'max_drawdown_1y': max_dd
        })

        # Generate realistic price
        covid_dip = 0
        if profile['has_covid_dip'] and quarter >= pd.Timestamp('2020-03-31') and quarter <= pd.Timestamp('2020-06-30'):
            covid_dip = -profile['price_start'] * 0.25  # 25% drop

        price = (profile['price_start'] +
                i * profile['price_trend'] +
                covid_dip +
                np.random.randn() * profile['price_start'] * profile['volatility'])
        prices.append(max(price, profile['price_start'] * 0.5))  # Floor at 50% of start

    return pd.DataFrame(scores), pd.Series(prices, index=quarters)


# ================================================================================
# V1.0 vs V2.0 SIMULATION
# ================================================================================

def simulate_v1_position_size(score, tier, beta):
    """v1.0 position sizing (beta only)"""
    base_allocations = {1: 10, 2: 7, 3: 5}
    volatility_factors = {1: 0.75, 2: 1.0, 3: 1.3}

    base = base_allocations[tier]
    vol_factor = volatility_factors[tier]
    beta_adj = 1 + (beta - 1) * vol_factor

    return (base * score / 100) / beta_adj


def simulate_v2_position_size(score, tier, beta, max_drawdown):
    """v2.0 position sizing (beta + drawdown)"""
    base_allocations = {1: 10, 2: 7, 3: 5}
    volatility_factors = {1: 0.75, 2: 1.0, 3: 1.3}

    base = base_allocations[tier]
    vol_factor = volatility_factors[tier]

    beta_adj = 1 + (beta - 1) * vol_factor
    dd_penalty = 1 + (abs(max_drawdown) / 100) * 0.5
    combined_risk = beta_adj * dd_penalty

    return (base * score / 100) / combined_risk


def run_backtest_comparison(stock_data, price_data, version='v2.0', starting_capital=100000):
    """
    Run backtest with specified system version
    """
    portfolio = {'cash': starting_capital, 'positions': {}}
    portfolio_values = []
    trades = []

    tier_minimums = {1: 60, 2: 65, 3: 67}
    stop_losses = {
        'v1.0': {1: None, 2: None, 3: None},  # Only Tier 4 has stop
        'v2.0': {1: 0.80, 2: 0.75, 3: 0.70}   # All tiers have stops
    }

    quarters = sorted(stock_data['date'].unique())

    for quarter_idx, quarter in enumerate(quarters):
        quarter_scores = stock_data[stock_data['date'] == quarter]

        # Check exits
        exits_this_quarter = []
        for ticker, pos in list(portfolio['positions'].items()):
            ticker_score = quarter_scores[quarter_scores['ticker'] == ticker]
            if ticker_score.empty:
                continue

            current_score = ticker_score['adjusted_composite'].values[0]
            tier = pos['tier']
            min_score = tier_minimums[tier]

            # 2-Quarter Rule
            if current_score < min_score:
                pos['quarters_below_min'] += 1
                if pos['quarters_below_min'] >= 2:
                    exits_this_quarter.append({
                        'ticker': ticker,
                        'reason': '2Q_RULE',
                        'score': current_score
                    })
            else:
                pos['quarters_below_min'] = 0

            # Stop Loss Check (v2.0 enhancement)
            stop_loss_pct = stop_losses[version][tier]
            if stop_loss_pct is not None:
                current_price = price_data[ticker][quarter]
                stop_price = pos['entry_price'] * stop_loss_pct

                if current_price <= stop_price:
                    exits_this_quarter.append({
                        'ticker': ticker,
                        'reason': f'STOP_LOSS_{version}',
                        'entry': pos['entry_price'],
                        'current': current_price,
                        'loss_pct': (current_price / pos['entry_price'] - 1) * 100
                    })

        # Execute exits
        for exit_info in exits_this_quarter:
            ticker = exit_info['ticker']
            if ticker not in portfolio['positions']:
                continue

            pos = portfolio['positions'][ticker]
            shares = pos['shares']
            exit_price = price_data[ticker][quarter]

            proceeds = shares * exit_price
            portfolio['cash'] += proceeds

            trades.append({
                'date': quarter,
                'ticker': ticker,
                'action': 'SELL',
                'reason': exit_info['reason'],
                'shares': shares,
                'price': exit_price,
                'value': proceeds,
                'entry_price': pos['entry_price'],
                'return_pct': (exit_price / pos['entry_price'] - 1) * 100,
                'holding_quarters': quarter_idx - pos['entry_quarter']
            })

            del portfolio['positions'][ticker]

        # Calculate current portfolio value
        position_value = sum(
            pos['shares'] * price_data[ticker][quarter]
            for ticker, pos in portfolio['positions'].items()
            if ticker in price_data
        )
        total_value = portfolio['cash'] + position_value

        portfolio_values.append({
            'date': quarter,
            'total_value': total_value,
            'cash': portfolio['cash'],
            'position_value': position_value,
            'num_positions': len(portfolio['positions'])
        })

        # Entry logic - only buy Strong Buy or Buy
        for _, row in quarter_scores.iterrows():
            ticker = row['ticker']
            score = row['adjusted_composite']

            if score < 70 or ticker in portfolio['positions']:
                continue

            # Calculate position size based on version
            if version == 'v1.0':
                target_pct = simulate_v1_position_size(score, row['tier'], row['beta'])
            else:
                target_pct = simulate_v2_position_size(score, row['tier'], row['beta'], row['max_drawdown_1y'])

            target_value = total_value * (target_pct / 100)

            if portfolio['cash'] >= target_value * 0.5:  # At least 50% of target
                price = price_data[ticker][quarter]
                shares = int(target_value / price)
                cost = shares * price

                if cost <= portfolio['cash']:
                    portfolio['cash'] -= cost
                    portfolio['positions'][ticker] = {
                        'shares': shares,
                        'entry_price': price,
                        'entry_date': quarter,
                        'entry_quarter': quarter_idx,
                        'tier': row['tier'],
                        'quarters_below_min': 0
                    }

                    trades.append({
                        'date': quarter,
                        'ticker': ticker,
                        'action': 'BUY',
                        'shares': shares,
                        'price': price,
                        'value': cost,
                        'score': score,
                        'target_pct': target_pct,
                        'version': version
                    })

    # Final value
    final_quarter = quarters[-1]
    final_position_value = sum(
        pos['shares'] * price_data[ticker][final_quarter]
        for ticker, pos in portfolio['positions'].items()
        if ticker in price_data
    )
    final_value = portfolio['cash'] + final_position_value

    return {
        'version': version,
        'final_value': final_value,
        'starting_capital': starting_capital,
        'total_return_pct': (final_value / starting_capital - 1) * 100,
        'portfolio_values': pd.DataFrame(portfolio_values),
        'trades': pd.DataFrame(trades)
    }


def calculate_metrics(results):
    """Calculate comprehensive performance metrics"""
    pv = results['portfolio_values'].set_index('date')
    pv['returns'] = pv['total_value'].pct_change()

    # Time period
    years = (pv.index[-1] - pv.index[0]).days / 365.25

    # Returns
    total_return = results['total_return_pct']
    cagr = (np.power(results['final_value'] / results['starting_capital'], 1/years) - 1) * 100

    # Risk
    volatility = pv['returns'].std() * np.sqrt(4) * 100  # Annualized
    cummax = pv['total_value'].cummax()
    drawdown = (pv['total_value'] - cummax) / cummax
    max_drawdown = drawdown.min() * 100

    # Risk-adjusted
    risk_free = 0.02
    sharpe = (cagr/100 - risk_free) / (volatility/100) if volatility > 0 else 0

    # Trade analysis
    trades = results['trades']
    sell_trades = trades[trades['action'] == 'SELL']

    if len(sell_trades) > 0:
        win_rate = (len(sell_trades[sell_trades['return_pct'] > 0]) / len(sell_trades)) * 100
        avg_win = sell_trades[sell_trades['return_pct'] > 0]['return_pct'].mean() if len(sell_trades[sell_trades['return_pct'] > 0]) > 0 else 0
        avg_loss = sell_trades[sell_trades['return_pct'] < 0]['return_pct'].mean() if len(sell_trades[sell_trades['return_pct'] < 0]) > 0 else 0

        # Exit breakdown
        exit_2q = len(sell_trades[sell_trades['reason'] == '2Q_RULE'])
        exit_stop_v1 = len(sell_trades[sell_trades['reason'].str.contains('STOP_LOSS_v1.0', na=False)])
        exit_stop_v2 = len(sell_trades[sell_trades['reason'].str.contains('STOP_LOSS_v2.0', na=False)])
    else:
        win_rate = 0
        avg_win = 0
        avg_loss = 0
        exit_2q = 0
        exit_stop_v1 = 0
        exit_stop_v2 = 0

    return {
        'Total Return': total_return,
        'CAGR': cagr,
        'Volatility': volatility,
        'Max Drawdown': max_drawdown,
        'Sharpe Ratio': sharpe,
        'Win Rate': win_rate,
        'Avg Win': avg_win,
        'Avg Loss': avg_loss,
        'Total Trades': len(trades[trades['action'] == 'BUY']),
        'Exit 2Q Rule': exit_2q,
        'Exit Stop Loss v1': exit_stop_v1,
        'Exit Stop Loss v2': exit_stop_v2,
        'Final Positions': pv['num_positions'].iloc[-1],
        'Years': years
    }


# ================================================================================
# MAIN EXECUTION
# ================================================================================

def main():
    print("="*80)
    print("4-TIER SYSTEM BACKTEST - v1.0 vs v2.0 COMPARISON")
    print("="*80)
    print("\nTest Period: 2019 Q1 - 2024 Q4 (5 years, 20 quarters)")
    print("Starting Capital: $100,000")
    print("Rebalancing: Quarterly")
    print("Universe: 8 stocks across 3 tiers\n")

    # Generate data for all stocks
    print("Generating realistic historical data...")
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'PLTR', 'SNOW', 'CRWD', 'RKLB', 'PATH']

    all_scores = []
    all_prices = {}

    for ticker in tickers:
        scores, prices = generate_realistic_stock_data(ticker)
        if scores is not None:
            all_scores.append(scores)
            all_prices[ticker] = prices
            print(f"  ✓ {ticker}: {len(scores)} quarters, Tier {scores['tier'].iloc[0]}")

    stock_data = pd.concat(all_scores, ignore_index=True)
    price_data = all_prices

    print(f"\n✓ Total data points: {len(stock_data)} score records\n")

    # Run v1.0 backtest
    print("="*80)
    print("RUNNING v1.0 BACKTEST (Original System)")
    print("="*80)
    print("Features: Beta-only position sizing, No stops for Tiers 1-3\n")

    results_v1 = run_backtest_comparison(stock_data, price_data, version='v1.0')
    metrics_v1 = calculate_metrics(results_v1)

    print("v1.0 Results:")
    print(f"  Final Value: ${results_v1['final_value']:,.0f}")
    print(f"  Total Return: {metrics_v1['Total Return']:.1f}%")
    print(f"  CAGR: {metrics_v1['CAGR']:.1f}%")
    print(f"  Max Drawdown: {metrics_v1['Max Drawdown']:.1f}%")
    print(f"  Sharpe Ratio: {metrics_v1['Sharpe Ratio']:.2f}")
    print(f"  Total Trades: {metrics_v1['Total Trades']}")

    # Run v2.0 backtest
    print("\n" + "="*80)
    print("RUNNING v2.0 BACKTEST (Enhanced System)")
    print("="*80)
    print("Features: Beta + Drawdown sizing, Graduated stops for all tiers\n")

    results_v2 = run_backtest_comparison(stock_data, price_data, version='v2.0')
    metrics_v2 = calculate_metrics(results_v2)

    print("v2.0 Results:")
    print(f"  Final Value: ${results_v2['final_value']:,.0f}")
    print(f"  Total Return: {metrics_v2['Total Return']:.1f}%")
    print(f"  CAGR: {metrics_v2['CAGR']:.1f}%")
    print(f"  Max Drawdown: {metrics_v2['Max Drawdown']:.1f}%")
    print(f"  Sharpe Ratio: {metrics_v2['Sharpe Ratio']:.2f}")
    print(f"  Total Trades: {metrics_v2['Total Trades']}")

    # Comparison
    print("\n" + "="*80)
    print("V1.0 vs V2.0 COMPARISON")
    print("="*80)

    comparison = pd.DataFrame({
        'v1.0': metrics_v1,
        'v2.0': metrics_v2
    }).T

    print("\nKey Metrics:")
    print(f"{'Metric':<25} {'v1.0':>12} {'v2.0':>12} {'Improvement':>12}")
    print("-"*65)

    key_metrics = ['Total Return', 'CAGR', 'Max Drawdown', 'Sharpe Ratio', 'Win Rate']
    for metric in key_metrics:
        v1_val = metrics_v1[metric]
        v2_val = metrics_v2[metric]

        if metric == 'Max Drawdown':
            improvement = v2_val - v1_val  # Less negative is better
            imp_str = f"+{improvement:.1f}%" if improvement > 0 else f"{improvement:.1f}%"
        elif metric in ['Total Return', 'CAGR', 'Sharpe Ratio', 'Win Rate']:
            improvement = ((v2_val / v1_val - 1) * 100) if v1_val != 0 else 0
            imp_str = f"+{improvement:.1f}%" if improvement > 0 else f"{improvement:.1f}%"
        else:
            imp_str = "N/A"

        if '%' in str(v1_val) or metric in ['Total Return', 'CAGR', 'Max Drawdown', 'Win Rate']:
            print(f"{metric:<25} {v1_val:>11.1f}% {v2_val:>11.1f}% {imp_str:>12}")
        else:
            print(f"{metric:<25} {v1_val:>12.2f} {v2_val:>12.2f} {imp_str:>12}")

    # Exit Analysis
    print("\n" + "="*80)
    print("EXIT ANALYSIS")
    print("="*80)

    print(f"\nv1.0 Exits:")
    print(f"  2-Quarter Rule: {metrics_v1['Exit 2Q Rule']}")
    print(f"  Stop Loss: {metrics_v1['Exit Stop Loss v1']} (Tier 4 only)")

    print(f"\nv2.0 Exits:")
    print(f"  2-Quarter Rule: {metrics_v2['Exit 2Q Rule']}")
    print(f"  Stop Loss: {metrics_v2['Exit Stop Loss v2']} (All tiers)")

    # Trade details
    print("\n" + "="*80)
    print("TRADE DETAILS")
    print("="*80)

    sells_v1 = results_v1['trades'][results_v1['trades']['action'] == 'SELL']
    sells_v2 = results_v2['trades'][results_v2['trades']['action'] == 'SELL']

    if len(sells_v1) > 0:
        print(f"\nv1.0 Closed Positions:")
        print(f"  Average Return: {sells_v1['return_pct'].mean():.1f}%")
        print(f"  Best Trade: {sells_v1['return_pct'].max():.1f}%")
        print(f"  Worst Trade: {sells_v1['return_pct'].min():.1f}%")
        print(f"  Avg Holding: {sells_v1['holding_quarters'].mean():.1f} quarters")

    if len(sells_v2) > 0:
        print(f"\nv2.0 Closed Positions:")
        print(f"  Average Return: {sells_v2['return_pct'].mean():.1f}%")
        print(f"  Best Trade: {sells_v2['return_pct'].max():.1f}%")
        print(f"  Worst Trade: {sells_v2['return_pct'].min():.1f}%")
        print(f"  Avg Holding: {sells_v2['holding_quarters'].mean():.1f} quarters")

    # Key Insights
    print("\n" + "="*80)
    print("KEY INSIGHTS")
    print("="*80)

    insights = []

    # Drawdown improvement
    dd_improvement = metrics_v2['Max Drawdown'] - metrics_v1['Max Drawdown']
    if dd_improvement > 0:
        insights.append(f"✓ v2.0 reduced max drawdown by {dd_improvement:.1f}% (stop losses working)")

    # Sharpe improvement
    sharpe_improvement = ((metrics_v2['Sharpe Ratio'] / metrics_v1['Sharpe Ratio']) - 1) * 100
    if sharpe_improvement > 0:
        insights.append(f"✓ v2.0 improved risk-adjusted returns by {sharpe_improvement:.1f}% (higher Sharpe)")

    # Position sizing
    if metrics_v2['Total Trades'] < metrics_v1['Total Trades']:
        insights.append(f"✓ v2.0 more conservative: {metrics_v1['Total Trades'] - metrics_v2['Total Trades']} fewer positions")

    # Stop losses
    if metrics_v2['Exit Stop Loss v2'] > 0:
        insights.append(f"✓ v2.0 stop losses prevented {metrics_v2['Exit Stop Loss v2']} large losses")

    if insights:
        for insight in insights:
            print(f"  {insight}")
    else:
        print("  Both systems performed similarly in this simulation")

    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80)

    if metrics_v2['Sharpe Ratio'] > metrics_v1['Sharpe Ratio']:
        print("\n✅ v2.0 VALIDATED: Superior risk-adjusted performance")
        print("\nv2.0 improvements:")
        print("  • Graduated stop losses reduced max drawdowns")
        print("  • Drawdown penalty factor sized positions more appropriately")
        print("  • Better risk-reward trade-off achieved")
    else:
        print("\n⚠️  Mixed results - both systems competitive")

    print("\nNote: This backtest uses simulated but realistic data patterns.")
    print("For production use, replace with actual historical fundamentals and prices.")
    print("\nSee BACKTEST_FRAMEWORK.md for methodology with real data sources.")
    print("\n" + "="*80)

    # Save results
    results_summary = {
        'v1.0': {
            'final_value': float(results_v1['final_value']),
            'metrics': {k: float(v) if isinstance(v, (int, float, np.number)) else v
                       for k, v in metrics_v1.items()}
        },
        'v2.0': {
            'final_value': float(results_v2['final_value']),
            'metrics': {k: float(v) if isinstance(v, (int, float, np.number)) else v
                       for k, v in metrics_v2.items()}
        }
    }

    with open('backtest_results.json', 'w') as f:
        json.dump(results_summary, f, indent=2)

    print("\n✓ Results saved to backtest_results.json\n")


if __name__ == "__main__":
    main()
