"""
Excel Generator Tool for Constructiv AI Competitive Analysis

This module provides functions to generate formatted Excel workbooks with competitor data.
"""
import os
import json
from pathlib import Path
import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.chart import BarChart, Reference, PieChart, ScatterChart
from openpyxl.utils import get_column_letter

# Import configuration
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config import PROCESSED_DIR, ANALYSIS_DIR, EXCEL_OUTPUT_DIR, EXCEL_TEMPLATES

class ExcelGenerator:
    """Class for generating Excel workbooks with competitor data"""
    
    def __init__(self, template_name="competitor_profile"):
        """
        Initialize the Excel generator
        
        Parameters:
        - template_name: Which Excel template to use
        """
        self.template_name = template_name
        self.template_config = EXCEL_TEMPLATES.get(template_name, {})
        self.workbook = Workbook()
        
        # Remove default sheet
        if "Sheet" in self.workbook.sheetnames:
            self.workbook.remove(self.workbook.active)
        
        # Create sheets based on template
        for sheet_name in self.template_config.get("sheets", []):
            self.workbook.create_sheet(sheet_name)
        
        # Apply basic formatting
        self._apply_basic_formatting()
    
    def _apply_basic_formatting(self):
        """Apply basic formatting to all sheets"""
        for sheet in self.workbook.worksheets:
            # Set column widths
            for col in range(1, 20):
                sheet.column_dimensions[get_column_letter(col)].width = 15
            
            # Set row heights
            for row in range(1, 10):
                sheet.row_dimensions[row].height = 20
            
            # Add header row formatting
            header_fill = PatternFill(start_color="0072BA", end_color="0072BA", fill_type="solid")
            header_font = Font(color="FFFFFF", bold=True, size=12)
            header_alignment = Alignment(horizontal="center", vertical="center")
            
            # Apply header styling to first row
            for cell in sheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = header_alignment
    
    def generate_company_profile(self, company_data):
        """
        Generate a company profile workbook
        
        Parameters:
        - company_data: Dictionary with company information
        """
        if "Company Overview" in self.workbook.sheetnames:
            sheet = self.workbook["Company Overview"]
            
            # Add company header
            sheet["A1"] = "Company Name"
            sheet["B1"] = "Website"
            sheet["C1"] = "Founded"
            sheet["D1"] = "Headquarters"
            sheet["E1"] = "Description"
            
            # Add company data
            sheet["A2"] = company_data.get("name", "")
            sheet["B2"] = company_data.get("website", "")
            sheet["C2"] = company_data.get("founded", "")
            sheet["D2"] = company_data.get("headquarters", "")
            sheet["E2"] = company_data.get("description", "")
            
            # Add funding info
            sheet["A4"] = "Funding History"
            sheet["A4"].font = Font(bold=True, size=12)
            
            sheet["A5"] = "Date"
            sheet["B5"] = "Round"
            sheet["C5"] = "Amount"
            sheet["D5"] = "Lead Investor"
            sheet["E5"] = "All Investors"
            
            # Style the funding header
            for cell in sheet[5]:
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="E6F2FF", end_color="E6F2FF", fill_type="solid")
            
            # Add funding data
            funding_data = company_data.get("funding", [])
            for i, funding in enumerate(funding_data):
                row = 6 + i
                sheet[f"A{row}"] = funding.get("date", "")
                sheet[f"B{row}"] = funding.get("round", "")
                sheet[f"C{row}"] = funding.get("amount", "")
                
                investors = funding.get("investors", [])
                if investors:
                    sheet[f"D{row}"] = investors[0] if investors else ""
                    sheet[f"E{row}"] = ", ".join(investors)
        
        # Products & Services sheet
        if "Products & Services" in self.workbook.sheetnames:
            sheet = self.workbook["Products & Services"]
            
            sheet["A1"] = "Product Name"
            sheet["B1"] = "Category"
            sheet["C1"] = "Target Audience"
            sheet["D1"] = "Description"
            
            products = company_data.get("products_services", [])
            for i, product in enumerate(products):
                row = 2 + i
                sheet[f"A{row}"] = product.get("name", "")
                sheet[f"B{row}"] = product.get("category", "")
                sheet[f"C{row}"] = product.get("target_audience", "")
                sheet[f"D{row}"] = product.get("description", "")
        
        # Market Position sheet
        if "Market Position" in self.workbook.sheetnames:
            sheet = self.workbook["Market Position"]
            
            sheet["A1"] = "Competitors"
            sheet["A1"].font = Font(bold=True, size=12)
            
            competitors = company_data.get("competitors", [])
            for i, competitor in enumerate(competitors):
                sheet[f"A{i+2}"] = competitor
            
            sheet["C1"] = "Technology Stack"
            sheet["C1"].font = Font(bold=True, size=12)
            
            tech_stack = company_data.get("technology_stack", [])
            for i, tech in enumerate(tech_stack):
                sheet[f"C{i+2}"] = tech
        
        # SWOT Analysis sheet
        if "SWOT Analysis" in self.workbook.sheetnames:
            sheet = self.workbook["SWOT Analysis"]
            
            # Add SWOT headers
            sheet["A1"] = "Strengths"
            sheet["B1"] = "Weaknesses"
            sheet["C1"] = "Opportunities"
            sheet["D1"] = "Threats"
            
            # Set up SWOT table for manual entry
            for col in ["A", "B", "C", "D"]:
                for row in range(2, 12):
                    cell = sheet[f"{col}{row}"]
                    cell.border = Border(
                        left=Side(style='thin'), 
                        right=Side(style='thin'),
                        top=Side(style='thin'), 
                        bottom=Side(style='thin')
                    )
    
    def generate_competitive_landscape(self, competitors_data):
        """
        Generate a competitive landscape workbook
        
        Parameters:
        - competitors_data: List of dictionaries with competitor information
        """
        if "Market Map" in self.workbook.sheetnames:
            sheet = self.workbook["Market Map"]
            
            # Add market map headers
            sheet["A1"] = "Company"
            sheet["B1"] = "Category"
            sheet["C1"] = "Total Funding"
            sheet["D1"] = "Founded"
            sheet["E1"] = "Employees"
            sheet["F1"] = "Market Focus"
            
            # Add competitor data
            for i, competitor in enumerate(competitors_data):
                row = 2 + i
                sheet[f"A{row}"] = competitor.get("name", "")
                sheet[f"B{row}"] = competitor.get("category", "")
                
                # Calculate total funding
                funding = competitor.get("funding", [])
                total_funding = sum([self._parse_funding_amount(f.get("amount", "0")) for f in funding])
                sheet[f"C{row}"] = f"${total_funding:,.2f}" if total_funding > 0 else "Unknown"
                
                sheet[f"D{row}"] = competitor.get("founded", "")
                sheet[f"E{row}"] = competitor.get("employees", "")
                sheet[f"F{row}"] = competitor.get("market_focus", "")
            
            # Create market map chart
            if len(competitors_data) > 1:
                chart = ScatterChart()
                chart.title = "Competitive Landscape"
                chart.x_axis.title = "Market Focus"
                chart.y_axis.title = "Total Funding"
                
                # Add data
                data = Reference(sheet, min_col=3, min_row=2, max_row=1+len(competitors_data), max_col=3)
                categories = Reference(sheet, min_col=6, min_row=2, max_row=1+len(competitors_data))
                series = chart.series[0] if chart.series else chart.add_series()
                series.marker.symbol = "circle"
                series.marker.size = 10
                series.graphicalProperties.line.noFill = True
                
                # Set titles
                titles = Reference(sheet, min_col=1, min_row=2, max_row=1+len(competitors_data))
                
                sheet.add_chart(chart, "H2")
        
        # Competitor Comparison sheet
        if "Competitor Comparison" in self.workbook.sheetnames and competitors_data:
            sheet = self.workbook["Competitor Comparison"]
            
            # Setup comparison table
            sheet["A1"] = "Feature"
            
            # Add competitor names as headers
            for i, competitor in enumerate(competitors_data):
                col = get_column_letter(i + 2)
                sheet[f"{col}1"] = competitor.get("name", f"Competitor {i+1}")
            
            # Standard features to compare
            features = [
                "Founded Year", 
                "Headquarters",
                "Latest Funding Round", 
                "Total Funding", 
                "Primary Product",
                "Target Market",
                "Technology Stack",
                "Key Differentiator"
            ]
            
            # Add feature rows
            for i, feature in enumerate(features):
                row = i + 2
                sheet[f"A{row}"] = feature
            
            # Add data for each competitor
            for i, competitor in enumerate(competitors_data):
                col = get_column_letter(i + 2)
                
                sheet[f"{col}2"] = competitor.get("founded", "")
                sheet[f"{col}3"] = competitor.get("headquarters", "")
                
                # Latest funding
                funding = competitor.get("funding", [])
                latest_funding = funding[-1] if funding else {}
                sheet[f"{col}4"] = f"{latest_funding.get('round', '')} ({latest_funding.get('amount', '')})" if latest_funding else ""
                
                # Calculate total funding
                total_funding = sum([self._parse_funding_amount(f.get("amount", "0")) for f in funding])
                sheet[f"{col}5"] = f"${total_funding:,.2f}" if total_funding > 0 else "Unknown"
                
                # Product info
                products = competitor.get("products_services", [])
                primary_product = products[0] if products else {}
                sheet[f"{col}6"] = primary_product.get("name", "")
                sheet[f"{col}7"] = competitor.get("market_focus", "")
                
                # Tech stack
                tech_stack = competitor.get("technology_stack", [])
                sheet[f"{col}8"] = ", ".join(tech_stack) if tech_stack else ""
                
                # Key differentiator would typically be added manually or through AI analysis
                sheet[f"{col}9"] = competitor.get("key_differentiator", "")
    
    def _parse_funding_amount(self, amount_str):
        """Parse funding amount string to float"""
        if not amount_str:
            return 0
        
        # Remove non-numeric characters except for M, K, B
        clean_str = ''.join(c for c in amount_str if c.isdigit() or c in '.,MKB')
        
        try:
            # Handle different formats
            if 'B' in clean_str:
                return float(clean_str.replace('B', '')) * 1000000000
            elif 'M' in clean_str:
                return float(clean_str.replace('M', '')) * 1000000
            elif 'K' in clean_str:
                return float(clean_str.replace('K', '')) * 1000
            else:
                return float(clean_str)
        except ValueError:
            return 0
    
    def add_funding_chart(self, company_data):
        """Add funding chart to Company Overview sheet"""
        sheet = self.workbook["Company Overview"]
        funding_data = company_data.get("funding", [])
        
        if not funding_data:
            return
        
        # Create a small table for chart data
        sheet["G4"] = "Round"
        sheet["H4"] = "Amount (USD)"
        
        for i, funding in enumerate(funding_data):
            row = 5 + i
            sheet[f"G{row}"] = funding.get("round", f"Round {i+1}")
            
            # Parse amount 
            amount_str = funding.get("amount", "0")
            amount = self._parse_funding_amount(amount_str)
            sheet[f"H{row}"] = amount
        
        # Create chart
        chart = BarChart()
        chart.title = "Funding History"
        chart.style = 10
        chart.x_axis.title = "Round"
        chart.y_axis.title = "Amount (USD)"
        
        data = Reference(sheet, min_col=8, min_row=4, max_row=4+len(funding_data))
        cats = Reference(sheet, min_col=7, min_row=5, max_row=4+len(funding_data))
        
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)
        
        sheet.add_chart(chart, "G15")
    
    def save_workbook(self, output_path=None, company_name=None):
        """
        Save the workbook to a file
        
        Parameters:
        - output_path: Path to save the Excel file (optional)
        - company_name: Name of the company for default filename (optional)
        
        Returns:
        - Path to the saved file
        """
        if not output_path:
            # Create output path in analysis directory
            if not company_name:
                company_name = "competitive_analysis"
            
            # Sanitize filename
            company_name = company_name.replace(' ', '_').lower()
            output_path = EXCEL_OUTPUT_DIR / f"{company_name}_{self.template_name}.xlsx"
        
        # Create directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.workbook.save(output_path)
        return output_path

