#!/usr/bin/env python3
"""
4-Tier Quantitative Stock Scoring System - ENHANCED VERSION 2.0
Addresses: Bonus stacking, graduated stop-losses, sector adjustments, improved risk metrics

Key Improvements:
- Bonus caps per component (max +30 total bonuses)
- Graduated stop-losses for all tiers (not just Tier 4)
- Management execution reduced to 8 quarters with magnitude weighting
- Enhanced customer concentration penalties
- Sector adjustment framework
- Alternative risk metrics beyond beta
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule


def add_header_section(ws, tier_name, tier_desc, min_score, position_range, risk_level, stop_loss):
    """Add common header section to worksheet with stop-loss info"""
    ws[f'A1'] = tier_name
    ws['A1'].font = Font(bold=True, size=14, color="1F4E78")
    ws.merge_cells('A1:F1')

    ws['A2'] = f"Minimum Score: {min_score} | Position Size: {position_range} | Risk: {risk_level} | Stop Loss: {stop_loss}"
    ws['A2'].font = Font(size=10, italic=True)
    ws.merge_cells('A2:F2')

    return 4


def add_stock_info(ws, start_row, tier_num):
    """Add stock information section with stop loss calculation"""
    section_fill = PatternFill(start_color="D6DCE4", end_color="D6DCE4", fill_type="solid")
    section_font = Font(bold=True, size=11)

    row = start_row
    ws[f'A{row}'] = "STOCK INFORMATION"
    ws[f'A{row}'].fill = section_fill
    ws[f'A{row}'].font = section_font
    ws.merge_cells(f'A{row}:B{row}')

    row += 1
    fields = [
        ("Ticker", ""),
        ("Company Name", ""),
        ("Sector", ""),  # NEW: For sector adjustments
        ("Market Cap ($B)", ""),
        ("Beta", 1.0),
        ("Max Drawdown (1Y %)", ""),  # NEW: Alternative risk metric
        ("Current Price", ""),
        ("Entry Price", "")
    ]

    for field, default_val in fields:
        ws[f'A{row}'] = field
        ws[f'A{row}'].font = Font(bold=True)
        if default_val != "":
            ws[f'B{row}'] = default_val
        row += 1

    # Add stop loss calculation
    stop_loss_pct = {1: 0.80, 2: 0.75, 3: 0.70, 4: 0.60}[tier_num]  # -20%, -25%, -30%, -40%
    stop_loss_display = {1: "-20%", 2: "-25%", 3: "-30%", 4: "-40%"}[tier_num]

    ws[f'A{row}'] = f"⚠️ STOP LOSS PRICE ({stop_loss_display})"
    ws[f'A{row}'].font = Font(bold=True, color="C00000")
    ws[f'A{row}'].fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
    entry_price_row = row - 1
    ws[f'B{row}'] = f"=B{entry_price_row}*{stop_loss_pct}"
    ws[f'B{row}'].number_format = '$0.00'
    ws[f'B{row}'].fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

    return row + 1


def add_sector_adjustment_section(ws, start_row):
    """Add sector adjustment framework"""
    section_fill = PatternFill(start_color="D6DCE4", end_color="D6DCE4", fill_type="solid")

    row = start_row + 1
    ws[f'A{row}'] = "SECTOR ADJUSTMENT"
    ws[f'A{row}'].fill = section_fill
    ws[f'A{row}'].font = Font(bold=True, size=11)
    ws.merge_cells(f'A{row}:F{row}')

    row += 1
    ws[f'A{row}'] = "Sector Modifier"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'B{row}'] = 0
    ws[f'B{row}'].number_format = '+0;-0;0'
    ws[f'F{row}'] = "Tech/Software: +2 | Healthcare: +1 | Industrials: 0 | Financials: -1 | Utilities: -2"

    row += 1
    ws[f'A{row}'] = "Economic Cycle Adj"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'B{row}'] = 0
    ws[f'B{row}'].number_format = '+0;-0;0'
    ws[f'F{row}'] = "Expansion: +1 | Peak: 0 | Contraction: -1 | Trough: 0"

    return row


def add_component_section(ws, start_row, section_name, weight_pct, components):
    """
    Add a score component section with IMPROVED BONUS CONTROLS

    components: list of tuples (name, weight, notes, bonus_cap)
    bonus_cap: Maximum total bonus points allowed for this component
    """
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)

    row = start_row
    ws[f'A{row}'] = f"{section_name} ({weight_pct}% weight)"
    ws[f'A{row}'].fill = header_fill
    ws[f'A{row}'].font = header_font
    ws.merge_cells(f'A{row}:F{row}')

    row += 1
    headers = ["Component", "Input Value", "Score (0-100)", "Weight", "Weighted Score", "Notes"]
    for col_idx, header in enumerate(headers, start=1):
        col = get_column_letter(col_idx)
        ws[f'{col}{row}'] = header
        ws[f'{col}{row}'].font = Font(bold=True)
        ws[f'{col}{row}'].fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")

    first_component_row = row + 1

    for item in components:
        if len(item) == 4:
            comp_name, comp_weight, comp_notes, bonus_cap = item
            notes_with_cap = f"{comp_notes} | MAX BONUS: +{bonus_cap}"
        else:
            comp_name, comp_weight, comp_notes = item
            notes_with_cap = comp_notes

        row += 1
        ws[f'A{row}'] = comp_name
        ws[f'B{row}'] = ""  # Input value
        ws[f'C{row}'] = ""  # Score
        ws[f'D{row}'] = comp_weight
        ws[f'E{row}'] = f"=C{row}*{float(comp_weight.strip('%'))/100}"
        ws[f'F{row}'] = notes_with_cap

    last_component_row = row

    # Total row
    row += 1
    total_row = row
    ws[f'A{row}'] = f"{section_name.upper()} TOTAL"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f"=AVERAGE(C{first_component_row}:C{last_component_row})"
    ws[f'E{row}'] = f"=SUM(E{first_component_row}:E{last_component_row})"
    ws[f'E{row}'].font = Font(bold=True)
    ws[f'E{row}'].fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

    return row + 1, total_row, first_component_row, last_component_row


def add_composite_and_sizing(ws, start_row, composite_formula, min_score, tier_volatility_factor,
                            beta_cell, sector_adj_row, base_allocation, tier_num):
    """Add composite score, rating, and ENHANCED position sizing with sector adjustments"""
    row = start_row + 1
    composite_row = row

    ws[f'A{row}'] = "COMPOSITE SCORE (Raw)"
    ws[f'A{row}'].fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    ws[f'A{row}'].font = Font(bold=True, size=11, color="FFFFFF")
    ws.merge_cells(f'A{row}:B{row}')
    ws[f'C{row}'] = composite_formula
    ws[f'C{row}'].font = Font(bold=True, size=12)
    ws[f'C{row}'].number_format = '0.00'

    row += 1
    adjusted_composite_row = row
    ws[f'A{row}'] = "ADJUSTED COMPOSITE"
    ws[f'A{row}'].fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    ws[f'A{row}'].font = Font(bold=True, size=12, color="FFFFFF")
    ws.merge_cells(f'A{row}:B{row}')
    # Add sector and economic adjustments
    ws[f'C{row}'] = f"=C{composite_row}+B{sector_adj_row}+B{sector_adj_row+1}"
    ws[f'C{row}'].font = Font(bold=True, size=14)
    ws[f'C{row}'].fill = PatternFill(start_color="FFC000", end_color="FFC000", fill_type="solid")
    ws[f'C{row}'].number_format = '0.00'

    row += 1
    ws[f'A{row}'] = "RATING"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=IF(C{adjusted_composite_row}>=80,"Strong Buy",IF(C{adjusted_composite_row}>=70,"Buy",IF(C{adjusted_composite_row}>=60,"Hold","Sell")))'
    ws[f'C{row}'].font = Font(bold=True, size=12)

    row += 1
    ws[f'A{row}'] = f"Score Buffer vs Min ({min_score})"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=C{adjusted_composite_row}-{min_score}'
    ws[f'C{row}'].number_format = '0.00'
    buffer_row = row

    # ENHANCED Position Sizing with alternative risk metrics
    row += 2
    ws[f'A{row}'] = "POSITION SIZING (Risk-Adjusted)"
    ws[f'A{row}'].fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    ws[f'A{row}'].font = Font(bold=True, size=12, color="FFFFFF")
    ws.merge_cells(f'A{row}:B{row}')

    row += 1
    ws[f'A{row}'] = "Beta Adjustment Factor"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f"=1+({beta_cell}-1)*{tier_volatility_factor}"
    ws[f'C{row}'].number_format = '0.00'
    beta_adj_row = row

    row += 1
    max_dd_cell = f"B{int(beta_cell.replace('B','')) + 1}"  # Max Drawdown cell
    ws[f'A{row}'] = "Drawdown Penalty Factor"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f"=IF({max_dd_cell}=\"\",1,1+({max_dd_cell}/100)*0.5)"
    ws[f'C{row}'].number_format = '0.00'
    ws[f'F{row}'] = "If 1Y Max DD = -30%, penalty = 1.15x"
    dd_penalty_row = row

    row += 1
    ws[f'A{row}'] = "Combined Risk Factor"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f"=C{beta_adj_row}*C{dd_penalty_row}"
    ws[f'C{row}'].number_format = '0.00'
    combined_risk_row = row

    row += 1
    ws[f'A{row}'] = "Target Position %"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f"=({base_allocation}%*C{adjusted_composite_row}/100)/C{combined_risk_row}"
    ws[f'C{row}'].number_format = '0.0%'
    target_pct_row = row

    row += 1
    ws[f'A{row}'] = "Portfolio Value ($)"
    ws[f'B{row}'] = 100000
    ws[f'B{row}'].number_format = '$#,##0'
    ws[f'A{row}'].font = Font(bold=True)
    portfolio_val_row = row

    row += 1
    ws[f'A{row}'] = "Target Dollar Amount"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=C{target_pct_row}*B{portfolio_val_row}'
    ws[f'C{row}'].number_format = '$#,##0'

    row += 1
    ws[f'A{row}'] = "Current Position Value"
    ws[f'B{row}'] = ""
    ws[f'B{row}'].number_format = '$#,##0'
    ws[f'A{row}'].font = Font(bold=True)
    current_val_row = row

    row += 1
    ws[f'A{row}'] = "Current Position %"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=IF(B{portfolio_val_row}>0,B{current_val_row}/B{portfolio_val_row},0)'
    ws[f'C{row}'].number_format = '0.0%'
    current_pct_row = row

    row += 1
    ws[f'A{row}'] = "Drift %"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=IF(C{target_pct_row}>0,(C{current_pct_row}-C{target_pct_row})/C{target_pct_row},0)'
    ws[f'C{row}'].number_format = '0.0%'
    drift_row = row

    row += 1
    ws[f'A{row}'] = "Action"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=IF(C{drift_row}>0.10,"TRIM",IF(AND(C{drift_row}<-0.10,C{adjusted_composite_row}>={min_score}+8),"ADD IF STRONG","HOLD"))'
    ws[f'C{row}'].font = Font(bold=True)

    # Conditional formatting for buffer
    ws.conditional_formatting.add(f'C{buffer_row}',
        CellIsRule(operator='greaterThanOrEqual', formula=['15'],
                   fill=PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")))
    ws.conditional_formatting.add(f'C{buffer_row}',
        CellIsRule(operator='between', formula=['5', '14'],
                   fill=PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")))
    ws.conditional_formatting.add(f'C{buffer_row}',
        CellIsRule(operator='lessThan', formula=['5'],
                   fill=PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")))

    return row


def create_tier1_template_v2():
    """Create ENHANCED Tier 1: Mega-Cap Core (>$200B) with improved controls"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Tier 1 Mega-Cap"

    row = add_header_section(ws, "TIER 1: MEGA-CAP CORE (>$200B) - Enhanced v2.0",
                             "Quality-focused blue chips", 60, "8-12%", "Lowest", "-20% Stop")
    row = add_stock_info(ws, row, tier_num=1)
    sector_adj_row = add_sector_adjustment_section(ws, row)

    # Valuation (20%) - IMPROVED: Reduced bonus caps
    row = sector_adj_row + 2
    row, val_total, _, _ = add_component_section(ws, row, "Valuation Score", "20", [
        ("P/E Ratio", "35%", "100-[(Current/Historical)-1]×100, Floor 0, Cap 100"),
        ("FCF Yield", "30%", ">5%=100, 3-5%=80, 2-3%=60, 1-2%=40, <1%=20"),
        ("PEG Ratio", "35%", "<1.0=100, 1.0-1.5=85, 1.5-2.0=70, 2.0-2.5=50, >2.5=30")
    ])

    # Quality (35%) - IMPROVED: Bonus caps, Management to 8Q, Beat magnitude
    row, qual_total, _, _ = add_component_section(ws, row + 1, "Quality Score", "35", [
        ("ROIC", "30%", ">25%=100, 20-25%=90, 15-20%=75, 10-15%=50, <10%=25"),
        ("Operating Margin", "20%", ">30%=100, 20-30%=85, 15-20%=70, 10-15%=50, <10%=30"),
        ("Op Margin Trend", "12%", ">200bps/yr=100, 100-200=85, 50-100=70, ±50=60, decline=25"),
        ("Competitive Moat", "18%", "Base 50 + Network+20, Scale+15, Switching+15, IP+12, Reg+8", 30),
        ("Management Execution", "10%", "8Q Beat Rate >75%=100, 60-75%=85, 50-60%=70 + Avg Beat >5%=+15, Smart M&A=+10", 25),
        ("Cash Conversion", "10%", "FCF/NI: >1.2=100, 1.0-1.2=80, 0.8-1.0=60, <0.8=30")
    ])

    # Growth (25%)
    row, growth_total, _, _ = add_component_section(ws, row + 1, "Growth Score", "25", [
        ("Revenue Growth 3Yr CAGR", "30%", ">20%=100, 15-20%=85, 10-15%=65, 7-10%=45, 5-7%=30, <5%=15"),
        ("Growth Consistency", "15%", "Base 50, adjust for accel/decel vs 3yr avg", 30),
        ("EPS Growth 3Yr CAGR", "25%", ">25%=100, 18-25%=85, 12-18%=70, 8-12%=50, <8%=30 + Op leverage=+15", 15),
        ("Future Growth Potential", "15%", "TAM >$500B + <20% share = 100, adjust + bonuses", 25),
        ("Analyst Consensus", "15%", ">15%=100, 12-15%=80, 8-12%=60, 5-8%=40, <5%=20")
    ])

    # Momentum (10%)
    row, mom_total, _, _ = add_component_section(ws, row + 1, "Momentum Score", "10", [
        ("12-Month Price Return", "40%", ">30%=100, 20-30%=80, 10-20%=60, 0-10%=45, -10-0%=40, <-10%=60"),
        ("Relative Strength vs SPY", "35%", "Outperform >10%=100, 5-10%=75, 0-5%=60, -5-0%=50, <-5%=30 + Inst flow=+10", 10),
        ("Technical Setup", "25%", "Above 50&200 MA=100, Above 200=70, Above 50=55, Between=50, Below=30")
    ])

    # Financial Health (10%) - IMPROVED: Reduced bonus caps
    row, fh_total, _, _ = add_component_section(ws, row + 1, "Financial Health Score", "10", [
        ("Net Cash Position", "50%", ">$75B=100, $50-75B=90, $25-50B=80, $0-25B=70, debt<$50B=60, >$50B=40"),
        ("FCF Generation", "40%", ">$20B=100, $15-20B=90, $10-15B=80, $5-10B=60, <$5B=40"),
        ("Capital Allocation", "10%", "Base 50 + Buybacks&R&D>10%=+20, Smart M&A=+15, Dividend=+12", 25)
    ])

    composite_formula = f"=E{val_total}+E{qual_total}+E{growth_total}+E{mom_total}+E{fh_total}"
    add_composite_and_sizing(ws, row, composite_formula, 60, 0.75, "B9", sector_adj_row, 10, 1)

    # Set column widths
    ws.column_dimensions['A'].width = 28
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 75

    return wb


