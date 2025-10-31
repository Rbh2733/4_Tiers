# Backtesting Framework for 4-Tier Quantitative Stock Scoring System

## Overview

This document outlines the comprehensive backtesting methodology for validating the scoring system using real historical data. Due to API limitations in some environments, we provide both automated and manual approaches.

---

## 🎯 Backtesting Objectives

### Primary Goals:
1. **Validate Scoring System**: Confirm that higher scores correlate with better returns
2. **Test Exit Rules**: Verify 2-quarter rule and stop-losses work as intended
3. **Measure Alpha Generation**: Compare vs tier-appropriate benchmarks
4. **Assess Risk Management**: Evaluate draw downs, Sharpe ratios, volatility
5. **Compare v1.0 vs v2.0**: Quantify improvements from bonus caps and stop-losses

### Key Questions to Answer:
- Do Strong Buy (80+) stocks outperform Hold (60-69) stocks?
- Does the 2-quarter exit rule prevent holding deteriorating positions too long?
- Do v2.0 stop-losses reduce maximum drawdowns vs v1.0?
- Which tiers generate the most alpha after risk-adjustment?
- Does position sizing correctly balance risk vs return?

---

## 📊 Backtest Methodology

### Test Period
**Recommended**: 5 years (2019-2024)
- Captures multiple market regimes (bull, bear, recovery)
- Includes COVID crash (stress test)
- Sufficient data for quarterly rebalancing

### Stock Universe by Tier

**Tier 1 (Mega-Cap >$200B):**
- AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, BRK.B
- Benchmark: SPY (S&P 500)

**Tier 2 (Large-Cap $50-200B):**
- PLTR, SNOW, CRWD, DDOG, NET, ZS, TEAM, ADBE
- Benchmark: QQQ (NASDAQ-100)

**Tier 3 (Mid-Cap $10-50B):**
- RKLB, IONQ, BBAI, PATH, S, MDB, HUBS, ZM
- Benchmark: IWM (Russell 2000)

**Tier 4 (Small-Cap <$10B):**
- ASTS, LUNR, SPIR, PL, Bros, CAVA (select carefully)
- Benchmark: IWO (Russell 2000 Growth)

### Rebalancing Frequency
**Quarterly** (matches 2-quarter exit rule cadence)
- Re-score all positions
- Execute exits (2Q rule or stop loss)
- Rebalance positions to target allocations
- Add new positions if capacity

---

## 🔢 Data Requirements

### For Each Stock, Each Quarter:

**Price Data:**
- Daily OHLCV for momentum calculations
- Entry price, current price, stop loss levels
- 50-day and 200-day moving averages

**Fundamental Data (from 10-Q/10-K filings):**
- Revenue (TTM and quarterly)
- Operating Income & Margin
- Net Income & EPS
- Free Cash Flow
- Gross Profit & Margin
- Total Debt, Cash, Equity
- Shares Outstanding

**Calculated Metrics:**
- Market Cap (price × shares)
- P/E Ratio, FCF Yield, PEG Ratio
- ROIC, ROE, ROA
- Revenue Growth (YoY, 3Yr CAGR)
- EPS Growth (YoY, 3Yr CAGR)
- Operating Margin Trend (bps/year)
- 12M and 6M price returns
- Max Drawdown (trailing 1Y)

**Qualitative Inputs (manual):**
- Competitive moat assessment
- Management execution (earnings beats)
- TAM size and penetration estimates
- Customer concentration data
- Sector classification
- Economic cycle phase

---

## 📐 Scoring Process (Quarterly)

### Step 1: Data Collection (T-1)
Collect all fundamental and price data as of quarter-end

### Step 2: Component Scoring (T-1 to T)
For each stock:
1. Calculate each component score (0-100)
2. Apply bonuses (with v2.0 caps)
3. Apply penalties (concentration, burn rate)
4. Calculate weighted section totals
5. Sum to Raw Composite
6. Apply sector/cycle adjustments → Adjusted Composite
7. Assign rating (Strong Buy/Buy/Hold/Sell)

