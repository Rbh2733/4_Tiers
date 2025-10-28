# Quick Reference Guide
## 4-Tier Quantitative Stock Scoring System

### 🎯 Which Tier for My Stock?

| Market Cap | Tier | File | Min Score | Position |
|------------|------|------|-----------|----------|
| >$200B | Tier 1 | Tier1_MegaCap_Template.xlsx | 60 | 8-12% |
| $50-200B | Tier 2 | Tier2_LargeCap_Template.xlsx | 65 | 5-8% |
| $10-50B | Tier 3 | Tier3_MidCap_Template.xlsx | 67 | 3-5% |
| <$10B | Tier 4 | Tier4_SmallCap_Template.xlsx | 70 | 1-3% |

### 📊 What Each Tier Emphasizes

**Tier 1 - Quality First** (35% weight)
- Best for: Stable blue chips
- Look for: High ROIC (>25%), strong moats, consistent margins

**Tier 2 - Balanced Growth** (32% weight)
- Best for: Established growth companies
- Look for: 25%+ revenue growth, NRR >120%, expanding margins

**Tier 3 - High Growth** (38% weight)
- Best for: Emerging category leaders
- Look for: 35%+ growth, huge TAM (>$75B), <10% penetration

**Tier 4 - Hypergrowth** (40% weight)
- Best for: Disruptive moonshots
- Look for: 75%+ growth, category creation, massive TAM
- ⚠️ **MANDATORY -40% stop loss**

### 🎯 Composite Formula by Tier

```
Tier 1: V(20%) + Q(35%) + G(25%) + M(10%) + FH(10%)
Tier 2: V(18%) + Q(28%) + G(32%) + M(12%) + SM(10%)
Tier 3: V(15%) + Q(22%) + G(38%) + M(15%) + SI(10%)
Tier 4: V(10%) + Q(15%) + G(40%) + M(15%) + D(20%)
```

### 📈 Rating Scale (All Tiers)

| Score | Rating | Action |
|-------|--------|--------|
| 80-100 | Strong Buy | Maximum position size |
| 70-79 | Buy | Good entry point |
| 60-69 | Hold | Monitor closely |
| <60 | Sell | Exit position |

### 🚨 Exit Rules

**2-Quarter Rule (All Tiers)**
```
IF score < tier minimum for 2 consecutive quarters → EXIT
```

**Stop Loss (Tier 4 ONLY)**
```
IF price drops 40% from entry → IMMEDIATE EXIT
Example: Entry $10.00 → Exit at $6.00
```

### 🔢 Position Sizing Quick Reference

**At Minimum Score:**
- Tier 1 @ 60: ~5.6% position (Beta 1.1)
- Tier 2 @ 65: ~3.0% position (Beta 1.5)
- Tier 3 @ 67: ~1.6% position (Beta 1.8)
- Tier 4 @ 70: ~0.7% position (Beta 2.3)

**At High Score (85-90):**
- Tier 1: 8-10% position
- Tier 2: 5-6% position
- Tier 3: 3-4% position
- Tier 4: 1.5-2.5% position

### 📊 Key Metrics by Tier

#### Tier 1 (Mega-Cap) - Must Haves
- ✅ ROIC >20%
- ✅ Operating Margin >25%
- ✅ Revenue Growth >10%
- ✅ Strong competitive moat
- ✅ Positive FCF >$15B

#### Tier 2 (Large-Cap) - Must Haves
- ✅ Revenue Growth >20%
- ✅ NRR >110% (if SaaS)
- ✅ Gross Margin >60%
- ✅ Expanding operating margins
- ✅ Clear path to profitability (if not yet profitable)

#### Tier 3 (Mid-Cap) - Must Haves
- ✅ Revenue Growth >30%
- ✅ TAM >$50B with <15% penetration
- ✅ Gross Margin >55%
- ✅ LTV/CAC >2x
- ✅ Multiple growth drivers

#### Tier 4 (Small-Cap) - Must Haves
- ✅ Revenue Growth >75%
- ✅ TAM >$100B with <5% penetration
- ✅ Disruptive technology/business model
- ✅ Strong insider ownership (>20%)
- ✅ Clear catalysts in next 6 months

### 🎨 Score Buffer Colors

**In Excel Templates:**
- 🟢 Green (≥15 buffer): Excellent, well above minimum
- 🟡 Yellow (5-14 buffer): Adequate, monitor
- 🔴 Red (<5 buffer): Warning, approaching minimum

### 🔄 Rebalancing Triggers

| Drift % | Action | Condition |
|---------|--------|-----------|
| >+10% | TRIM | Quarterly review |
| >-10% | ADD | If score ≥ min + 8 |
| ±5-10% | HOLD | Within tolerance |

### 📍 Benchmark by Tier

- Tier 1: SPY (S&P 500)
- Tier 2: QQQ (NASDAQ-100)
- Tier 3: IWM (Russell 2000)
- Tier 4: IWO (Russell 2000 Growth)

### 🔢 Portfolio Allocation Targets

**Ideal Allocation:**
```
Tier 1: 40-50% (Core holdings)
Tier 2: 25-35% (Growth engine)
Tier 3: 12-20% (Emerging leaders)
Tier 4: 5-10%  (Moonshots)
Cash:   5-10%  (Opportunities)
```

### 📝 How to Use

1. **Choose Tier** based on market cap
2. **Open Template** for that tier
3. **Enter Stock Data** in white cells (Column B)
4. **Calculate Scores** using brackets in Column F
5. **Review Composite** - Auto-calculates
6. **Check Rating** - Strong Buy/Buy/Hold/Sell
7. **Note Position Size** - Volatility-adjusted
8. **Add to Portfolio Summary** - Track across all holdings

### ⚠️ Common Mistakes

❌ Using wrong tier (check market cap first!)
❌ Forgetting Tier 4 stop loss
❌ Not updating scores quarterly
❌ Ignoring the 2-quarter rule
❌ Over-allocating to high scores in small-caps
❌ Mixing up benchmarks (each tier has its own)

### 🚀 Pro Tips

✅ **Update quarterly** after earnings
✅ **Document reasoning** in Notes column
✅ **Track score history** for 2-quarter rule
✅ **Use Portfolio Summary** to see big picture
✅ **Respect position sizes** (don't go over limits)
✅ **Set alerts** for Tier 4 stop losses
✅ **Rebalance quarterly** (don't let winners run too much)

### 📊 Example Scores

**Strong Mega-Cap (MSFT - Tier 1)**
```
Valuation: 85  (reasonable P/E, great FCF)
Quality: 95    (excellent ROIC, margins, moat)
Growth: 68     (steady but not explosive)
Momentum: 82   (strong performance)
Fin Health: 98 (fortress balance sheet)
COMPOSITE: 88  → Strong Buy @ 8% position
```

**Hypergrowth Small-Cap (RKLB - Tier 4)**
```
Valuation: 75  (high P/S but justified by growth)
Quality: 65    (improving but not there yet)
Growth: 95     (explosive 80%+ growth)
Momentum: 88   (strong uptrend)
Disruption: 90 (attacking $300B+ market)
COMPOSITE: 85  → Strong Buy @ 2% position
⚠️ Stop Loss: -40% from entry
```

---

## 📞 Need Help?

1. Check the full **README.md** for detailed explanations
2. Review **Column F (Notes)** in Excel templates for scoring brackets
3. Use **Portfolio_Summary.xlsx** to track all positions
4. Verify you're using correct tier for market cap

---

**Remember:** This is a systematic approach to stock analysis, not a guarantee of returns. Always do additional due diligence and consult financial advisors before investing.
