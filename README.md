# 4-Tier Quantitative Stock Scoring System

A comprehensive, multi-tier investment framework for analyzing and scoring stocks based on market capitalization. This system provides Excel templates with pre-configured formulas to evaluate stocks across five key dimensions: Valuation, Quality, Growth, Momentum, and tier-specific factors.

## 📊 Overview

This framework divides stocks into 4 tiers based on market cap, with progressively higher minimum scores and smaller position sizes for higher-risk tiers:

| Tier | Market Cap | Min Score | Position Size | Risk Level | Primary Focus |
|------|------------|-----------|---------------|------------|---------------|
| **Tier 1** | >$200B | 60 | 8-12% | Lowest | Quality (35%) |
| **Tier 2** | $50-200B | 65 | 5-8% | Low-Moderate | Growth (32%) |
| **Tier 3** | $10-50B | 67 | 3-5% | Moderate-High | Growth (38%) |
| **Tier 4** | <$10B | 70 | 1-3% | Highest | Growth (40%) |

## 📁 Files Included

### Excel Templates
1. **Tier1_MegaCap_Template.xlsx** - Mega-Cap Core stocks (>$200B)
2. **Tier2_LargeCap_Template.xlsx** - Large-Cap Growth stocks ($50-200B)
3. **Tier3_MidCap_Template.xlsx** - Mid-Cap Emerging stocks ($10-50B)
4. **Tier4_SmallCap_Template.xlsx** - Small-Cap Moonshots (<$10B)
5. **Portfolio_Summary.xlsx** - Portfolio tracking and rebalancing tool

### Python Scripts
- **generate_all_tiers.py** - Complete generator for all templates
- **generate_excel_templates.py** - Original Tier 1 generator

## 🚀 Quick Start

### 1. Choose the Right Tier
Select the template that matches your stock's market capitalization:
- Apple (AAPL), Microsoft (MSFT) → Tier 1
- Palantir (PLTR), Snowflake (SNOW) → Tier 2
- CrowdStrike (CRWD), Datadog (DDOG) → Tier 3
- Rocket Lab (RKLB), AST SpaceMobile (ASTS) → Tier 4

### 2. Fill in Stock Data
Open the appropriate tier template and enter data in the **white/unshaded cells**:
- **Stock Information**: Ticker, name, market cap, beta, prices
- **Component Scores**: For each metric, enter the raw input value (column B) and manually calculate the score (column C) based on the scoring brackets in column F

### 3. Review Results
The template automatically calculates:
- **Composite Score** (0-100) - Overall stock rating
- **Rating** - Strong Buy (80+), Buy (70-79), Hold (60-69), Sell (<60)
- **Target Position %** - Volatility-adjusted position size
- **Score Buffer** - Distance from minimum tier threshold

### 4. Track Your Portfolio
Use **Portfolio_Summary.xlsx** to:
- Monitor all holdings across all tiers
- Track allocation vs. targets
- Identify rebalancing opportunities
- Apply 2-quarter exit rules

## 📐 Scoring Methodology

### Tier 1: Mega-Cap Core (>$200B)
**Composite Formula:** `V×20% + Q×35% + G×25% + M×10% + FH×10%`

**Components:**
- **Valuation (20%)**: P/E Ratio, FCF Yield, PEG Ratio
- **Quality (35%)** ⭐ HIGHEST: ROIC, Operating Margin, Margin Trend, Moat, Management, Cash Conversion
- **Growth (25%)**: Revenue CAGR, Consistency, EPS CAGR, Future Potential, Analyst Consensus
- **Momentum (10%)**: 12M Return, Relative Strength vs SPY, Technical Setup
- **Financial Health (10%)**: Net Cash, FCF Generation, Capital Allocation

**Key Features:**
- Focus on stability and quality
- Benchmark: S&P 500 (SPY)
- No stop loss (quality-based exits only)

### Tier 2: Large-Cap Growth ($50-200B)
**Composite Formula:** `V×18% + Q×28% + G×32% + M×12% + SM×10%`

**Components:**
- **Valuation (18%)**: Forward P/E or P/S, PEG Ratio, Relative Valuation
- **Quality (28%)**: Revenue Scale, Profitability Status, Gross Margin, Margin Trajectory, Customer Retention (NRR), Market Position
- **Growth (32%)** ⭐ HIGHEST: Revenue Growth, Consistency, Forward Estimates, EPS vs Revenue, TAM & Penetration, Growth Drivers, Cyclicality
- **Momentum (12%)**: 6M Performance, Relative Strength vs QQQ, Technical Setup
- **Scale & Moat (10%)**: Competitive Position, Moat Development, Operating Leverage, Partnerships

**Key Features:**
- Emphasis on growth with quality
- Benchmark: NASDAQ-100 (QQQ)
- NRR >110% ideal for SaaS companies

### Tier 3: Mid-Cap Emerging ($10-50B)
**Composite Formula:** `V×15% + Q×22% + G×38% + M×15% + SI×10%`

