#!/usr/bin/env python3
"""
4-Tier Quantitative Stock Scoring System - Complete Excel Template Generator
Generates Excel workbooks for all 4 tiers with pre-configured formulas
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule


def add_header_section(ws, tier_name, tier_desc, min_score, position_range, risk_level):
    """Add common header section to worksheet"""
    ws[f'A1'] = tier_name
    ws['A1'].font = Font(bold=True, size=14, color="1F4E78")
    ws.merge_cells('A1:F1')

    ws['A2'] = f"Minimum Score: {min_score} | Position Size: {position_range} | Risk: {risk_level}"
    ws['A2'].font = Font(size=10, italic=True)
    ws.merge_cells('A2:F2')

    return 4


def add_stock_info(ws, start_row):
    """Add stock information section"""
    section_fill = PatternFill(start_color="D6DCE4", end_color="D6DCE4", fill_type="solid")
    section_font = Font(bold=True, size=11)

    row = start_row
    ws[f'A{row}'] = "STOCK INFORMATION"
    ws[f'A{row}'].fill = section_fill
    ws[f'A{row}'].font = section_font
    ws.merge_cells(f'A{row}:B{row}')

    row += 1
    fields = ["Ticker", "Company Name", "Market Cap ($B)", "Beta", "Current Price", "Entry Price"]
    for field in fields:
        ws[f'A{row}'] = field
        ws[f'A{row}'].font = Font(bold=True)
        if field == "Beta":
            ws[f'B{row}'] = 1.0
        row += 1

    return row


def add_component_section(ws, start_row, section_name, weight_pct, components):
    """
    Add a score component section with multiple sub-components

    components: list of tuples (name, weight, notes)
    Returns: (last_row, total_row, first_component_row, last_component_row)
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

    for comp_name, comp_weight, comp_notes in components:
        row += 1
        ws[f'A{row}'] = comp_name
        ws[f'B{row}'] = ""  # Input value
        ws[f'C{row}'] = ""  # Score
        ws[f'D{row}'] = comp_weight
        ws[f'E{row}'] = f"=C{row}*{float(comp_weight.strip('%'))/100}"
        ws[f'F{row}'] = comp_notes

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


def add_composite_and_sizing(ws, start_row, composite_formula, min_score, tier_volatility_factor, beta_cell):
    """Add composite score, rating, and position sizing"""
    row = start_row + 1
    composite_row = row

    ws[f'A{row}'] = "COMPOSITE SCORE"
    ws[f'A{row}'].fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    ws[f'A{row}'].font = Font(bold=True, size=12, color="FFFFFF")
    ws.merge_cells(f'A{row}:B{row}')
    ws[f'C{row}'] = composite_formula
    ws[f'C{row}'].font = Font(bold=True, size=14)
    ws[f'C{row}'].fill = PatternFill(start_color="FFC000", end_color="FFC000", fill_type="solid")
    ws[f'C{row}'].number_format = '0.00'

    row += 1
    ws[f'A{row}'] = "RATING"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=IF(C{composite_row}>=80,"Strong Buy",IF(C{composite_row}>=70,"Buy",IF(C{composite_row}>=60,"Hold","Sell")))'
    ws[f'C{row}'].font = Font(bold=True, size=12)

    row += 1
    ws[f'A{row}'] = f"Score Buffer vs Min ({min_score})"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=C{composite_row}-{min_score}'
    ws[f'C{row}'].number_format = '0.00'
    buffer_row = row

    # Position Sizing
    row += 2
    ws[f'A{row}'] = "POSITION SIZING"
    ws[f'A{row}'].fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    ws[f'A{row}'].font = Font(bold=True, size=12, color="FFFFFF")
    ws.merge_cells(f'A{row}:B{row}')

    base_allocation = {"0.75": 10, "1.0": 7, "1.3": 5, "1.5": 3}[str(tier_volatility_factor)]

    row += 1
    ws[f'A{row}'] = "Target Position %"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=({base_allocation}%*C{composite_row}/100)/(1+({beta_cell}-1)*{tier_volatility_factor})'
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
    ws[f'C{row}'] = f'=IF(C{drift_row}>0.10,"TRIM",IF(AND(C{drift_row}<-0.10,C{composite_row}>={min_score}+8),"ADD IF STRONG","HOLD"))'
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