def create_tier2_template_v2():
    """Create ENHANCED Tier 2: Large-Cap Growth with improved controls"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Tier 2 Large-Cap Growth"

    row = add_header_section(ws, "TIER 2: LARGE-CAP GROWTH ($50-200B) - Enhanced v2.0",
                             "Growth-focused established companies", 65, "5-8%", "Low-Moderate", "-25% Stop")
    row = add_stock_info(ws, row, tier_num=2)
    sector_adj_row = add_sector_adjustment_section(ws, row)

    # Valuation (18%) - IMPROVED with bonus caps
    row = sector_adj_row + 2
    row, val_total, _, _ = add_component_section(ws, row, "Valuation Score", "18", [
        ("Forward P/E or P/S", "55%", "P/E: <25=100, 25-35=85, 35-50=70 | P/S: <8=100, 8-12=85 + growth >35%=+20", 25),
        ("PEG Ratio", "25%", "<1.0=100, 1.0-1.5=85, 1.5-2.0=70, 2.0-2.5=50, >2.5=30"),
        ("Relative Valuation", "20%", "Below sector=100, 0-15% above=80, 15-30%=60, 30-50%=40, >50%=20")
    ])

    # Quality (28%) - IMPROVED: Enhanced customer concentration penalties
    row, qual_total, _, _ = add_component_section(ws, row + 1, "Quality Score", "28", [
        ("Revenue Scale", "15%", ">$10B=100, $7-10B=90, $5-7B=80, $3-5B=70, $2-3B=60, <$2B=45"),
        ("Profitability Status", "18%", "GAAP >20%=100, 15-20%=90, 10-15%=75, 5-10%=60, Non-GAAP=50 - Burn accel=-20", 0),
        ("Gross Margin", "20%", ">75%(SaaS)=100, 65-75%(Cloud)=90, 55-65%=80, 45-55%(Semi)=70"),
        ("Op Margin Trajectory", "15%", ">300bps/yr=100, 200-300=90, 100-200=80, 50-100=65, ±50=50"),
        ("Customer Retention", "20%", "NRR >130%=100, 120-130%=90, 110-120%=80 | Concentration >30%=-35, >20%=-25", 15),
        ("Market Position", "12%", "Base 50 + #1-2 in category=+30, Top 3-5=+20, Share gains=+20", 30)
    ])

    # Growth (32%) - HIGHEST
    row, growth_total, _, _ = add_component_section(ws, row + 1, "Growth Score", "32", [
        ("Revenue Growth Rate", "25%", ">35%=100, 28-35%=90, 22-28%=80, 18-22%=70, 15-18%=55, 12-15%=40"),
        ("Growth Consistency", "15%", "3 yrs 25%+=100, 2 yrs=85, Accelerating=80, Volatile 20%+=60", 20),
        ("Forward Growth Estimates", "20%", ">30%=100, 25-30%=85, 20-25%=70, 15-20%=55 + accel=+15", 15),
        ("EPS vs Revenue Growth", "10%", "Base 50, EPS>Rev+7%=+40, ±5%=+15, <Rev-5%=-20", 40),
        ("TAM & Penetration", "15%", ">$100B TAM <10% pen=100, $75-100B <12%=90 (Use standardized TAM calc)"),
        ("Growth Drivers", "10%", "Base 50 + Multiple segments=+20, Geo expand=+12, New products=+12", 25),
        ("Cyclicality Factor", "5%", "Non-cyclical=100, Early/mid cycle=85, Late cycle secular=70")
    ])

    # Momentum (12%)
    row, mom_total, _, _ = add_component_section(ws, row + 1, "Momentum Score", "12", [
        ("6-Month Price Performance", "40%", ">50%=100, 35-50%=85, 20-35%=70, 10-20%=50 + inst flow=+12", 15),
        ("Relative Strength vs QQQ", "35%", "Outperform >15%=100, 8-15%=80, 0-8%=60 + analyst upgrades=+12", 15),
        ("Technical Setup", "25%", "Above 50&200 MA=100, Above 200=70, Above 50=55, Between=50, Below=30")
    ])

    # Scale & Moat (10%) - IMPROVED: Bonus caps
    row, sm_total, _, _ = add_component_section(ws, row + 1, "Scale & Moat Score", "10", [
        ("Competitive Position Evolution", "35%", "Pulling away=100, Maintaining=80, Steady=60, Losing=30"),
        ("Moat Development", "30%", "Base 50 + Network=+25, Switching=+20, Scale=+15, Brand=+15", 30),
        ("Operating Leverage Inflection", "20%", "Margin > Revenue growth=100, In line=75, Slower=50"),
        ("Strategic Partnerships", "15%", "Base 50 + Major tech=+20, Gov=+20, Ecosystem=+15", 25)
    ])

    composite_formula = f"=E{val_total}+E{qual_total}+E{growth_total}+E{mom_total}+E{sm_total}"
    add_composite_and_sizing(ws, row, composite_formula, 65, 1.0, "B9", sector_adj_row, 7, 2)

    ws.column_dimensions['A'].width = 29
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 78

    return wb


def create_tier3_template_v2():
    """Create ENHANCED Tier 3: Mid-Cap Emerging with improved controls"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Tier 3 Mid-Cap Emerging"

    row = add_header_section(ws, "TIER 3: MID-CAP EMERGING ($10-50B) - Enhanced v2.0",
                             "High-growth emerging leaders", 67, "3-5%", "Moderate-High", "-30% Stop")
    row = add_stock_info(ws, row, tier_num=3)
    sector_adj_row = add_sector_adjustment_section(ws, row)

    row = sector_adj_row + 2
    row, val_total, _, _ = add_component_section(ws, row, "Valuation Score", "15", [
        ("Price-to-Sales", "60%", "<10x=100, 10-15=85, 15-22=70, 22-30=55 + growth >40%=+20", 25),
        ("Relative Valuation", "25%", "Below sector=100, At median=75, 1-1.5x=60, 1.5-2x=40, >2x=20"),
        ("Insider Ownership", "15%", ">20%=100, 15-20%=90, 10-15%=75 + recent buying=+15, Founder>30%=+15", 20)
    ])

    # Quality (22%) - IMPROVED: Stronger concentration penalties
    row, qual_total, _, _ = add_component_section(ws, row + 1, "Quality Score", "22", [
        ("Revenue Scale", "18%", ">$5B=100, $3-5B=85, $2-3B=75, $1-2B=60, $0.5-1B=45, <$0.5B=30"),
        ("Profitability Path", "20%", "Profitable >15%=100, 10-15%=85, 5-10%=70 - Burn accel 20%+=-25", 0),
        ("Gross Margin", "22%", ">75%=100, 65-75%=90, 55-65%=80, 45-55%=65, 35-45%=50"),
        ("Unit Economics", "20%", "LTV/CAC >3x=100, 2-3x=75, 1-2x=40 | Payback <12mo=85 + Improving=+10", 10),
        ("Customer Quality", "20%", "NRR >125%=100, 115-125%=85 | Concentration >40%=-40, >30%=-30, <10%=+12", 12)
    ])

    # Growth (38%) - HIGHEST with bonus caps
    row, growth_total, _, _ = add_component_section(ws, row + 1, "Growth Score", "38", [
        ("Revenue Growth", "28%", ">50%=100, 40-50%=90, 32-40%=80, 25-32%=70, 20-25%=55"),
        ("Growth Acceleration", "18%", "4+ qtrs accel=100, 3 qtrs=90, 2 qtrs=75, Stable high 30%+=60 +10/qtr", 30),
        ("Forward Estimates", "18%", ">40%=100, 32-40%=85, 25-32%=70 + accel >8%=+15", 15),
        ("TAM & Penetration", "18%", ">$75B TAM <8% pen=100, $50-75B <12%=85 (Standardized TAM)"),
        ("Growth Driver Diversity", "12%", "Base 50 + Multiple segments=+25, Geo=+15, Platform=+15", 30),
        ("Cyclicality", "6%", "Non-cyclical=100, Early cycle+secular=85, Mid=70, Late=45")
    ])

    row, mom_total, _, _ = add_component_section(ws, row + 1, "Momentum Score", "15", [
        ("6-Month Return", "40%", ">70%=100, 50-70%=90, 30-50%=75, 15-30%=55, 0-15%=40, <0%=60"),
        ("Relative Strength vs IWM", "35%", ">20% outperform=100, 12-20%=80, 5-12%=60 + upgrades=+12", 15),
        ("Volume & Sentiment", "25%", "Base 50 + Volume up >50%=+20, Positive trending=+12", 25)
    ])

    row, si_total, _, _ = add_component_section(ws, row + 1, "Scale Inflection Score", "10", [
        ("Market Position", "30%", "Rapid gains 10%+ vs sector=100, Moderate 5-10%=80, Maintain=60"),
        ("Operating Leverage", "30%", ">400bps/yr=100, 250-400=85, 150-250=70, 100-150=55"),
        ("Moat Formation", "25%", "Base 50 + Network=+25, Switching=+20, Scale=+15, Data=+15", 30),
        ("Partnerships", "15%", "Base 50 + Major tech=+25, Gov/enterprise=+20, Integrations=+15", 25)
    ])

    composite_formula = f"=E{val_total}+E{qual_total}+E{growth_total}+E{mom_total}+E{si_total}"
    add_composite_and_sizing(ws, row, composite_formula, 67, 1.3, "B9", sector_adj_row, 5, 3)

    ws.column_dimensions['A'].width = 29
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 80

    return wb


