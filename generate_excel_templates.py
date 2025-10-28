#!/usr/bin/env python3
"""
4-Tier Quantitative Stock Scoring System - Excel Template Generator
Generates Excel workbooks with pre-configured formulas for stock analysis
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule
import openpyxl.worksheet.datavalidation as dv


def create_tier1_template():
    """Create Tier 1: Mega-Cap Core (>$200B) template"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Tier 1 Mega-Cap"

    # Header styling
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)
    section_fill = PatternFill(start_color="D6DCE4", end_color="D6DCE4", fill_type="solid")
    section_font = Font(bold=True, size=11)

    # Title
    ws['A1'] = "TIER 1: MEGA-CAP CORE (>$200B)"
    ws['A1'].font = Font(bold=True, size=14, color="1F4E78")
    ws.merge_cells('A1:F1')

    ws['A2'] = "Minimum Score: 60 | Position Size: 8-12% | Risk: Lowest"
    ws['A2'].font = Font(size=10, italic=True)
    ws.merge_cells('A2:F2')

    # Stock Info Section
    row = 4
    ws[f'A{row}'] = "STOCK INFORMATION"
    ws[f'A{row}'].fill = section_fill
    ws[f'A{row}'].font = section_font
    ws.merge_cells(f'A{row}:B{row}')

    row += 1
    ws[f'A{row}'] = "Ticker"
    ws[f'B{row}'] = ""
    ws[f'A{row}'].font = Font(bold=True)

    row += 1
    ws[f'A{row}'] = "Company Name"
    ws[f'B{row}'] = ""
    ws[f'A{row}'].font = Font(bold=True)

    row += 1
    ws[f'A{row}'] = "Market Cap ($B)"
    ws[f'B{row}'] = ""
    ws[f'A{row}'].font = Font(bold=True)

    row += 1
    ws[f'A{row}'] = "Beta"
    ws[f'B{row}'] = 1.0
    ws[f'A{row}'].font = Font(bold=True)

    row += 1
    ws[f'A{row}'] = "Current Price"
    ws[f'B{row}'] = ""
    ws[f'A{row}'].font = Font(bold=True)

    row += 1
    ws[f'A{row}'] = "Entry Price (if held)"
    ws[f'B{row}'] = ""
    ws[f'A{row}'].font = Font(bold=True)

    # VALUATION SCORE SECTION (20% weight)
    row += 2
    ws[f'A{row}'] = "VALUATION SCORE (20% weight)"
    ws[f'A{row}'].fill = header_fill
    ws[f'A{row}'].font = header_font
    ws.merge_cells(f'A{row}:F{row}')

    row += 1
    ws[f'A{row}'] = "Component"
    ws[f'B{row}'] = "Input Value"
    ws[f'C{row}'] = "Score (0-100)"
    ws[f'D{row}'] = "Weight"
    ws[f'E{row}'] = "Weighted Score"
    ws[f'F{row}'] = "Notes"
    for col in ['A', 'B', 'C', 'D', 'E', 'F']:
        ws[f'{col}{row}'].font = Font(bold=True)
        ws[f'{col}{row}'].fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")

    val_score_row = row

    # P/E Ratio (35%)
    row += 1
    pe_row = row
    ws[f'A{row}'] = "P/E Ratio"
    ws[f'B{row}'] = ""  # Input: Current P/E
    ws[f'C{row}'] = ""  # Score calculated manually or via lookup
    ws[f'D{row}'] = "35%"
    ws[f'E{row}'] = f"=C{row}*0.35"
    ws[f'F{row}'] = "Current P/E vs Historical Avg"

    # FCF Yield (30%)
    row += 1
    fcf_row = row
    ws[f'A{row}'] = "FCF Yield"
    ws[f'B{row}'] = ""  # Input: FCF Yield %
    ws[f'C{row}'] = ""  # Score
    ws[f'D{row}'] = "30%"
    ws[f'E{row}'] = f"=C{row}*0.30"
    ws[f'F{row}'] = ">5%=100, 3-5%=80, 2-3%=60, 1-2%=40, <1%=20"

    # PEG Ratio (35%)
    row += 1
    peg_row = row
    ws[f'A{row}'] = "PEG Ratio"
    ws[f'B{row}'] = ""  # Input: PEG
    ws[f'C{row}'] = ""  # Score
    ws[f'D{row}'] = "35%"
    ws[f'E{row}'] = f"=C{row}*0.35"
    ws[f'F{row}'] = "<1.0=100, 1.0-1.5=85, 1.5-2.0=70, 2.0-2.5=50, >2.5=30"

    # Valuation Total
    row += 1
    val_total_row = row
    ws[f'A{row}'] = "VALUATION TOTAL"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f"=AVERAGE(C{pe_row}:C{peg_row})"
    ws[f'E{row}'] = f"=SUM(E{pe_row}:E{peg_row})"
    ws[f'E{row}'].font = Font(bold=True)
    ws[f'E{row}'].fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

    # QUALITY SCORE SECTION (35% weight - HIGHEST)
    row += 2
    ws[f'A{row}'] = "QUALITY SCORE (35% weight - HIGHEST)"
    ws[f'A{row}'].fill = header_fill
    ws[f'A{row}'].font = header_font
    ws.merge_cells(f'A{row}:F{row}')

    row += 1
    ws[f'A{row}'] = "Component"
    ws[f'B{row}'] = "Input Value"
    ws[f'C{row}'] = "Score (0-100)"
    ws[f'D{row}'] = "Weight"
    ws[f'E{row}'] = "Weighted Score"
    ws[f'F{row}'] = "Notes"
    for col in ['A', 'B', 'C', 'D', 'E', 'F']:
        ws[f'{col}{row}'].font = Font(bold=True)
        ws[f'{col}{row}'].fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")

    # ROIC (30%)
    row += 1
    roic_row = row
    ws[f'A{row}'] = "ROIC"
    ws[f'B{row}'] = ""  # Input: ROIC %
    ws[f'C{row}'] = ""  # Score
    ws[f'D{row}'] = "30%"
    ws[f'E{row}'] = f"=C{row}*0.30"
    ws[f'F{row}'] = ">25%=100, 20-25%=90, 15-20%=75, 10-15%=50, <10%=25"

    # Operating Margin (20%)
    row += 1
    ws[f'A{row}'] = "Operating Margin"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "20%"
    ws[f'E{row}'] = f"=C{row}*0.20"
    ws[f'F{row}'] = ">30%=100, 20-30%=85, 15-20%=70, 10-15%=50, <10%=30"

    # Op Margin Trend (12%)
    row += 1
    ws[f'A{row}'] = "Op Margin Trend"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "12%"
    ws[f'E{row}'] = f"=C{row}*0.12"
    ws[f'F{row}'] = ">200bps/yr=100, 100-200=85, 50-100=70, ±50=60, declining=25"

    # Competitive Moat (18%)
    row += 1
    ws[f'A{row}'] = "Competitive Moat"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "18%"
    ws[f'E{row}'] = f"=C{row}*0.18"
    ws[f'F{row}'] = "Base 50 + bonuses (Network+25, Scale+20, Switching+20, Brand+15, Reg+10)"

    # Management Execution (10%)
    row += 1
    ws[f'A{row}'] = "Management Execution"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "10%"
    ws[f'E{row}'] = f"=C{row}*0.10"
    ws[f'F{row}'] = "Earnings beat rate: >80%=100, 70-80%=85, 60-70%=70, <60%=50 + bonuses"

    # Cash Conversion (10%)
    row += 1
    quality_last_row = row
    ws[f'A{row}'] = "Cash Conversion"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "10%"
    ws[f'E{row}'] = f"=C{row}*0.10"
    ws[f'F{row}'] = "FCF/Net Income: >1.2=100, 1.0-1.2=80, 0.8-1.0=60, <0.8=30"

    # Quality Total
    row += 1
    quality_total_row = row
    ws[f'A{row}'] = "QUALITY TOTAL"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f"=AVERAGE(C{roic_row}:C{quality_last_row})"
    ws[f'E{row}'] = f"=SUM(E{roic_row}:E{quality_last_row})"
    ws[f'E{row}'].font = Font(bold=True)
    ws[f'E{row}'].fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

    # GROWTH SCORE SECTION (25% weight)
    row += 2
    ws[f'A{row}'] = "GROWTH SCORE (25% weight)"
    ws[f'A{row}'].fill = header_fill
    ws[f'A{row}'].font = header_font
    ws.merge_cells(f'A{row}:F{row}')

    row += 1
    ws[f'A{row}'] = "Component"
    ws[f'B{row}'] = "Input Value"
    ws[f'C{row}'] = "Score (0-100)"
    ws[f'D{row}'] = "Weight"
    ws[f'E{row}'] = "Weighted Score"
    ws[f'F{row}'] = "Notes"
    for col in ['A', 'B', 'C', 'D', 'E', 'F']:
        ws[f'{col}{row}'].font = Font(bold=True)
        ws[f'{col}{row}'].fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")

    # Revenue Growth 3Yr CAGR (30%)
    row += 1
    growth_first_row = row
    ws[f'A{row}'] = "Revenue Growth (3Yr CAGR)"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "30%"
    ws[f'E{row}'] = f"=C{row}*0.30"
    ws[f'F{row}'] = ">20%=100, 15-20%=85, 10-15%=65, 7-10%=45, 5-7%=30, <5%=15"

    # Growth Consistency (15%)
    row += 1
    ws[f'A{row}'] = "Growth Consistency"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "15%"
    ws[f'E{row}'] = f"=C{row}*0.15"
    ws[f'F{row}'] = "Base 50, adjust for acceleration/deceleration"

    # EPS Growth 3Yr CAGR (25%)
    row += 1
    ws[f'A{row}'] = "EPS Growth (3Yr CAGR)"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "25%"
    ws[f'E{row}'] = f"=C{row}*0.25"
    ws[f'F{row}'] = ">25%=100, 18-25%=85, 12-18%=70, 8-12%=50, <8%=30"

    # Future Growth Potential (15%)
    row += 1
    ws[f'A{row}'] = "Future Growth Potential"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "15%"
    ws[f'E{row}'] = f"=C{row}*0.15"
    ws[f'F{row}'] = "TAM assessment + bonuses for expansion opportunities"

    # Analyst Consensus (15%)
    row += 1
    growth_last_row = row
    ws[f'A{row}'] = "Analyst Consensus"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "15%"
    ws[f'E{row}'] = f"=C{row}*0.15"
    ws[f'F{row}'] = ">15%=100, 12-15%=80, 8-12%=60, 5-8%=40, <5%=20"

    # Growth Total
    row += 1
    growth_total_row = row
    ws[f'A{row}'] = "GROWTH TOTAL"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f"=AVERAGE(C{growth_first_row}:C{growth_last_row})"
    ws[f'E{row}'] = f"=SUM(E{growth_first_row}:E{growth_last_row})"
    ws[f'E{row}'].font = Font(bold=True)
    ws[f'E{row}'].fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

    # MOMENTUM SCORE SECTION (10% weight)
    row += 2
    ws[f'A{row}'] = "MOMENTUM SCORE (10% weight)"
    ws[f'A{row}'].fill = header_fill
    ws[f'A{row}'].font = header_font
    ws.merge_cells(f'A{row}:F{row}')

    row += 1
    ws[f'A{row}'] = "Component"
    ws[f'B{row}'] = "Input Value"
    ws[f'C{row}'] = "Score (0-100)"
    ws[f'D{row}'] = "Weight"
    ws[f'E{row}'] = "Weighted Score"
    ws[f'F{row}'] = "Notes"
    for col in ['A', 'B', 'C', 'D', 'E', 'F']:
        ws[f'{col}{row}'].font = Font(bold=True)
        ws[f'{col}{row}'].fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")

    # 12-Month Price Return (40%)
    row += 1
    momentum_first_row = row
    ws[f'A{row}'] = "12-Month Price Return"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "40%"
    ws[f'E{row}'] = f"=C{row}*0.40"
    ws[f'F{row}'] = ">30%=100, 20-30%=80, 10-20%=60, 0-10%=45, -10-0%=40, <-10%=60"

    # Relative Strength vs SPY (35%)
    row += 1
    ws[f'A{row}'] = "Relative Strength vs SPY"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "35%"
    ws[f'E{row}'] = f"=C{row}*0.35"
    ws[f'F{row}'] = "Outperform >10%=100, 5-10%=75, 0-5%=60, -5-0%=50, <-5%=30"

    # Technical Setup (25%)
    row += 1
    momentum_last_row = row
    ws[f'A{row}'] = "Technical Setup"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "25%"
    ws[f'E{row}'] = f"=C{row}*0.25"
    ws[f'F{row}'] = "Above 50&200 MA=100, Above 200=70, Above 50=55, Between=50, Below=30"

    # Momentum Total
    row += 1
    momentum_total_row = row
    ws[f'A{row}'] = "MOMENTUM TOTAL"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f"=AVERAGE(C{momentum_first_row}:C{momentum_last_row})"
    ws[f'E{row}'] = f"=SUM(E{momentum_first_row}:E{momentum_last_row})"
    ws[f'E{row}'].font = Font(bold=True)
    ws[f'E{row}'].fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

    # FINANCIAL HEALTH SCORE SECTION (10% weight)
    row += 2
    ws[f'A{row}'] = "FINANCIAL HEALTH SCORE (10% weight)"
    ws[f'A{row}'].fill = header_fill
    ws[f'A{row}'].font = header_font
    ws.merge_cells(f'A{row}:F{row}')

    row += 1
    ws[f'A{row}'] = "Component"
    ws[f'B{row}'] = "Input Value"
    ws[f'C{row}'] = "Score (0-100)"
    ws[f'D{row}'] = "Weight"
    ws[f'E{row}'] = "Weighted Score"
    ws[f'F{row}'] = "Notes"
    for col in ['A', 'B', 'C', 'D', 'E', 'F']:
        ws[f'{col}{row}'].font = Font(bold=True)
        ws[f'{col}{row}'].fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")

    # Net Cash Position (50%)
    row += 1
    fh_first_row = row
    ws[f'A{row}'] = "Net Cash Position"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "50%"
    ws[f'E{row}'] = f"=C{row}*0.50"
    ws[f'F{row}'] = ">$75B=100, $50-75B=90, $25-50B=80, $0-25B=70, Net debt<$50B=60, >$50B=40"

    # FCF Generation (40%)
    row += 1
    ws[f'A{row}'] = "FCF Generation"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "40%"
    ws[f'E{row}'] = f"=C{row}*0.40"
    ws[f'F{row}'] = ">$20B=100, $15-20B=90, $10-15B=80, $5-10B=60, <$5B=40"

    # Capital Allocation (10%)
    row += 1
    fh_last_row = row
    ws[f'A{row}'] = "Capital Allocation"
    ws[f'B{row}'] = ""
    ws[f'C{row}'] = ""
    ws[f'D{row}'] = "10%"
    ws[f'E{row}'] = f"=C{row}*0.10"
    ws[f'F{row}'] = "Base 50 + bonuses (Buybacks+R&D>10%=+25, M&A=+20, Dividend=+15)"

    # Financial Health Total
    row += 1
    fh_total_row = row
    ws[f'A{row}'] = "FINANCIAL HEALTH TOTAL"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f"=AVERAGE(C{fh_first_row}:C{fh_last_row})"
    ws[f'E{row}'] = f"=SUM(E{fh_first_row}:E{fh_last_row})"
    ws[f'E{row}'].font = Font(bold=True)
    ws[f'E{row}'].fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

    # COMPOSITE SCORE
    row += 3
    composite_row = row
    ws[f'A{row}'] = "COMPOSITE SCORE"
    ws[f'A{row}'].fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    ws[f'A{row}'].font = Font(bold=True, size=12, color="FFFFFF")
    ws.merge_cells(f'A{row}:B{row}')

    ws[f'C{row}'] = f"=E{val_total_row}+E{quality_total_row}+E{growth_total_row}+E{momentum_total_row}+E{fh_total_row}"
    ws[f'C{row}'].font = Font(bold=True, size=14)
    ws[f'C{row}'].fill = PatternFill(start_color="FFC000", end_color="FFC000", fill_type="solid")
    ws[f'C{row}'].number_format = '0.00'

    row += 1
    ws[f'A{row}'] = "RATING"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=IF(C{composite_row}>=80,"Strong Buy",IF(C{composite_row}>=70,"Buy",IF(C{composite_row}>=60,"Hold","Sell")))'
    ws[f'C{row}'].font = Font(bold=True, size=12)

    row += 1
    ws[f'A{row}'] = "Score Buffer vs Min (60)"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=C{composite_row}-60'
    ws[f'C{row}'].number_format = '0.00'

    # POSITION SIZING
    row += 2
    ws[f'A{row}'] = "POSITION SIZING"
    ws[f'A{row}'].fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    ws[f'A{row}'].font = Font(bold=True, size=12, color="FFFFFF")
    ws.merge_cells(f'A{row}:B{row}')

    row += 1
    ws[f'A{row}'] = "Target Position %"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=(10%*C{composite_row}/100)/(1+(B9-1)*0.75)'
    ws[f'C{row}'].number_format = '0.0%'
    ws[f'F{row}'] = "Formula: (10% × Score/100) / (1 + (Beta-1) × 0.75)"

    row += 1
    ws[f'A{row}'] = "Portfolio Value ($)"
    ws[f'B{row}'] = 100000
    ws[f'B{row}'].number_format = '$#,##0'
    ws[f'A{row}'].font = Font(bold=True)

    row += 1
    ws[f'A{row}'] = "Target Dollar Amount"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=C{row-2}*B{row-1}'
    ws[f'C{row}'].number_format = '$#,##0'

    row += 1
    ws[f'A{row}'] = "Current Position Value"
    ws[f'B{row}'] = ""
    ws[f'B{row}'].number_format = '$#,##0'
    ws[f'A{row}'].font = Font(bold=True)

    row += 1
    ws[f'A{row}'] = "Current Position %"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=IF(B{row-4}>0,B{row-1}/B{row-4},0)'
    ws[f'C{row}'].number_format = '0.0%'

    row += 1
    ws[f'A{row}'] = "Drift %"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=IF(C{row-4}>0,(C{row-1}-C{row-4})/C{row-4},0)'
    ws[f'C{row}'].number_format = '0.0%'

    row += 1
    ws[f'A{row}'] = "Action"
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'C{row}'] = f'=IF(C{row-1}>0.10,"TRIM",IF(AND(C{row-1}<-0.10,C{composite_row}>=68),"ADD IF STRONG","HOLD"))'
    ws[f'C{row}'].font = Font(bold=True)

    # Column widths
    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 60

    # Add conditional formatting for score buffer
    ws.conditional_formatting.add(f'C{composite_row-2}',
        CellIsRule(operator='greaterThanOrEqual', formula=['15'], fill=PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")))
    ws.conditional_formatting.add(f'C{composite_row-2}',
        CellIsRule(operator='between', formula=['5', '14'], fill=PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")))
    ws.conditional_formatting.add(f'C{composite_row-2}',
        CellIsRule(operator='lessThan', formula=['5'], fill=PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")))

    return wb


def main():
    """Generate all tier templates"""
    print("Generating Tier 1 (Mega-Cap) template...")
    wb1 = create_tier1_template()
    wb1.save("Tier1_MegaCap_Template.xlsx")
    print("✓ Tier1_MegaCap_Template.xlsx created")

    print("\nTier 2-4 templates will be created in next iteration...")
    print("\nDone! Check the generated Excel files.")


if __name__ == "__main__":
    main()