**Components:**
- **Valuation (15%)**: P/S Ratio, Relative Valuation, Insider Ownership
- **Quality (22%)**: Revenue Scale, Profitability Path, Gross Margin, Unit Economics (LTV/CAC), Customer Quality
- **Growth (38%)** ⭐ HIGHEST: Revenue Growth, Growth Acceleration, Forward Estimates, TAM & Penetration, Driver Diversity, Cyclicality
- **Momentum (15%)**: 6M Return, Relative Strength vs IWM, Volume & Sentiment
- **Scale Inflection (10%)**: Market Position, Operating Leverage, Moat Formation, Partnerships

**Key Features:**
- Hypergrowth focus (30%+ revenue growth)
- Benchmark: Russell 2000 (IWM)
- TAM >$50B with <15% penetration ideal

### Tier 4: Small-Cap Moonshots (<$10B)
**Composite Formula:** `V×10% + Q×15% + G×40% + M×15% + D×20%`

**Components:**
- **Valuation (10%)**: P/S Ratio, Relative Valuation, Insider Ownership (>20%)
- **Quality (15%)**: Gross Margin, Revenue Quality, Unit Economics, Profitability Path
- **Growth (40%)** ⭐ HIGHEST: Revenue Growth (>75%), Consistency, TAM Size, Market Penetration (<5%), Driver Strength, Forward Estimates, Catalysts
- **Momentum (15%)**: 6M Return, Relative Strength vs IWO, Social Sentiment, Volume Surge
- **Disruption Potential (20%)**: Market Disruption, Technology Moat, Competitive Dynamics, Catalyst Pipeline

**Key Features:**
- Maximum growth emphasis (75%+ revenue growth)
- **MANDATORY -40% stop loss from entry**
- Benchmark: Russell 2000 Growth (IWO)
- Disruption of $100B+ markets ideal

## 🎯 Position Sizing Formulas

Each tier uses volatility-adjusted position sizing:

```excel
Tier 1: (10% × Score/100) / (1 + (Beta-1) × 0.75)
Tier 2: (7% × Score/100) / (1 + (Beta-1) × 1.0)
Tier 3: (5% × Score/100) / (1 + (Beta-1) × 1.3)
Tier 4: (3% × Score/100) / (1 + (Beta-1) × 1.5)
```

**Examples:**
- Tier 1 stock scoring 85 with Beta 1.1 → ~8% position
- Tier 2 stock scoring 88 with Beta 1.5 → ~4% position
- Tier 3 stock scoring 82 with Beta 1.8 → ~2% position
- Tier 4 stock scoring 90 with Beta 2.4 → ~1% position

## 📋 Exit Rules

### 2-Quarter Rule (All Tiers)
Exit if score drops below tier minimum for **2 consecutive quarters**:
- Tier 1: Exit if <60 for 2 quarters
- Tier 2: Exit if <65 for 2 quarters
- Tier 3: Exit if <67 for 2 quarters
- Tier 4: Exit if <70 for 2 quarters

### Stop Loss (Tier 4 Only)
**MANDATORY -40% stop loss from entry price** - This overrides the 2-quarter rule.

**Example:**
- Entry at $8.20 → Stop loss at $4.92 (immediate exit if hit)

## 🔄 Portfolio Rebalancing

### Drift Thresholds
- **>10% above target**: Trim position on next quarterly review
- **>10% below target**: Add if score ≥ tier minimum + 8 points
- **Quarterly review**: Trim all positions >5% off target

### Target Allocation by Tier
- **Tier 1**: 40-50% of portfolio (4-6 positions)
- **Tier 2**: 25-35% of portfolio (4-6 positions)
- **Tier 3**: 12-20% of portfolio (4-5 positions)
- **Tier 4**: 5-10% of portfolio (3-5 positions)
- **Cash**: 5-10% reserve

**Example $100K Portfolio:**
```
Tier 1: $45,000 (45%) - 5 positions @ 9% avg
Tier 2: $28,000 (28%) - 5 positions @ 5.6% avg
Tier 3: $15,000 (15%) - 5 positions @ 3% avg
Tier 4: $7,000 (7%)  - 5 positions @ 1.4% avg
Cash:   $5,000 (5%)
```

## 🚨 Red Flags & Automatic Score Reductions

### Tier 1 (Mega-Cap)
- ROIC drops below 15% → Quality -15
- Op margin contracts >100 bps → Quality -10
- Revenue growth decelerates >5% → Growth -15
- Breaks 200-day MA → Momentum -20
- Net cash becomes net debt → Financial Health -25

### Tier 2 (Large-Cap Growth)
- NRR drops below 100% → Quality -20
- Growth decelerates below 20% → Growth -20
- Path to profitability extends >2 quarters → Quality -15
- Operating margin contraction → Quality -15

### Tier 3 (Mid-Cap Emerging)
- NRR drops below 100% → Quality -20
- Growth decelerates below 25% → Growth -25
- Burn rate accelerates 20%+ → Quality -20
- Customer concentration increases → Quality -15

### Tier 4 (Small-Cap Moonshots)
- Burn rate accelerates 20%+ → Quality -25
- Growth decelerates below 40% → Growth -25
- **Stop loss hit (-40%) → AUTO EXIT** (no 2-quarter grace)
- Customer concentration >40% → Quality -20