def create_tier1_template():
    """Create Tier 1: Mega-Cap Core (>$200B)"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Tier 1 Mega-Cap"

    row = add_header_section(ws, "TIER 1: MEGA-CAP CORE (>$200B)",
                             "Quality-focused blue chips", 60, "8-12%", "Lowest")
    row = add_stock_info(ws, row)

    # Valuation (20%)
    row, val_total, _, _ = add_component_section(ws, row + 1, "Valuation Score", "20", [
        ("P/E Ratio", "35%", "100-[(Current/Historical)-1]×100, Floor 0, Cap 100"),
        ("FCF Yield", "30%", ">5%=100, 3-5%=80, 2-3%=60, 1-2%=40, <1%=20"),
        ("PEG Ratio", "35%", "<1.0=100, 1.0-1.5=85, 1.5-2.0=70, 2.0-2.5=50, >2.5=30")
    ])

    # Quality (35%) - HIGHEST
    row, qual_total, _, _ = add_component_section(ws, row + 1, "Quality Score", "35", [
        ("ROIC", "30%", ">25%=100, 20-25%=90, 15-20%=75, 10-15%=50, <10%=25"),
        ("Operating Margin", "20%", ">30%=100, 20-30%=85, 15-20%=70, 10-15%=50, <10%=30"),
        ("Op Margin Trend", "12%", ">200bps/yr=100, 100-200=85, 50-100=70, ±50=60, decline=25"),
        ("Competitive Moat", "18%", "Base 50 + Network+25, Scale+20, Switching+20, IP+15, Reg+10"),
        ("Management Execution", "10%", "Beat rate >80%=100, 70-80%=85, 60-70%=70, <60%=50 + bonuses"),
        ("Cash Conversion", "10%", "FCF/NI: >1.2=100, 1.0-1.2=80, 0.8-1.0=60, <0.8=30")
    ])

    # Growth (25%)
    row, growth_total, _, _ = add_component_section(ws, row + 1, "Growth Score", "25", [
        ("Revenue Growth 3Yr CAGR", "30%", ">20%=100, 15-20%=85, 10-15%=65, 7-10%=45, 5-7%=30, <5%=15"),
        ("Growth Consistency", "15%", "Base 50, adjust for accel/decel vs 3yr avg"),
        ("EPS Growth 3Yr CAGR", "25%", ">25%=100, 18-25%=85, 12-18%=70, 8-12%=50, <8%=30"),
        ("Future Growth Potential", "15%", "TAM >$500B + <20% share = 100, adjust + bonuses"),
        ("Analyst Consensus", "15%", ">15%=100, 12-15%=80, 8-12%=60, 5-8%=40, <5%=20")
    ])

    # Momentum (10%)
    row, mom_total, _, _ = add_component_section(ws, row + 1, "Momentum Score", "10", [
        ("12-Month Price Return", "40%", ">30%=100, 20-30%=80, 10-20%=60, 0-10%=45, -10-0%=40, <-10%=60"),
        ("Relative Strength vs SPY", "35%", "Outperform >10%=100, 5-10%=75, 0-5%=60, -5-0%=50, <-5%=30"),
        ("Technical Setup", "25%", "Above 50&200 MA=100, Above 200=70, Above 50=55, Between=50, Below=30")
    ])

    # Financial Health (10%)
    row, fh_total, _, _ = add_component_section(ws, row + 1, "Financial Health Score", "10", [
        ("Net Cash Position", "50%", ">$75B=100, $50-75B=90, $25-50B=80, $0-25B=70, debt<$50B=60, >$50B=40"),
        ("FCF Generation", "40%", ">$20B=100, $15-20B=90, $10-15B=80, $5-10B=60, <$5B=40"),
        ("Capital Allocation", "10%", "Base 50 + Buybacks&R&D>10%=+25, M&A=+20, Dividend=+15")
    ])

    composite_formula = f"=E{val_total}+E{qual_total}+E{growth_total}+E{mom_total}+E{fh_total}"
    add_composite_and_sizing(ws, row, composite_formula, 60, 0.75, "B9")

    # Set column widths
    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 65

    return wb


def create_tier2_template():
    """Create Tier 2: Large-Cap Growth ($50-200B)"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Tier 2 Large-Cap Growth"

    row = add_header_section(ws, "TIER 2: LARGE-CAP GROWTH ($50-200B)",
                             "Growth-focused established companies", 65, "5-8%", "Low-Moderate")
    row = add_stock_info(ws, row)

    # Valuation (18%)
    row, val_total, _, _ = add_component_section(ws, row + 1, "Valuation Score", "18", [
        ("Forward P/E or P/S", "55%", "P/E: <25=100, 25-35=85, 35-50=70, 50-70=50, >70=35 | P/S: <8=100, 8-12=85, 12-18=70, 18-25=50 + growth bonuses"),
        ("PEG Ratio", "25%", "<1.0=100, 1.0-1.5=85, 1.5-2.0=70, 2.0-2.5=50, >2.5=30"),
        ("Relative Valuation", "20%", "Below sector=100, 0-15% above=80, 15-30%=60, 30-50%=40, >50%=20")
    ])

    # Quality (28%)
    row, qual_total, _, _ = add_component_section(ws, row + 1, "Quality Score", "28", [
        ("Revenue Scale", "15%", ">$10B=100, $7-10B=90, $5-7B=80, $3-5B=70, $2-3B=60, <$2B=45"),
        ("Profitability Status", "18%", "GAAP >20%=100, 15-20%=90, 10-15%=75, 5-10%=60, Non-GAAP=50"),
        ("Gross Margin", "20%", ">75%(SaaS)=100, 65-75%(Cloud)=90, 55-65%=80, 45-55%(Semi)=70"),
        ("Op Margin Trajectory", "15%", ">300bps/yr=100, 200-300=90, 100-200=80, 50-100=65, ±50=50"),
        ("Customer Retention", "20%", "NRR >130%=100, 120-130%=90, 110-120%=80, 100-110%=65 | Non-SaaS: use best metric"),
        ("Market Position", "12%", "Base 50 + #1-2 in category=+35, Top 3-5=+25, Share gains=+25")
    ])

    # Growth (32%) - HIGHEST
    row, growth_total, _, _ = add_component_section(ws, row + 1, "Growth Score", "32", [
        ("Revenue Growth Rate", "25%", ">35%=100, 28-35%=90, 22-28%=80, 18-22%=70, 15-18%=55, 12-15%=40"),
        ("Growth Consistency", "15%", "3 yrs 25%+=100, 2 yrs=85, Accelerating=80, Volatile 20%+=60"),
        ("Forward Growth Estimates", "20%", ">30%=100, 25-30%=85, 20-25%=70, 15-20%=55 + accel bonus"),
        ("EPS vs Revenue Growth", "10%", "Base 50, EPS>Rev+7%=+50, ±5%=+20, <Rev-5%=-20"),
        ("TAM & Penetration", "15%", ">$100B TAM <10% pen=100, $75-100B <12%=90, adjust down"),
        ("Growth Drivers", "10%", "Base 50 + Multiple segments=+25, Geo expand=+15, New products=+15"),
        ("Cyclicality Factor", "5%", "Non-cyclical=100, Early/mid cycle=85, Late cycle secular=70")
    ])

    # Momentum (12%)
    row, mom_total, _, _ = add_component_section(ws, row + 1, "Momentum Score", "12", [
        ("6-Month Price Performance", "40%", ">50%=100, 35-50%=85, 20-35%=70, 10-20%=50 + inst flow bonuses"),
        ("Relative Strength vs QQQ", "35%", "Outperform >15%=100, 8-15%=80, 0-8%=60 + analyst bonuses"),
        ("Technical Setup", "25%", "Above 50&200 MA=100, Above 200=70, Above 50=55, Between=50, Below=30")
    ])

    # Scale & Moat (10%)
    row, sm_total, _, _ = add_component_section(ws, row + 1, "Scale & Moat Score", "10", [
        ("Competitive Position Evolution", "35%", "Pulling away=100, Maintaining=80, Steady=60, Losing=30"),
        ("Moat Development", "30%", "Base 50 + Network=+30, Switching=+25, Scale=+20, Brand=+20"),
        ("Operating Leverage Inflection", "20%", "Margin > Revenue growth=100, In line=75, Slower=50"),
        ("Strategic Partnerships", "15%", "Base 50 + Major tech=+25, Gov=+25, Ecosystem=+20")
    ])

    composite_formula = f"=E{val_total}+E{qual_total}+E{growth_total}+E{mom_total}+E{sm_total}"
    add_composite_and_sizing(ws, row, composite_formula, 65, 1.0, "B9")

    # Set column widths
    ws.column_dimensions['A'].width = 27
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 70

    return wb


