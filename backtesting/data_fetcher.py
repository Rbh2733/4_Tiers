#!/usr/bin/env python3
"""
Real Historical Data Fetcher
Fetches actual financial data from Yahoo Finance and other free sources
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')


class HistoricalDataFetcher:
    """Fetches real historical financial and price data"""

    def __init__(self):
        self.cache = {}

    def fetch_stock_data(self, ticker: str, start_date: str, end_date: str) -> Dict:
        """
        Fetch comprehensive historical data for a stock

        Returns:
        {
            'prices': DataFrame with OHLCV data,
            'fundamentals': Dict of quarterly fundamentals,
            'info': Current stock info,
            'financials': Income statements,
            'balance_sheet': Balance sheets,
            'cashflow': Cash flow statements
        }
        """
        print(f"Fetching data for {ticker}...")

        try:
            stock = yf.Ticker(ticker)

            # Price history
            prices = stock.history(start=start_date, end=end_date)

            # Fundamentals (quarterly for more granular scoring)
            quarterly_financials = stock.quarterly_financials
            quarterly_balance_sheet = stock.quarterly_balance_sheet
            quarterly_cashflow = stock.quarterly_cashflow

            # Annual for some metrics
            annual_financials = stock.financials
            annual_balance_sheet = stock.balance_sheet
            annual_cashflow = stock.cashflow

            # Current info
            info = stock.info

            return {
                'ticker': ticker,
                'prices': prices,
                'quarterly_financials': quarterly_financials,
                'quarterly_balance_sheet': quarterly_balance_sheet,
                'quarterly_cashflow': quarterly_cashflow,
                'annual_financials': annual_financials,
                'annual_balance_sheet': annual_balance_sheet,
                'annual_cashflow': annual_cashflow,
                'info': info,
                'success': True
            }

        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return {
                'ticker': ticker,
                'success': False,
                'error': str(e)
            }

    def calculate_fundamental_metrics(self, data: Dict, as_of_date: datetime) -> Dict:
        """
        Calculate fundamental metrics from historical data as of a specific date
        This simulates what we would have known at that point in time
        """
        try:
            metrics = {
                'ticker': data['ticker'],
                'date': as_of_date,
                'success': True
            }

            # Get the most recent data available as of as_of_date
            qf = data['quarterly_financials']
            qb = data['quarterly_balance_sheet']
            qc = data['quarterly_cashflow']

            # Filter to only use data available before as_of_date
            if not qf.empty:
                qf = qf.loc[:, qf.columns <= as_of_date]
            if not qb.empty:
                qb = qb.loc[:, qb.columns <= as_of_date]
            if not qc.empty:
                qc = qc.loc[:, qc.columns <= as_of_date]

            if qf.empty or qb.empty:
                metrics['success'] = False
                return metrics

            # Revenue (TTM)
            revenue_ttm = self._safe_get_ttm(qf, 'Total Revenue', 4)
            metrics['revenue_ttm'] = revenue_ttm

            # Operating Income (TTM)
            operating_income_ttm = self._safe_get_ttm(qf, 'Operating Income', 4)
            metrics['operating_income_ttm'] = operating_income_ttm

            # Net Income (TTM)
            net_income_ttm = self._safe_get_ttm(qf, 'Net Income', 4)
            metrics['net_income_ttm'] = net_income_ttm

            # Operating Margin
            if revenue_ttm and revenue_ttm != 0:
                metrics['operating_margin'] = (operating_income_ttm / revenue_ttm) * 100

            # Gross Profit and Margin
            gross_profit_ttm = self._safe_get_ttm(qf, 'Gross Profit', 4)
            if revenue_ttm and revenue_ttm != 0 and gross_profit_ttm:
                metrics['gross_margin'] = (gross_profit_ttm / revenue_ttm) * 100

            # Free Cash Flow (TTM)
            operating_cf = self._safe_get_ttm(qc, 'Operating Cash Flow', 4)
            capex = self._safe_get_ttm(qc, 'Capital Expenditure', 4)
            if operating_cf and capex:
                metrics['fcf_ttm'] = operating_cf + capex  # capex is negative

            # Balance Sheet items (most recent quarter)
            if not qb.empty and len(qb.columns) > 0:
                latest_bs = qb.iloc[:, 0]

                # Cash and equivalents
                metrics['cash'] = self._safe_get(latest_bs, ['Cash And Cash Equivalents', 'Cash'])

                # Total Debt
                metrics['total_debt'] = self._safe_get(latest_bs, ['Total Debt', 'Long Term Debt'])

                # Total Equity
                metrics['total_equity'] = self._safe_get(latest_bs, ['Total Equity', 'Stockholders Equity'])

            # Revenue Growth (YoY)
            if not qf.empty and len(qf.columns) >= 5:
                current_rev = self._safe_get(qf.iloc[:, 0], 'Total Revenue')
                yoy_rev = self._safe_get(qf.iloc[:, 4], 'Total Revenue')
                if current_rev and yoy_rev and yoy_rev != 0:
                    metrics['revenue_growth_yoy'] = ((current_rev / yoy_rev) - 1) * 100

            # EPS Growth (YoY)
            if not qf.empty and len(qf.columns) >= 5:
                current_ni = self._safe_get(qf.iloc[:, 0], 'Net Income')
                yoy_ni = self._safe_get(qf.iloc[:, 4], 'Net Income')
                if current_ni and yoy_ni and yoy_ni != 0:
                    metrics['eps_growth_yoy'] = ((current_ni / yoy_ni) - 1) * 100

            # Get price data for momentum and valuation
            prices = data['prices']
            if not prices.empty:
                # Current price
                price_slice = prices[prices.index <= as_of_date]
                if not price_slice.empty:
                    current_price = price_slice['Close'].iloc[-1]
                    metrics['price'] = current_price

                    # Market Cap (approximate)
                    shares_out = data['info'].get('sharesOutstanding', None)
                    if shares_out:
                        metrics['market_cap'] = current_price * shares_out / 1e9  # in billions

                    # 12-month return
                    one_year_ago = as_of_date - timedelta(days=365)
                    past_price_slice = prices[prices.index <= one_year_ago]
                    if not past_price_slice.empty:
                        past_price = past_price_slice['Close'].iloc[-1]
                        metrics['return_12m'] = ((current_price / past_price) - 1) * 100

                    # 6-month return
                    six_months_ago = as_of_date - timedelta(days=180)
                    past_price_slice = prices[prices.index <= six_months_ago]
                    if not past_price_slice.empty:
                        past_price = past_price_slice['Close'].iloc[-1]
                        metrics['return_6m'] = ((current_price / past_price) - 1) * 100

                    # 50-day and 200-day moving averages
                    price_slice_50d = prices[prices.index <= as_of_date].tail(50)
                    if len(price_slice_50d) >= 50:
                        metrics['ma_50'] = price_slice_50d['Close'].mean()

                    price_slice_200d = prices[prices.index <= as_of_date].tail(200)
                    if len(price_slice_200d) >= 200:
                        metrics['ma_200'] = price_slice_200d['Close'].mean()

                    # Max Drawdown (1 year)
                    one_year_prices = prices[(prices.index <= as_of_date) &
                                            (prices.index >= one_year_ago)]
                    if not one_year_prices.empty:
                        cummax = one_year_prices['Close'].cummax()
                        drawdown = (one_year_prices['Close'] - cummax) / cummax
                        metrics['max_drawdown_1y'] = drawdown.min() * 100

            # Calculate P/E ratio if possible
            if 'market_cap' in metrics and 'net_income_ttm' in metrics:
                if metrics['net_income_ttm'] and metrics['net_income_ttm'] > 0:
                    metrics['pe_ratio'] = (metrics['market_cap'] * 1e9) / (metrics['net_income_ttm'])

            # FCF Yield
            if 'fcf_ttm' in metrics and 'market_cap' in metrics and metrics['market_cap']:
                metrics['fcf_yield'] = (metrics['fcf_ttm'] / (metrics['market_cap'] * 1e9)) * 100

            return metrics

        except Exception as e:
            print(f"Error calculating metrics for {data['ticker']}: {e}")
            return {
                'ticker': data['ticker'],
                'date': as_of_date,
                'success': False,
                'error': str(e)
            }

    def _safe_get_ttm(self, df, field_name, periods=4):
        """Safely get TTM (trailing 12 months) value by summing last N quarters"""
        try:
            if df.empty or len(df.columns) < periods:
                return None

            if field_name in df.index:
                values = df.loc[field_name, :periods]
                # Filter out NaN values
                values = values.dropna()
                if len(values) > 0:
                    return values.sum()
            return None
        except:
            return None

    def _safe_get(self, series_or_df, field_names):
        """Safely get a value from a series, trying multiple field names"""
        if not isinstance(field_names, list):
            field_names = [field_names]

        try:
            for field in field_names:
                if isinstance(series_or_df, pd.Series):
                    if field in series_or_df.index:
                        val = series_or_df[field]
                        if pd.notna(val):
                            return float(val)
                elif isinstance(series_or_df, pd.DataFrame):
                    if field in series_or_df.index:
                        val = series_or_df.loc[field].iloc[0]
                        if pd.notna(val):
                            return float(val)
            return None
        except:
            return None

    def fetch_benchmark_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch benchmark (index) price history"""
        try:
            benchmark = yf.Ticker(ticker)
            prices = benchmark.history(start=start_date, end=end_date)
            return prices['Close']
        except Exception as e:
            print(f"Error fetching benchmark {ticker}: {e}")
            return pd.DataFrame()

    def get_sector_for_ticker(self, ticker: str) -> str:
        """Get sector for a ticker"""
        try:
            stock = yf.Ticker(ticker)
            sector = stock.info.get('sector', 'Unknown')
            return sector
        except:
            return 'Unknown'