### Step 3: Position Sizing (T)
1. Calculate Beta Adjustment Factor
2. Calculate Drawdown Penalty Factor (v2.0)
3. Combined Risk Factor = Beta Adj × DD Penalty
4. Target % = (Base% × Score/100) / Combined Risk
5. Round to nearest 0.5%

### Step 4: Portfolio Construction (T)
1. Rank all stocks by Adjusted Composite Score
2. Select top N per tier (capacity limits)
3. Allocate capital according to position sizes
4. Respect tier allocation targets:
   - Tier 1: 40-50%
   - Tier 2: 25-35%
   - Tier 3: 12-20%
   - Tier 4: 5-10%
   - Cash: 5-10%

### Step 5: Exit Rule Application (T)
**2-Quarter Rule:**
- Track scores for 2 consecutive quarters
- IF score < tier minimum for 2Q → EXIT
- Mark for sale at next rebalance

**Stop Loss (v2.0):**
- Tier 1: -20% from entry
- Tier 2: -25% from entry
- Tier 3: -30% from entry
- Tier 4: -40% from entry
- IF stop hit → IMMEDIATE EXIT (intraday)

**Note:** Stop loss overrides 2Q rule

### Step 6: Rebalancing (T)
1. Execute exits from Step 5
2. Trim positions with >10% positive drift
3. Add to positions with >10% negative drift (if score strong)
4. Add new positions if capacity available
5. Record all trades with dates, prices, reasons

---

## 📈 Performance Metrics

### Returns
- **Total Return** (%)
- **CAGR** (annualized)
- **Excess Return** vs benchmark
- **Alpha** (risk-adjusted excess return)
- **Return by Tier** (attribution analysis)

### Risk
- **Volatility** (annualized std dev)
- **Max Drawdown** (%)
- **Max Drawdown Duration** (days)
- **Downside Deviation**
- **Beta** vs benchmark
- **Correlation** vs benchmark

### Risk-Adjusted
- **Sharpe Ratio** (return / volatility)
- **Sortino Ratio** (return / downside deviation)
- **Calmar Ratio** (CAGR / max drawdown)
- **Information Ratio** (alpha / tracking error)

### Win Rates
- **% Winning Positions** (closed profitable)
- **Avg Win** vs **Avg Loss**
- **Win/Loss Ratio**
- **Profit Factor** (gross profit / gross loss)

### Exit Effectiveness
- **2Q Rule Exits:** Count and avg return from initial entry
- **Stop Loss Exits:** Count and avg loss magnitude
- **Positions Held >1 Year:** % and avg return
- **Avg Holding Period** by rating

---

## 🔬 v1.0 vs v2.0 Comparison

Run backtest with BOTH versions on same universe, same period.

**Expected v2.0 Improvements:**
1. **Lower Max Drawdown**: -20/-25/-30% stops should limit losses
2. **Fewer Large Losses**: Stop losses prevent -40%+ individual position losses
3. **Higher Sharpe Ratio**: Better risk-adjusted returns
4. **More Exits Triggered**: Stricter scoring may flag more positions
5. **Smaller Position Sizes**: Drawdown penalty reduces high-risk allocations

**Comparison Table:**
```
Metric                  | v1.0    | v2.0    | Change
------------------------|---------|---------|--------
Total Return            | 85%     | 78%     | -7%
CAGR                    | 13.1%   | 12.3%   | -0.8%
Max Drawdown            | -32%    | -24%    | +8%  ✓
Sharpe Ratio            | 0.92    | 1.15    | +25% ✓
% Positions w/ >-30% loss| 8%      | 2%      | -6%  ✓
Avg Position Loss       | -18%    | -14%    | +4%  ✓
```

**Interpretation:**
- Slight reduction in raw returns (expected - more conservative)
- Significant improvement in risk metrics (goal achieved)
- Better risk-adjusted returns (Sharpe up 25%)
- Fewer catastrophic losses (stop-loss working)

---

## 🧪 Sensitivity Analysis

### Test Variations:

**1. Minimum Score Thresholds:**
- What if Tier 1 min = 65 (instead of 60)?
- Impact on portfolio turnover and returns

**2. Stop Loss Levels:**
- What if all tiers use -30% (uniform)?
- Trade-off between protection and whipsaw

**3. Rebalancing Frequency:**
- Monthly vs Quarterly vs Semi-Annual
- Transaction costs vs optimization

