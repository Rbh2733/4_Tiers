# Changelog - Version 2.0 (Enhanced)

## Overview
Version 2.0 addresses critical structural issues identified in the original system, including bonus stacking, insufficient risk management, and methodology gaps.

---

## 🔴 CRITICAL FIXES

### 1. **Bonus Stacking Control** ✅ FIXED
**Problem:** Components could accumulate excessive bonuses (up to 90+ points), compressing scores at the upper bound and reducing differentiation between good and excellent companies.

**Solution:**
- Implemented **maximum bonus caps** per component (typically +25-30 points)
- Each component now shows `MAX BONUS: +XX` in the Notes column
- Prevents artificial score inflation

**Example - Tier 1 Competitive Moat:**
```
v1.0: Base 50 + Network(25) + Scale(20) + Switching(20) + IP(15) + Reg(10) = 140 → Cap at 100
      (Always maxed out, no differentiation)

v2.0: Base 50 + MAX BONUS +30 → Maximum 80 points
      (Requires 2-3 strong moats to max out, better differentiation)
```

**Impact:** Better score distribution, more meaningful differences between companies

---

### 2. **Graduated Stop-Losses for All Tiers** ✅ NEW
**Problem:** Only Tier 4 had mandatory stop loss. Tier 1-3 positions vulnerable to severe drawdowns (potentially -60%+) while maintaining passing scores.

**Solution:**
- **Tier 1 (Mega-Cap):** -20% stop loss from entry
- **Tier 2 (Large-Cap):** -25% stop loss from entry
- **Tier 3 (Mid-Cap):** -30% stop loss from entry
- **Tier 4 (Small-Cap):** -40% stop loss from entry (unchanged)

**Implementation:**
- Auto-calculates stop price in Stock Information section
- Red-highlighted warning cell with stop price
- Formula: `Entry Price × (1 - Stop Loss %)`

**Example:**
```
Entry: $150.00
Tier 1 Stop: $120.00 (-20%)
Action: Immediate exit if price hits $120, regardless of score
```

**Rationale:** Higher-quality, lower-volatility stocks deserve tighter stops. Progressive structure aligns with risk levels.

---

### 3. **Management Execution - Improved Recency** ✅ UPDATED
**Problem:** 12-quarter (3-year) lookback too long to reflect current management effectiveness. All beats treated equally regardless of magnitude.

**Solution:**
- **Reduced to 8 quarters** (2 years) for more recent performance
- **Added magnitude weighting:** Average beat >5% earns +15 bonus
- **Maintained bonus cap:** Total bonuses limited to +25 points

**Scoring (Tier 1):**
```
v1.0:
  12Q Beat Rate >80% = 100 + M&A(10) + Buybacks(8) + Dividend(7) = 125 → Cap 100

v2.0:
  8Q Beat Rate >75% = 100 + Avg Beat >5%(15) + Smart M&A(10) = 125 → Cap 100
  Max Bonus: +25 points
```

**Impact:** Emphasizes recent track record and magnitude of beats, not just frequency.

---

### 4. **Customer Concentration - Enhanced Penalties** ✅ INCREASED
**Problem:** A company with 30% revenue from one customer faced only -20 penalty despite existential risk. Penalties too light relative to actual business risk.

**Solution - Significantly Increased:**

| Concentration | v1.0 Penalty | v2.0 Penalty | Change |
|---------------|--------------|--------------|--------|
| >50% single customer | -35 | **-45** | -10 pts |
| >40% | -30 | **-40** | -10 pts |
| >30% | -25 | **-35** | -10 pts |
| >20% | -20 | **-25** | -5 pts |

**Example Impact:**
```
Tier 2 Company: NRR 120% (base 90)
v1.0: 45% customer concentration → 90 - 30 = 60 points
v2.0: 45% customer concentration → 90 - 40 = 50 points
      (Could drop below tier minimum 65, triggering exit consideration)
```

**Rationale:** Concentration risk is existential and deserves severe scoring penalty.

---

## 🟡 MAJOR ENHANCEMENTS

### 5. **Sector Adjustment Framework** ✅ NEW
**Problem:** Sector-agnostic approach disadvantages certain industries. 35% gross margin for retailer vs 80% for SaaS compared unfairly.