def create_tier3_template():
    """Create Tier 3: Mid-Cap Emerging ($10-50B)"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Tier 3 Mid-Cap Emerging"

    row = add_header_section(ws, "TIER 3: MID-CAP EMERGING ($10-50B)",
                             "High-growth emerging leaders", 67, "3-5%", "Moderate-High")
    row = add_stock_info(ws, row)

    # Valuation (15%)
    row, val_total, _, _ = add_component_section(ws, row + 1, "Valuation Score", "15", [
        ("Price-to-Sales", "60%", "<10x=100, 10-15=85, 15-22=70, 22-30=55, 30-40=40 + growth bonuses"),
        ("Relative Valuation", "25%", "Below sector=100, At median=75, 1-1.5x=60, 1.5-2x=40, >2x=20"),
        ("Insider Ownership", "15%", ">20%=100, 15-20%=90, 10-15%=75 + recent buying=+20")
    ])

    # Quality (22%)
    row, qual_total, _, _ = add_component_section(ws, row + 1, "Quality Score", "22", [
        ("Revenue Scale", "18%", ">$5B=100, $3-5B=85, $2-3B=75, $1-2B=60, $0.5-1B=45, <$0.5B=30"),
        ("Profitability Path", "20%", "Profitable >15%=100, 10-15%=85, 5-10%=70, Path <12mo=50"),
        ("Gross Margin", "22%", ">75%=100, 65-75%=90, 55-65%=80, 45-55%=65, 35-45%=50"),
        ("Unit Economics", "20%", "LTV/CAC >3x=100, 2-3x=75, 1-2x=40 | Payback <12mo=85"),
        ("Customer Quality", "20%", "NRR >125%=100, 115-125%=85, 105-115%=70 | Non-SaaS: best metric")
    ])

    # Growth (38%) - HIGHEST
    row, growth_total, _, _ = add_component_section(ws, row + 1, "Growth Score", "38", [
        ("Revenue Growth", "28%", ">50%=100, 40-50%=90, 32-40%=80, 25-32%=70, 20-25%=55"),
        ("Growth Acceleration", "18%", "4+ qtrs accel=100, 3 qtrs=90, 2 qtrs=75, Stable high 30%+=60"),
        ("Forward Estimates", "18%", ">40%=100, 32-40%=85, 25-32%=70 + accel >8%=+20"),
        ("TAM & Penetration", "18%", ">$75B TAM <8% pen=100, $50-75B <12%=85, adjust down"),
        ("Growth Driver Diversity", "12%", "Base 50 + Multiple segments=+30, Geo=+20, Platform=+20"),
        ("Cyclicality", "6%", "Non-cyclical=100, Early cycle+secular=85, Mid=70, Late=45")
    ])

    # Momentum (15%)
    row, mom_total, _, _ = add_component_section(ws, row + 1, "Momentum Score", "15", [
        ("6-Month Return", "40%", ">70%=100, 50-70%=90, 30-50%=75, 15-30%=55, 0-15%=40, <0%=60"),
        ("Relative Strength vs IWM", "35%", ">20% outperform=100, 12-20%=80, 5-12%=60 + upgrades"),
        ("Volume & Sentiment", "25%", "Base 50 + Volume up >50%=+25, Positive trending=+15")
    ])

    # Scale Inflection (10%)
    row, si_total, _, _ = add_component_section(ws, row + 1, "Scale Inflection Score", "10", [
        ("Market Position", "30%", "Rapid gains 10%+ vs sector=100, Moderate 5-10%=80, Maintain=60"),
        ("Operating Leverage", "30%", ">400bps/yr=100, 250-400=85, 150-250=70, 100-150=55"),
        ("Moat Formation", "25%", "Base 50 + Network=+30, Switching=+25, Scale=+20, Data=+20"),
        ("Partnerships", "15%", "Base 50 + Major tech=+30, Gov/enterprise=+25, Integrations=+20")
    ])

    composite_formula = f"=E{val_total}+E{qual_total}+E{growth_total}+E{mom_total}+E{si_total}"
    add_composite_and_sizing(ws, row, composite_formula, 67, 1.3, "B9")

    # Set column widths
    ws.column_dimensions['A'].width = 27
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 72

    return wb


def create_tier4_template():
    """Create Tier 4: Small-Cap Moonshots (<$10B)"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Tier 4 Small-Cap Moonshots"

    row = add_header_section(ws, "TIER 4: SMALL-CAP MOONSHOTS (<$10B)",
                             "Hypergrowth disruptors - MANDATORY -40% STOP LOSS", 70, "1-3%", "Highest")
    row = add_stock_info(ws, row)

    # Add stop loss warning
    ws[f'A{row}'] = "⚠️ STOP LOSS: -40% from entry (MANDATORY)"
    ws[f'A{row}'].font = Font(bold=True, size=11, color="C00000")
    ws[f'A{row}'].fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
    ws.merge_cells(f'A{row}:F{row}')
    row += 1
    ws[f'A{row}'] = "Stop Loss Price"
    ws[f'B{row}'] = "=B10*0.6"
    ws[f'B{row}'].number_format = '$0.00'
    ws[f'A{row}'].font = Font(bold=True)

    # Valuation (10%)
    row, val_total, _, _ = add_component_section(ws, row + 1, "Valuation Score", "10", [
        ("Price-to-Sales", "60%", "<12x=100, 12-20=85, 20-35=70, 35-50=50 + hypergrowth bonuses"),
        ("Relative Valuation", "25%", "Below median=100, At median=75, 1-2x=60, 2-3x=40, >3x=20"),
        ("Insider Ownership", "15%", ">25%=100, 20-25%=90, 15-20%=80 + buying=+20, Founder >30%=+20")
    ])

    # Quality (15%)
    row, qual_total, _, _ = add_component_section(ws, row + 1, "Quality Score", "15", [
        ("Gross Margin", "30%", ">70%=100, 60-70%=85, 50-60%=70, 40-50%=50, 30-40%=35"),
        ("Revenue Quality", "30%", "Base 50 + >70% recurring=+30, NRR>110%=+20, Low concentration=+15"),
        ("Unit Economics", "20%", "LTV/CAC >3x=100, 2-3x=75, 1-2x=40 | Payback <12mo=85"),
        ("Path to Profitability", "20%", "Profitable=100, <12mo=80, 12-24mo=60, 24-36mo=40, >36mo=25")
    ])

    # Growth (40%) - HIGHEST
    row, growth_total, _, _ = add_component_section(ws, row + 1, "Growth Score", "40", [
        ("Revenue Growth", "28%", ">100%=100, 75-100%=95, 55-75%=85, 40-55%=70, 30-40%=50"),
        ("Growth Consistency", "15%", "5+ qtrs accel=100, 4 qtrs=90, 3 qtrs=80, Stable 40%+=70"),
        ("TAM Size", "15%", ">$150B=100, $100-150B=90, $50-100B=75, $25-50B=55, <$25B=35"),
        ("Market Penetration", "10%", "<3%=100, 3-5%=90, 5-10%=75, 10-15%=55, >15%=35"),
        ("Growth Driver Strength", "15%", "Base 50 + Network=+25, Viral>50%=+25, Platform=+20"),
        ("Forward Estimates", "12%", ">60%=100, 50-60%=90, 40-50%=80 + accel >12%=+20"),
        ("Catalyst Pipeline", "5%", "Base 50 + Launch=+30, Market expand=+25, Partnership=+25")
    ])

    # Momentum (15%)
    row, mom_total, _, _ = add_component_section(ws, row + 1, "Momentum Score", "15", [
        ("6-Month Return", "40%", ">100%=100, 70-100%=95, 50-70%=85, 30-50%=70, <0%=60 oversold"),
        ("Relative Strength vs IWO", "30%", ">30% outperform=100, 20-30%=85, 10-20%=65, 0-10%=45"),
        ("Social Sentiment", "20%", "Base 50 + Bullish mentions=+25, Upgrades=+25, avoid meme=-20"),
        ("Volume Surge", "10%", ">75% increase=100, 50-75%=85, 25-50%=65, Stable=50")
    ])

    # Disruption Potential (20%)
    row, disrupt_total, _, _ = add_component_section(ws, row + 1, "Disruption Potential Score", "20", [
        ("Market Disruption", "35%", "Attacking $100B+=100, New category=95, Share gains=85, Niche=70"),
        ("Technology Moat", "25%", "Base 50 + Proprietary AI=+30, Patents=+25, Data=+25, Supply chain=+25"),
        ("Competitive Dynamics", "25%", "Winner-take-most=100, Oligopoly=80, Differentiated=60, Crowded=40"),
        ("Catalyst Pipeline", "15%", "Base 50 + Launch=+30, Partnership=+25, Regulatory=+30, M&A target=+20")
    ])

    composite_formula = f"=E{val_total}+E{qual_total}+E{growth_total}+E{mom_total}+E{disrupt_total}"
    add_composite_and_sizing(ws, row, composite_formula, 70, 1.5, "B9")

    # Set column widths
    ws.column_dimensions['A'].width = 27
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 75

    return wb