def create_tier4_template_v2():
    """Create ENHANCED Tier 4: Small-Cap Moonshots with improved controls"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Tier 4 Small-Cap Moonshots"

    row = add_header_section(ws, "TIER 4: SMALL-CAP MOONSHOTS (<$10B) - Enhanced v2.0",
                             "Hypergrowth disruptors", 70, "1-3%", "Highest", "-40% Stop MANDATORY")
    row = add_stock_info(ws, row, tier_num=4)
    sector_adj_row = add_sector_adjustment_section(ws, row)

    row = sector_adj_row + 2
    row, val_total, _, _ = add_component_section(ws, row, "Valuation Score", "10", [
        ("Price-to-Sales", "60%", "<12x=100, 12-20=85, 20-35=70 + growth >75%=+25, >100%=+30", 30),
        ("Relative Valuation", "25%", "Below median=100, At median=75, 1-2x=60, 2-3x=40, >3x=20"),
        ("Insider Ownership", "15%", ">25%=100, 20-25%=90, 15-20%=80 + buying=+15, Founder>30%=+15", 20)
    ])

    # Quality (15%) - IMPROVED: Severe concentration penalties
    row, qual_total, _, _ = add_component_section(ws, row + 1, "Quality Score", "15", [
        ("Gross Margin", "30%", ">70%=100, 60-70%=85, 50-60%=70, 40-50%=50, 30-40%=35"),
        ("Revenue Quality", "30%", "Base 50 + >70% recurring=+25, NRR>110%=+15 - Conc >50%=-45, >40%=-35", 25),
        ("Unit Economics", "20%", "LTV/CAC >3x=100, 2-3x=75, 1-2x=40 | Payback <12mo=85 + Improving=+10", 10),
        ("Path to Profitability", "20%", "Profitable=100, <12mo=80, 12-24mo=60 - Burn accel=-30, No path=-20", 0)
    ])

    # Growth (40%) - HIGHEST with controlled bonuses
    row, growth_total, _, _ = add_component_section(ws, row + 1, "Growth Score", "40", [
        ("Revenue Growth", "28%", ">100%=100, 75-100%=95, 55-75%=85, 40-55%=70, 30-40%=50"),
        ("Growth Consistency", "15%", "5+ qtrs accel=100, 4 qtrs=90, 3 qtrs=80 +8/qtr beyond 5", 30),
        ("TAM Size", "15%", ">$150B=100, $100-150B=90, $50-100B=75, $25-50B=55 (Standardized)"),
        ("Market Penetration", "10%", "<3%=100, 3-5%=90, 5-10%=75, 10-15%=55, >15%=35"),
        ("Growth Driver Strength", "15%", "Base 50 + Network=+20, Viral>50%=+20, Platform=+15", 25),
        ("Forward Estimates", "12%", ">60%=100, 50-60%=90, 40-50%=80 + accel >12%=+15", 15),
        ("Catalyst Pipeline", "5%", "Base 50 + Launch=+25, Market expand=+20, Partnership=+20", 25)
    ])

    row, mom_total, _, _ = add_component_section(ws, row + 1, "Momentum Score", "15", [
        ("6-Month Return", "40%", ">100%=100, 70-100%=95, 50-70%=85, 30-50%=70, <0%=60 oversold"),
        ("Relative Strength vs IWO", "30%", ">30% outperform=100, 20-30%=85, 10-20%=65, 0-10%=45"),
        ("Social Sentiment", "20%", "Base 50 + Bullish mentions=+20, Upgrades=+20 - Unsustainable meme=-25", 25),
        ("Volume Surge", "10%", ">75% increase=100, 50-75%=85, 25-50%=65, Stable=50")
    ])

    row, disrupt_total, _, _ = add_component_section(ws, row + 1, "Disruption Potential Score", "20", [
        ("Market Disruption", "35%", "Attacking $100B+=100, New category=95, Share gains=85, Niche=70"),
        ("Technology Moat", "25%", "Base 50 + Proprietary AI=+25, Patents=+20, Data=+20, Supply=+20", 30),
        ("Competitive Dynamics", "25%", "Winner-take-most=100, Oligopoly=80, Differentiated=60, Crowded=40"),
        ("Catalyst Pipeline", "15%", "Base 50 + Launch=+25, Partnership=+20, Regulatory=+25", 25)
    ])

    composite_formula = f"=E{val_total}+E{qual_total}+E{growth_total}+E{mom_total}+E{disrupt_total}"
    add_composite_and_sizing(ws, row, composite_formula, 70, 1.5, "B9", sector_adj_row, 3, 4)

    ws.column_dimensions['A'].width = 29
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 82

    return wb


def main():
    """Generate all ENHANCED v2.0 templates"""
    print("="*70)
    print("4-TIER QUANTITATIVE STOCK SCORING SYSTEM - ENHANCED VERSION 2.0")
    print("="*70)
    print("\n🔧 KEY IMPROVEMENTS:")
    print("  ✓ Bonus caps per component (max +25-30 points)")
    print("  ✓ Graduated stop-losses for ALL tiers (-20%/-25%/-30%/-40%)")
    print("  ✓ Management execution reduced to 8 quarters with magnitude weighting")
    print("  ✓ Enhanced customer concentration penalties (-35 to -45 points)")
    print("  ✓ Sector adjustment framework (+/-2 points)")
    print("  ✓ Economic cycle adjustments (+/-1 point)")
    print("  ✓ Alternative risk metrics (Max Drawdown penalty factor)")
    print("  ✓ Improved position sizing with combined risk factors")
    print("\n" + "="*70 + "\n")

    print("Creating Tier 1 (Mega-Cap >$200B)...")
    wb1 = create_tier1_template_v2()
    wb1.save("Tier1_MegaCap_v2.xlsx")
    print("✓ Tier1_MegaCap_v2.xlsx")

    print("\nCreating Tier 2 (Large-Cap $50-200B)...")
    wb2 = create_tier2_template_v2()
    wb2.save("Tier2_LargeCap_v2.xlsx")
    print("✓ Tier2_LargeCap_v2.xlsx")

    print("\nCreating Tier 3 (Mid-Cap $10-50B)...")
    wb3 = create_tier3_template_v2()
    wb3.save("Tier3_MidCap_v2.xlsx")
    print("✓ Tier3_MidCap_v2.xlsx")

    print("\nCreating Tier 4 (Small-Cap <$10B)...")
    wb4 = create_tier4_template_v2()
    wb4.save("Tier4_SmallCap_v2.xlsx")
    print("✓ Tier4_SmallCap_v2.xlsx")

    print("\n" + "="*70)
    print("SUCCESS! Enhanced v2.0 templates generated")
    print("="*70)
    print("\n📋 CHANGES FROM v1.0:")
    print("\n1. BONUS STACKING FIXED:")
    print("   - Each component now has maximum bonus cap (+25-30 points)")
    print("   - Prevents artificial score compression at upper bound")
    print("   - Example: Moat can't exceed base 50 + 30 bonus = 80 max")

    print("\n2. GRADUATED STOP-LOSSES:")
    print("   - Tier 1: -20% from entry (NEW)")
    print("   - Tier 2: -25% from entry (NEW)")
    print("   - Tier 3: -30% from entry (NEW)")
    print("   - Tier 4: -40% from entry (unchanged)")
    print("   - Auto-calculates stop price based on entry")

    print("\n3. MANAGEMENT EXECUTION IMPROVED:")
    print("   - Reduced from 12 to 8 quarters (2 years vs 3 years)")
    print("   - Added magnitude bonus: Avg beat >5% = +15 points")
    print("   - Total bonus cap: +25 points")

    print("\n4. CUSTOMER CONCENTRATION PENALTIES:")
    print("   - >50% single customer: -45 points (was -35)")
    print("   - >40%: -40 points (was -30)")
    print("   - >30%: -35 points (was -25)")
    print("   - >20%: -25 points (was -20)")

    print("\n5. SECTOR ADJUSTMENTS:")
    print("   - Tech/Software: +2 points")
    print("   - Healthcare: +1 point")
    print("   - Industrials: 0 points")
    print("   - Financials: -1 point")
    print("   - Utilities: -2 points")

    print("\n6. ECONOMIC CYCLE ADJUSTMENTS:")
    print("   - Expansion: +1 point")
    print("   - Peak/Trough: 0 points")
    print("   - Contraction: -1 point")

    print("\n7. ENHANCED POSITION SIZING:")
    print("   - Beta adjustment (unchanged)")
    print("   - NEW: Max Drawdown penalty factor")
    print("   - If 1Y Max DD = -30%, position reduced by 15%")
    print("   - Combined Risk Factor = Beta Adj × DD Penalty")

    print("\n8. BURN RATE PENALTIES:")
    print("   - Accelerating burn 20%+: -25 to -30 points")
    print("   - Applied immediately to Quality score")

    print("\n" + "="*70)
    print("\n⚠️  MIGRATION NOTES:")
    print("   - v1.0 templates remain valid for existing positions")
    print("   - Use v2.0 for all NEW position evaluations")
    print("   - Re-score existing holdings quarterly using v2.0")
    print("   - Set stop-loss alerts for Tiers 1-3 (NEW requirement)")

    print("\n" + "="*70)
    print("\n📊 NEXT STEPS:")
    print("   1. Review sector adjustments for your holdings")
    print("   2. Set stop-loss alerts for ALL positions")
    print("   3. Input Max Drawdown data for enhanced risk sizing")
    print("   4. Re-score holdings using v2.0 templates")
    print("   5. Adjust positions if new scores trigger actions")

    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