def test_data_fetcher():
    """Test the data fetcher with a real stock"""
    fetcher = HistoricalDataFetcher()

    # Test with Microsoft
    print("Testing data fetcher with MSFT...")
    data = fetcher.fetch_stock_data('MSFT', '2020-01-01', '2024-01-01')

    if data['success']:
        print("✓ Successfully fetched MSFT data")
        print(f"  Price data points: {len(data['prices'])}")
        print(f"  Quarterly financials: {data['quarterly_financials'].shape}")

        # Test metrics calculation
        print("\nCalculating metrics as of 2023-06-30...")
        metrics = fetcher.calculate_fundamental_metrics(
            data,
            datetime(2023, 6, 30)
        )

        if metrics['success']:
            print("✓ Successfully calculated metrics")
            print(f"  Revenue TTM: ${metrics.get('revenue_ttm', 0)/1e9:.1f}B")
            print(f"  Operating Margin: {metrics.get('operating_margin', 0):.1f}%")
            print(f"  Market Cap: ${metrics.get('market_cap', 0):.1f}B")
            print(f"  12M Return: {metrics.get('return_12m', 0):.1f}%")
        else:
            print("✗ Failed to calculate metrics")
    else:
        print("✗ Failed to fetch MSFT data")

    # Test benchmark
    print("\nTesting benchmark data (SPY)...")
    spy = fetcher.fetch_benchmark_data('SPY', '2020-01-01', '2024-01-01')
    if not spy.empty:
        print(f"✓ Successfully fetched SPY data: {len(spy)} data points")
    else:
        print("✗ Failed to fetch SPY data")


if __name__ == "__main__":
    test_data_fetcher()