def create_portfolio_summary():
    """Create Portfolio Summary worksheet with rebalancing logic"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Portfolio Summary"

    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)

    # Title
    ws['A1'] = "PORTFOLIO SUMMARY & REBALANCING"
    ws['A1'].font = Font(bold=True, size=14, color="1F4E78")
    ws.merge_cells('A1:L1')

    ws['A2'] = "4-Tier Quantitative Stock Scoring System"
    ws['A2'].font = Font(size=11, italic=True)
    ws.merge_cells('A2:L2')

    # Portfolio Overview
    row = 4
    ws[f'A{row}'] = "PORTFOLIO OVERVIEW"
    ws[f'A{row}'].fill = header_fill
    ws[f'A{row}'].font = header_font
    ws.merge_cells(f'A{row}:D{row}')

    row += 1
    ws[f'A{row}'] = "Total Portfolio Value"
    ws[f'B{row}'] = 100000
    ws[f'B{row}'].number_format = '$#,##0'
    ws[f'A{row}'].font = Font(bold=True)
    portfolio_value_cell = f'B{row}'

    row += 1
    ws[f'A{row}'] = "Cash Reserve"
    ws[f'B{row}'] = 5000
    ws[f'B{row}'].number_format = '$#,##0'
    ws[f'A{row}'].font = Font(bold=True)

    row += 1
    ws[f'A{row}'] = "Invested Value"
    ws[f'B{row}'] = f'={portfolio_value_cell}-B{row-1}'
    ws[f'B{row}'].number_format = '$#,##0'
    ws[f'A{row}'].font = Font(bold=True)

    row += 1
    ws[f'A{row}'] = "Number of Positions"
    ws[f'B{row}'] = '=COUNTA(A13:A32)'
    ws[f'A{row}'].font = Font(bold=True)

    # Holdings Table
    row += 2
    holdings_start = row
    ws[f'A{row}'] = "CURRENT HOLDINGS"
    ws[f'A{row}'].fill = header_fill
    ws[f'A{row}'].font = header_font
    ws.merge_cells(f'A{row}:L{row}')

    row += 1
    headers = ["Ticker", "Tier", "Score", "Min Score", "Buffer", "Current Value",
               "Current %", "Target %", "Drift %", "Action", "Entry Price", "Current Price"]
    for col_idx, header in enumerate(headers, start=1):
        col = get_column_letter(col_idx)
        ws[f'{col}{row}'] = header
        ws[f'{col}{row}'].font = Font(bold=True)
        ws[f'{col}{row}'].fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")

    # Add 20 rows for holdings
    first_holding_row = row + 1
    for i in range(20):
        row += 1
        holding_row = row
        ws[f'A{row}'] = ""  # Ticker
        ws[f'B{row}'] = ""  # Tier (1-4)
        ws[f'C{row}'] = ""  # Score
        ws[f'D{row}'] = f'=IF(B{row}=1,60,IF(B{row}=2,65,IF(B{row}=3,67,IF(B{row}=4,70,""))))'  # Min Score
        ws[f'E{row}'] = f'=IF(C{row}<>"",C{row}-D{row},"")'  # Buffer
        ws[f'F{row}'] = ""  # Current Value
        ws[f'F{row}'].number_format = '$#,##0'
        ws[f'G{row}'] = f'=IF(F{row}<>"",F{row}/{portfolio_value_cell},"")'  # Current %
        ws[f'G{row}'].number_format = '0.0%'
        ws[f'H{row}'] = ""  # Target %
        ws[f'H{row}'].number_format = '0.0%'
        ws[f'I{row}'] = f'=IF(AND(G{row}<>"",H{row}<>""),(G{row}-H{row})/H{row},"")'  # Drift %
        ws[f'I{row}'].number_format = '0.0%'
        ws[f'J{row}'] = f'=IF(I{row}>0.10,"TRIM",IF(AND(I{row}<-0.10,E{row}>=8),"ADD","HOLD"))'  # Action
        ws[f'K{row}'] = ""  # Entry Price
        ws[f'K{row}'].number_format = '$0.00'
        ws[f'L{row}'] = ""  # Current Price
        ws[f'L{row}'].number_format = '$0.00'

    last_holding_row = row

    # Tier Allocation Summary
    row += 2
    ws[f'A{row}'] = "TIER ALLOCATION SUMMARY"
    ws[f'A{row}'].fill = header_fill
    ws[f'A{row}'].font = header_font
    ws.merge_cells(f'A{row}:E{row}')

    row += 1
    ws[f'A{row}'] = "Tier"
    ws[f'B{row}'] = "Target %"
    ws[f'C{row}'] = "Current %"
    ws[f'D{row}'] = "Difference"
    ws[f'E{row}'] = "Status"
    for col in ['A', 'B', 'C', 'D', 'E']:
        ws[f'{col}{row}'].font = Font(bold=True)
        ws[f'{col}{row}'].fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")

    tiers = [
        ("Tier 1: Mega-Cap Core", "45%", 1),
        ("Tier 2: Large-Cap Growth", "28%", 2),
        ("Tier 3: Mid-Cap Emerging", "15%", 3),
        ("Tier 4: Small-Cap Moonshots", "7%", 4)
    ]

    for tier_name, target, tier_num in tiers:
        row += 1
        ws[f'A{row}'] = tier_name
        ws[f'B{row}'] = target
        ws[f'C{row}'] = f'=SUMIF($B${first_holding_row}:$B${last_holding_row},{tier_num},$G${first_holding_row}:$G${last_holding_row})'
        ws[f'C{row}'].number_format = '0.0%'
        ws[f'D{row}'] = f'=C{row}-B{row}'
        ws[f'D{row}'].number_format = '0.0%'
        ws[f'E{row}'] = f'=IF(ABS(D{row})<0.05,"✓ On Target",IF(D{row}>0,"Overweight","Underweight"))'

    # 2-Quarter Exit Rule
    row += 3
    ws[f'A{row}'] = "EXIT RULES & WARNINGS"
    ws[f'A{row}'].fill = PatternFill(start_color="C00000", end_color="C00000", fill_type="solid")
    ws[f'A{row}'].font = Font(bold=True, color="FFFFFF", size=11)
    ws.merge_cells(f'A{row}:E{row}')

    row += 1
    ws[f'A{row}'] = "2-QUARTER RULE: Exit if score < tier minimum for 2 consecutive quarters"
    ws[f'A{row}'].font = Font(italic=True)
    ws.merge_cells(f'A{row}:E{row}')

    row += 1
    ws[f'A{row}'] = "TIER 4 ONLY: MANDATORY -40% stop loss from entry price"
    ws[f'A{row}'].font = Font(italic=True, color="C00000")
    ws.merge_cells(f'A{row}:E{row}')

    # Set column widths
    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 10
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 12
    ws.column_dimensions['F'].width = 15
    ws.column_dimensions['G'].width = 12
    ws.column_dimensions['H'].width = 12
    ws.column_dimensions['I'].width = 12
    ws.column_dimensions['J'].width = 12
    ws.column_dimensions['K'].width = 12
    ws.column_dimensions['L'].width = 12

    # Add conditional formatting for buffers
    for i in range(first_holding_row, last_holding_row + 1):
        ws.conditional_formatting.add(f'E{i}',
            CellIsRule(operator='greaterThanOrEqual', formula=['15'],
                       fill=PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")))
        ws.conditional_formatting.add(f'E{i}',
            CellIsRule(operator='between', formula=['5', '14'],
                       fill=PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")))
        ws.conditional_formatting.add(f'E{i}',
            CellIsRule(operator='lessThan', formula=['5'],
                       fill=PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")))

    return wb


def main():
    """Generate all tier templates"""
    print("Generating Excel templates for 4-Tier Quantitative Stock Scoring System...\n")

    print("Creating Tier 1 (Mega-Cap >$200B)...")
    wb1 = create_tier1_template()
    wb1.save("Tier1_MegaCap_Template.xlsx")
    print("✓ Tier1_MegaCap_Template.xlsx")

    print("\nCreating Tier 2 (Large-Cap $50-200B)...")
    wb2 = create_tier2_template()
    wb2.save("Tier2_LargeCap_Template.xlsx")
    print("✓ Tier2_LargeCap_Template.xlsx")

    print("\nCreating Tier 3 (Mid-Cap $10-50B)...")
    wb3 = create_tier3_template()
    wb3.save("Tier3_MidCap_Template.xlsx")
    print("✓ Tier3_MidCap_Template.xlsx")

    print("\nCreating Tier 4 (Small-Cap <$10B)...")
    wb4 = create_tier4_template()
    wb4.save("Tier4_SmallCap_Template.xlsx")
    print("✓ Tier4_SmallCap_Template.xlsx")

    print("\nCreating Portfolio Summary...")
    wb_summary = create_portfolio_summary()
    wb_summary.save("Portfolio_Summary.xlsx")
    print("✓ Portfolio_Summary.xlsx")

    print("\n" + "="*60)
    print("SUCCESS! All Excel templates generated:")
    print("="*60)
    print("1. Tier1_MegaCap_Template.xlsx      - >$200B (Min: 60, Risk: Lowest)")
    print("2. Tier2_LargeCap_Template.xlsx     - $50-200B (Min: 65, Risk: Low-Mod)")
    print("3. Tier3_MidCap_Template.xlsx       - $10-50B (Min: 67, Risk: Mod-High)")
    print("4. Tier4_SmallCap_Template.xlsx     - <$10B (Min: 70, Risk: Highest)")
    print("5. Portfolio_Summary.xlsx           - Portfolio tracking & rebalancing")
    print("="*60)
    print("\nUsage:")
    print("- Open each tier template to score stocks in that market cap range")
    print("- Fill in blue/white input cells with stock data")
    print("- Scores will calculate automatically")
    print("- Use Portfolio_Summary.xlsx to track all holdings and rebalancing")
    print("\n⚠️  Tier 4 has MANDATORY -40% stop loss from entry price")


if __name__ == "__main__":
    main()