**Solution:**
Added **Sector Modifier** section with manual adjustment:

| Sector | Adjustment | Rationale |
|--------|-----------|-----------|
| Tech/Software | +2 points | Structural advantages (high margins, scalability) |
| Healthcare | +1 point | Defensive characteristics, innovation premium |
| Industrials | 0 points | Baseline |
| Financials | -1 point | Leverage, regulatory constraints |
| Utilities | -2 points | Regulated, low growth |

**Usage:**
- User manually inputs sector modifier (0 by default)
- Applied to **Adjusted Composite Score**
- Documented in separate adjustment section

**Example:**
```
Software Company:
  Raw Composite: 82
  Sector Adj: +2
  Adjusted Composite: 84 → Strong Buy

Utility Company:
  Raw Composite: 82
  Sector Adj: -2
  Adjusted Composite: 80 → Strong Buy (but at threshold)
```

---

### 6. **Economic Cycle Adjustments** ✅ NEW
**Problem:** No macro overlay. Growth stocks score identically in rising/falling rate environments despite different performance drivers.

**Solution:**
Added **Economic Cycle Adjustment**:

| Cycle Phase | Adjustment | Application |
|-------------|-----------|-------------|
| Expansion | +1 point | Favor growth, momentum |
| Peak | 0 points | Neutral |
| Contraction | -1 point | Favor quality, defensives |
| Trough | 0 points | Neutral |

**Usage:**
- User manually sets based on macro view
- Applied to Adjusted Composite Score
- Re-evaluate quarterly

**Strategic Implications:**
```
Growth Stock (Tier 2) - Score 70:
  Expansion: 70 + 1 = 71 → Buy (aligned with cycle)
  Contraction: 70 - 1 = 69 → Hold (caution warranted)
```

---

### 7. **Alternative Risk Metrics - Max Drawdown Penalty** ✅ NEW
**Problem:** Position sizing relied solely on beta, ignoring company-specific risks, volatility clustering, and drawdown patterns.

**Solution:**
Added **Max Drawdown (1Y)** input with penalty factor in position sizing:

**Formula:**
```
Drawdown Penalty Factor = 1 + (Max DD % / 100) × 0.5

Example:
  Max DD = -30%
  Penalty = 1 + (30/100) × 0.5 = 1.15

Combined Risk Factor = Beta Adjustment × DD Penalty
```

**Position Sizing Impact:**
```
Tier 2 Stock, Score 85:
  Beta 1.5, Max DD -30%

v1.0:
  Beta Adj = 1 + (0.5 × 1.0) = 1.5
  Position = (7% × 0.85) / 1.5 = 4.0%

v2.0:
  Beta Adj = 1.5
  DD Penalty = 1.15
  Combined Risk = 1.5 × 1.15 = 1.725
  Position = (7% × 0.85) / 1.725 = 3.4%

Result: 15% position reduction due to drawdown history
```

**Rationale:** Stocks with severe drawdown history deserve smaller positions even if beta appears moderate.

---

### 8. **Burn Rate Penalties** ✅ ENHANCED
**Problem:** Growing burn rates not immediately penalized. Could maintain high scores while cash runway deteriorated.

**Solution:**
Immediate penalties applied to **Profitability Status / Profitability Path** components:

| Tier | Condition | Penalty |
|------|-----------|---------|
| Tier 1 | N/A (profitable only) | - |
| Tier 2 | Burn accelerating 20%+ | **-20 points** |
| Tier 3 | Burn accelerating 20%+ | **-25 points** |
| Tier 4 | Burn accelerating 20%+ | **-30 points** |

**Example - Tier 3:**
```
Profitability Path:
  Base: Path to profit in 18 months = 60 points
  Burn accelerating 25% QoQ: -25 penalty
  Final: 35 points (major red flag)

Impact on Quality Score (22% weight):
  Quality drops ~5 points → Could trigger exit consideration
```

---

## 🟢 STRUCTURAL IMPROVEMENTS

### 9. **New Stock Information Fields**
Added to all tiers:
- **Sector** - For sector adjustment application
- **Max Drawdown (1Y %)** - For enhanced position sizing
- **Stop Loss Price** - Auto-calculated with color highlighting