**4. Position Sizing:**
- Equal weight vs score-weighted vs risk-adjusted
- Which produces best Sharpe ratio?

**5. Sector Adjustments:**
- With vs without sector modifiers
- Does it improve score-return correlation?

**6. Economic Cycle Timing:**
- Retroactively apply cycle adjustments
- Does it add value or noise?

---

## 💻 Implementation Approaches

### Approach 1: Fully Automated (Ideal)
**Tools:**
- yfinance or Alpha Vantage for data
- Python pandas for calculations
- Backtrader or Zipline for simulation
- Matplotlib for visualization

**Pros:**
- Repeatable, scalable
- Can test many variations quickly
- Minimal manual work

**Cons:**
- Complex setup
- API limitations
- Fundamental data quality issues

### Approach 2: Semi-Automated (Practical)
**Tools:**
- Excel for score calculations (using v2.0 templates)
- Python for performance analysis
- Manual data entry from financial sites

**Pros:**
- Uses existing templates
- Full control over data quality
- Easier to debug

**Cons:**
- Time-consuming for large universe
- Manual entry errors possible
- Less scalable

### Approach 3: Historical Reconstruction (Manual)
**Process:**
1. Select 10-20 well-known stocks
2. Manually score them quarterly using historical data
3. Simulate portfolio using spreadsheet
4. Calculate performance metrics

**Pros:**
- Most accurate (hand-verified data)
- Deep understanding of each position
- High data quality

**Cons:**
- Very time-intensive
- Small sample size
- Not repeatable easily

---

## 📋 Example Backtest Results (Hypothetical)

### Portfolio: 20 stocks across 4 tiers, Quarterly rebal, 2019-2024

**Tier 1 Holdings (5 stocks, 45% allocation):**
- AAPL: Score 86 → 9% position
- MSFT: Score 88 → 10% position
- GOOGL: Score 82 → 8.5% position
- NVDA: Score 84 → 9% position
- META: Score 79 → 8.5% position

**Performance vs SPY:**
```
Metric                  | Portfolio | SPY    | Difference
------------------------|-----------|--------|------------
5Y Total Return         | 142%      | 98%    | +44%
CAGR                    | 19.3%     | 14.6%  | +4.7%
Max Drawdown            | -28%      | -34%   | +6%
Sharpe Ratio            | 1.28      | 0.91   | +0.37
Volatility              | 18.2%     | 17.8%  | +0.4%
% Winning Positions     | 72%       | N/A    | -
Avg Holding Period      | 3.2 qtrs  | N/A    | -
```

**Exit Rule Effectiveness:**
- 2Q Rule Exits: 12 positions, avg return -8% from entry
- Stop Loss Exits: 3 positions, avg loss -22%
- Voluntary Upgrades: 8 positions (scored better tier)

**Alpha Attribution by Tier:**
- Tier 1: +2.1% alpha (quality + momentum selection)
- Tier 2: +4.8% alpha (growth stock picking)
- Tier 3: +1.2% alpha (higher vol, mixed results)
- Tier 4: -0.5% alpha (moonshots underperformed)

**Key Insights:**
1. System successfully identified outperformers in Tiers 1-2
2. 2Q rule prevented holding degrading positions too long
3. Stop losses saved portfolio during COVID crash
4. Tier 4 selection needs improvement (too speculative)

---

## 🚀 Running Your Own Backtest

### Quick Start (Manual Method):

**Step 1: Select Universe (Week 1)**
- Choose 5-10 stocks per tier
- Ensure historical data availability back to 2019
- Mix of sectors for diversification

**Step 2: Collect Historical Data (Week 2-3)**
- Download quarterly financials (10-Q/10-K from SEC EDGAR)
- Download daily price history (Yahoo Finance, Google Finance)
- Organize in spreadsheets by quarter

**Step 3: Score Quarterly (Week 4-8)**
- Use v2.0 Excel templates
- Score each stock each quarter (20 quarters × 20 stocks = 400 scorings)
- Record scores in master tracking sheet

**Step 4: Simulate Portfolio (Week 9)**
- Implement position sizing formulas
- Apply exit rules each quarter
- Track all trades and capital allocation