def generate_excel(competitor_data, template_name="competitor_profile", output_path=None):
    """
    Generate a formatted Excel workbook with competitor data.
    
    Parameters:
    - competitor_data: Dictionary or list of dictionaries with competitor information
    - template_name: Which Excel template to use
    - output_path: Where to save the file
    
    Returns:
    - Path to generated Excel file
    """
    generator = ExcelGenerator(template_name)
    
    if template_name == "competitor_profile":
        # Single company profile
        generator.generate_company_profile(competitor_data)
        generator.add_funding_chart(competitor_data)
        company_name = competitor_data.get("name", "company")
    
    elif template_name == "competitive_landscape":
        # Multiple company comparison
        if not isinstance(competitor_data, list):
            competitor_data = [competitor_data]
        
        generator.generate_competitive_landscape(competitor_data)
        company_name = "competitive_landscape"
    
    else:
        # Unknown template
        raise ValueError(f"Unknown template: {template_name}")
    
    return generator.save_workbook(output_path, company_name)

def load_competitor_data(company_name, is_primary=True):
    """
    Load competitor data from processed files
    
    Parameters:
    - company_name: Name of the company
    - is_primary: Whether this is a primary competitor
    
    Returns:
    - Dictionary with competitor data
    """
    category = "primary" if is_primary else "adjacent"
    company_dir = PROCESSED_DIR / "competitors" / category / company_name
    
    if not company_dir.exists():
        return None
    
    # Find JSON files
    json_files = list(company_dir.glob("*.json"))
    
    if not json_files:
        return None
    
    # Load and combine data from all JSON files
    combined_data = {}
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            combined_data.update(data)
    
    return combined_data

def generate_competitive_landscape_excel(company_names, output_path=None):
    """
    Generate a competitive landscape Excel workbook for multiple companies
    
    Parameters:
    - company_names: List of company names
    - output_path: Where to save the file
    
    Returns:
    - Path to generated Excel file
    """
    companies_data = []
    
    for company_name in company_names:
        # Try as primary competitor first
        data = load_competitor_data(company_name, is_primary=True)
        
        # If not found, try as adjacent competitor
        if not data:
            data = load_competitor_data(company_name, is_primary=False)
        
        if data:
            companies_data.append(data)
    
    if not companies_data:
        return None
    
    return generate_excel(companies_data, template_name="competitive_landscape", output_path=output_path)

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python excel_generator.py <template_name> <company_name> [output_path]")
        sys.exit(1)
    
    template_name = sys.argv[1]
    company_name = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Load company data
    data = load_competitor_data(company_name)
    
    if not data:
        print(f"No data found for company: {company_name}")
        sys.exit(1)
    
    # Generate Excel
    excel_path = generate_excel(data, template_name, output_path)
    print(f"Excel file generated at: {excel_path}")