### 10. **Dual Composite Scores**
- **Raw Composite** - Pure formula result (unchanged from v1.0)
- **Adjusted Composite** - Includes sector and economic cycle adjustments
- **Rating based on Adjusted Composite**

### 11. **Enhanced Position Sizing Display**
New breakdown shows:
1. Beta Adjustment Factor
2. Drawdown Penalty Factor
3. Combined Risk Factor
4. Target Position %

User can see exactly how risk metrics affect position size.

---

## 📊 SCORING CHANGES SUMMARY

### Tier 1 (Mega-Cap) Changes
| Component | v1.0 Max Bonus | v2.0 Max Bonus | Change |
|-----------|----------------|----------------|--------|
| Competitive Moat | Unlimited (90+) | +30 | Capped |
| Management Execution | +25 (12Q) | +25 (8Q + magnitude) | Updated |
| Capital Allocation | +50 | +25 | Reduced |
| **Stop Loss** | **None** | **-20%** | **NEW** |

### Tier 2 (Large-Cap Growth) Changes
| Component | v1.0 Max Bonus | v2.0 Max Bonus | Change |
|-----------|----------------|----------------|--------|
| Customer Retention | +15 | +15, but Conc >30%=-35 | Penalty increased |
| Market Position | +80 | +30 | Capped |
| Moat Development | +75 | +30 | Capped |
| Growth Drivers | +60 | +25 | Capped |
| **Stop Loss** | **None** | **-25%** | **NEW** |

### Tier 3 (Mid-Cap) Changes
| Component | v1.0 Max Bonus | v2.0 Max Bonus | Change |
|-----------|----------------|----------------|--------|
| Customer Quality | +12, Conc >40%=-20 | +12, Conc >40%=-40 | Penalty doubled |
| Growth Acceleration | +Unlimited | +30 | Capped |
| Growth Drivers | +60 | +30 | Capped |
| Moat Formation | +75 | +30 | Capped |
| **Stop Loss** | **None** | **-30%** | **NEW** |

### Tier 4 (Small-Cap) Changes
| Component | v1.0 Max Bonus | v2.0 Max Bonus | Change |
|-----------|----------------|----------------|--------|
| Revenue Quality | +40, Conc >50%=-35 | +25, Conc >50%=-45 | Bonus cut, penalty up |
| Path to Profitability | No penalty | Burn accel=-30 | NEW penalty |
| Growth Consistency | +Unlimited | +30 | Capped |
| All other bonuses | Various | Capped at 20-30 | Standardized |
| Stop Loss | -40% | -40% | Unchanged |

---

## 🔄 MIGRATION GUIDE

### For Existing Holdings (scored with v1.0):
1. **Re-score using v2.0 templates** at next quarterly review
2. **Expect lower scores** due to bonus caps and enhanced penalties
3. **Set stop-loss alerts** for Tiers 1-3 (new requirement)
4. **Input Max Drawdown data** for accurate position sizing
5. **Apply sector adjustments** based on industry

### Score Expectations:
```
v1.0 Score → Expected v2.0 Score

Strong Buy (85+) → Likely 80-85 (still Strong Buy/Buy)
Buy (75-79) → Likely 70-75 (Buy/Hold)
Hold (65-69) → Likely 60-65 (Hold, watch closely)
Below Min → Likely below min (consider exit)

Individual results vary based on:
- Customer concentration
- Bonus stacking in v1.0
- Sector
- Drawdown history
```

### Actions After Re-scoring:
- **Score drops below min:** Begin 2-quarter watch (or exit if 2Q already)
- **Score 5-15 pts above min:** Reduce position to lower end of range
- **Stop loss hit:** Immediate exit regardless of score
- **Drift >10%:** Rebalance according to new target size

---

## 📈 IMPROVEMENTS BY STAKEHOLDER CONCERN

### Concern: "Bonus stacking compresses scores"
**Addressed by:**
- Component bonus caps (+25-30 max)
- Better score distribution across 60-100 range
- Meaningful differentiation between good/excellent companies

### Concern: "No downside protection for Tiers 1-3"
**Addressed by:**
- Graduated stop-losses for all tiers
- Auto-calculated stop prices
- Clear exit triggers independent of scores