**Step 5: Calculate Performance (Week 10)**
- Compute returns, drawdowns, Sharpe ratios
- Compare vs benchmarks
- Generate charts and attribution analysis

**Step 6: Document & Iterate (Week 11-12)**
- Write up findings
- Identify weaknesses
- Refine scoring components if needed

**Total Time Estimate:** 12 weeks for comprehensive manual backtest

---

## 📊 Expected Results & Validation

### Success Criteria:

**The system is validated if:**
1. ✅ **Score-Return Correlation >0.5**: Higher scores → higher returns
2. ✅ **Alpha vs Benchmark >2% annually**: Beats tier-appropriate index
3. ✅ **Sharpe Ratio >1.0**: Risk-adjusted returns competitive
4. ✅ **Max Drawdown <40%**: Survives market crashes
5. ✅ **2Q Rule Reduces Losses**: Exits save avg 10%+ vs buy-and-hold
6. ✅ **Win Rate >60%**: More winners than losers

**Red Flags (System Needs Revision):**
- ❌ No correlation between scores and returns
- ❌ Underperforms benchmarks consistently
- ❌ Excessive turnover (>100% annually)
- ❌ Large losses despite stop losses (slippage issues)
- ❌ Tier 4 consistently destroys capital

---

## 🔧 Data Sources

### Free Data Sources:
- **SEC EDGAR**: Official filings (10-Q, 10-K, 8-K)
- **Yahoo Finance**: Price history, basic fundamentals
- **FRED (Federal Reserve)**: Economic data for cycle phase
- **Company Investor Relations**: Earnings presentations, metrics

### Paid Data Sources (Optional):
- **Bloomberg Terminal**: Comprehensive data
- **FactSet**: Estimates, fundamentals
- **S&P Capital IQ**: Private company data
- **Koyfin**: Affordable alternative

### APIs for Automation:
- **Alpha Vantage**: Free tier available
- **IEX Cloud**: Real-time and historical
- **Polygon.io**: Affordable pricing
- **yfinance**: Free Python library (Yahoo Finance)

---

## 📝 Next Steps

1. **Choose Implementation Approach**: Fully automated, semi-automated, or manual
2. **Set Up Data Pipeline**: Select sources and collection method
3. **Score Historical Universe**: Start with 5-10 stocks, expand later
4. **Run Initial Backtest**: Test methodology on small sample
5. **Analyze Results**: Validate vs expectations
6. **Iterate & Improve**: Refine scoring components based on findings
7. **Expand Universe**: Scale to full 20-40 stock portfolio
8. **Document Thoroughly**: Create replicable process

---

## ⚠️ Important Caveats

### Limitations of Backtesting:
1. **Survivorship Bias**: Only testing stocks that survived (missing bankruptcies)
2. **Look-Ahead Bias**: Using data not available at time of decision
3. **Data Quality**: Historical fundamental data may have errors
4. **Transaction Costs**: Real-world costs reduce returns
5. **Liquidity**: Assumes perfect execution at closing prices
6. **Market Impact**: Large positions move prices
7. **Regime Change**: Past performance ≠ future results

### Best Practices:
- Use point-in-time data only (avoid look-ahead)
- Include delisted stocks if possible
- Model realistic transaction costs (0.1-0.5% per trade)
- Test on out-of-sample period (2024-2025)
- Stress test with worst historical drawdown periods
- Document all assumptions clearly

---

## 📚 Resources

**Books:**
- "Evidence-Based Technical Analysis" by David Aronson
- "Quantitative Trading" by Ernest Chan
- "Advances in Financial Machine Learning" by Marcos López de Prado

**Tools:**
- Backtrader (Python backtesting framework)
- Zipline (Quantopian's open-source engine)
- QuantConnect (cloud-based platform)
- Portfolio Visualizer (free online tool)

**Courses:**
- Coursera: "Computational Investing" (Georgia Tech)
- Udacity: "AI for Trading" Nanodegree
- DataCamp: "Quantitative Trading in Python"

---

**Status:** Framework documented, ready for implementation
**Next Action:** Choose implementation approach and begin data collection
**Time to Results:** 4-12 weeks depending on approach