## 💡 Usage Tips

### Data Sources
- **Financial Metrics**: Yahoo Finance, SEC filings (10-K, 10-Q)
- **Analyst Estimates**: Bloomberg, FactSet, Yahoo Finance
- **Technical Data**: TradingView, Yahoo Finance
- **SaaS Metrics**: Company earnings presentations
- **Beta**: Yahoo Finance, FactSet

### Scoring Best Practices
1. **Be Conservative**: When in doubt, use the lower end of scoring brackets
2. **Industry Context**: Adjust margins for industry norms (e.g., semiconductors vs. SaaS)
3. **Update Quarterly**: Rescore all holdings after earnings reports
4. **Document Assumptions**: Use the Notes column (F) to record your reasoning
5. **Track Score History**: Keep previous quarter scores to apply 2-quarter rule

### Common Mistakes to Avoid
- ❌ Ignoring beta in position sizing (can lead to oversized volatile positions)
- ❌ Not applying the 2-quarter rule (holding deteriorating positions too long)
- ❌ Forgetting Tier 4 stop losses (unlimited downside risk)
- ❌ Over-allocating to high-scoring small-caps (position size discipline critical)
- ❌ Mixing up benchmarks (SPY for Tier 1, QQQ for Tier 2, IWM for Tier 3, IWO for Tier 4)

## 🔧 Customization

### Regenerating Templates
If you need to modify the templates:

```bash
# Install dependencies
pip install openpyxl

# Generate all templates
python3 generate_all_tiers.py
```

### Modifying Scoring Components
Edit `generate_all_tiers.py` and modify the `add_component_section()` calls:
- Change weights (ensure they sum to 100%)
- Adjust scoring brackets in the notes column
- Add/remove bonus structures

### Custom Formulas
Each template uses Excel formulas that can be modified:
- Column E: Weighted scores (`=C × weight`)
- Composite: Sum of all weighted section totals
- Position sizing: Adjust base allocations or volatility factors

## 📊 Example Walkthroughs

### Example 1: Scoring a Mega-Cap (Tier 1)
**Stock: MSFT (Microsoft) - Market Cap $2.8T**

1. Open `Tier1_MegaCap_Template.xlsx`
2. Enter stock info: Ticker=MSFT, Beta=0.9, Price=$380
3. Score components:
   - P/E Ratio: 32 (current) vs 30 (historical) → Score 93
   - FCF Yield: 3.5% → Score 80
   - ROIC: 45% → Score 100
   - Op Margin: 42% → Score 100
   - Revenue Growth: 13% → Score 65
   - 12M Return: +45% → Score 100
4. Result: Composite Score 88 → **Strong Buy**
5. Position: 8.3% of portfolio

### Example 2: Scoring a Small-Cap (Tier 4)
**Stock: RKLB (Rocket Lab) - Market Cap $8B**

1. Open `Tier4_SmallCap_Template.xlsx`
2. Enter stock info: Ticker=RKLB, Beta=2.2, Entry=$8.20
3. **STOP LOSS**: Automatically calculates $4.92 (-40%)
4. Score components:
   - P/S: 28x with 80% growth → Base 50 + 35 bonus → Score 85
   - Gross Margin: 28% → Score 35
   - Revenue Growth: 85% → Score 95
   - Market Disruption: Attacking $300B+ market → Score 100
5. Result: Composite Score 82 → **Strong Buy**
6. Position: 2.2% of portfolio
7. **Monitor stop loss at $4.92**

## 📚 References

### System Standardizations
- All bonuses add to component score BEFORE capping at 100
- All individual component scores cap at 100 BEFORE weighting
- Composite scores range 0-100 (effectively limited by inputs)
- P/E calculations have floor at 0 (cannot go negative)
- Bracket scoring uses midpoint for ambiguous cases
- Final position sizes round to nearest 0.5%

### Rating System (All Tiers)
- **80-100**: Strong Buy
- **70-79**: Buy
- **60-69**: Hold
- **<60**: Sell

### Minimum Scores by Tier
- Tier 1: 60
- Tier 2: 65
- Tier 3: 67
- Tier 4: 70

## 🤝 Contributing

To contribute improvements:
1. Fork the repository
2. Modify `generate_all_tiers.py`
3. Regenerate templates
4. Test thoroughly with sample data
5. Submit a pull request

## 📄 License

This quantitative stock scoring system is provided as-is for educational and analytical purposes.

## ⚠️ Disclaimer

**This is not financial advice.** This scoring system is a tool for analysis and should not be the sole basis for investment decisions. Always:
- Conduct thorough due diligence
- Consult with financial advisors
- Understand your risk tolerance
- Never invest more than you can afford to lose
- Past performance does not guarantee future results

The creators assume no liability for investment losses resulting from use of this system.

---

## 📞 Support

For issues or questions:
- Review this README thoroughly
- Check the scoring methodology in each Excel template (Column F notes)
- Verify your data sources match the system requirements
- Ensure you're using the correct tier for your stock's market cap

---

**Version:** 1.0
**Last Updated:** October 2025
**Created by:** 4-Tier Quantitative Scoring System Team