### Concern: "Management metric too stale"
**Addressed by:**
- 8-quarter lookback (vs 12)
- Beat magnitude weighting
- Recent performance emphasized

### Concern: "Customer concentration penalties too light"
**Addressed by:**
- Penalties increased by 10-50%
- Can now trigger tier minimum failures
- Better reflects existential risk

### Concern: "Sector-agnostic unfair"
**Addressed by:**
- Sector adjustment framework
- +/-2 point range
- User-controlled, documented

### Concern: "Beta alone insufficient for risk"
**Addressed by:**
- Max Drawdown penalty factor
- Combined risk calculation
- Reduces positions for high-drawdown stocks

---

## 🚀 FUTURE ENHANCEMENTS (Documented, Not Yet Implemented)

### TAM Assessment Standardization
**Recommendation:** Create data source hierarchy
1. Industry research reports (Gartner, IDC, etc.)
2. Company investor presentations (use most conservative)
3. Proxy metrics (current revenue × penetration estimate)
4. Document source and assumptions in Notes

### Analyst Estimate Quality Adjustments
**Recommendation:** Track analyst accuracy
- Award bonus for consistently accurate analysts
- Penalize persistent optimists
- Adjust consensus by historical bias
- Manual tracking in separate worksheet

### Two-Quarter Rule Flexibility
**Recommendation:** Override provisions
- Document specific temporary factors (one-time charge, etc.)
- Require written justification
- Auto-expire after 1 quarter
- Use sparingly to maintain discipline

### Macro-Economic Overlays (Beyond Cycle Phase)
**Recommendation:** Additional factors
- Interest rate environment (rising/falling/stable)
- Sector rotation indicators
- Credit spread analysis
- Leading economic indicators
- Manual quarterly assessment

---

## 📁 FILE CHANGES

### New Files:
- `Tier1_MegaCap_v2.xlsx`
- `Tier2_LargeCap_v2.xlsx`
- `Tier3_MidCap_v2.xlsx`
- `Tier4_SmallCap_v2.xlsx`
- `generate_all_tiers_v2.py`
- `CHANGELOG_v2.md` (this file)

### Original Files (Preserved):
- `Tier1_MegaCap_Template.xlsx` (v1.0)
- `Tier2_LargeCap_Template.xlsx` (v1.0)
- `Tier3_MidCap_Template.xlsx` (v1.0)
- `Tier4_SmallCap_Template.xlsx` (v1.0)
- `Portfolio_Summary.xlsx` (compatible with both versions)
- `generate_all_tiers.py` (v1.0 generator)

**Note:** v1.0 files maintained for historical continuity and comparison.

---

## ⚠️ IMPORTANT NOTES

### Stop-Loss Discipline (NEW REQUIREMENT)
- **ALL TIERS** now require stop-loss alerts
- Stop loss **overrides** 2-quarter rule
- Price-based, not score-based
- Set alerts immediately upon entry
- Review stops quarterly (adjust for stock splits, dividends)

### Bonus Caps Enforcement
- User must manually enforce during scoring
- Notes column shows maximum allowed
- Example: "Base 50 + bonuses = 75, but MAX BONUS +30, so cap at 80"
- Critical for system integrity

### Sector/Cycle Adjustments Are Manual
- System provides framework, not automation
- User judgment required
- Document reasoning
- Re-evaluate quarterly
- Can be set to 0 if uncertain

### Enhanced Risk Sizing Is Optional
- Max Drawdown input not required
- If blank, defaults to beta-only sizing (v1.0 method)
- Recommended for all positions
- Use 1-year trailing max drawdown from entry date

---

## 📞 Questions & Feedback

For questions about v2.0 enhancements:
1. Review this changelog thoroughly
2. Compare v1.0 and v2.0 templates side-by-side
3. Test score a position in both versions
4. Note differences and validate against methodology

**Key Philosophy:**
v2.0 is more conservative, risk-aware, and disciplined than v1.0. Scores will generally be lower, but more accurate reflections of risk-adjusted opportunity. This is intentional and improves system robustness.

---

**Version:** 2.0
**Release Date:** October 31, 2025
**Status:** Production Ready
**Breaking Changes:** Yes (scoring methodology updates)
**Migration Required:** Yes (re-score all holdings)
