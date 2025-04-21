"""
Command-Line Interface for Constructiv AI Competitive Analysis Tool

This module provides a simple command-line interface for interacting with the competitive analysis tools.
"""
import os
import sys
from pathlib import Path
import argparse
import json
import time

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from config import OPENAI_API_KEY, RAW_DIR, PROCESSED_DIR, ANALYSIS_DIR
from src.tools.pdf_extractor import extract_from_pdf
from src.tools.web_scraper import scrape_competitor_website
from src.tools.excel_generator import generate_excel, generate_competitive_landscape_excel
from src.tools.visualization import create_visualization, load_competitor_data
from src.analysis.competitive_analyst import CompetitiveAnalyst, analyze_competitors

def check_setup():
    """Check if the system is properly set up"""
    if not OPENAI_API_KEY:
        print("Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        print("Create a .env file in the project root with: OPENAI_API_KEY=your_api_key_here")
        return False
    
    # Check if directories exist
    for directory in [RAW_DIR, PROCESSED_DIR, ANALYSIS_DIR]:
        if not directory.exists():
            print(f"Error: Directory {directory} not found.")
            return False
    
    return True

def extract_pdf(args):
    """Extract data from a PDF file"""
    if not args.pdf_path:
        print("Error: PDF path is required.")
        return
    
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: PDF file not found at {pdf_path}")
        return
    
    print(f"Extracting data from {pdf_path}...")
    output_path = args.output_path if args.output_path else None
    
    result = extract_from_pdf(pdf_path, output_path)
    if result:
        if output_path:
            print(f"Extraction complete. Data saved to {output_path}")
        else:
            print(f"Extraction complete.")
    else:
        print("Extraction failed.")

def scrape_website(args):
    """Scrape data from a competitor website"""
    if not args.url:
        print("Error: Website URL is required.")
        return
    
    print(f"Scraping data from {args.url}...")
    output_path = args.output_path if args.output_path else None
    
    result = scrape_competitor_website(args.url, output_path)
    if result:
        if output_path:
            print(f"Scraping complete. Data saved to {output_path}")
        else:
            print(f"Scraping complete.")
    else:
        print("Scraping failed.")

def generate_analysis(args):
    """Generate analysis for a company or companies"""
    if not args.companies:
        print("Error: At least one company name is required.")
        return
    
    company_names = args.companies.split(',')
    print(f"Analyzing competitors: {', '.join(company_names)}...")
    
    result = analyze_competitors(company_names, not args.adjacent)
    if result:
        print("Analysis complete.")
        
        # Print summary if requested
        if args.summary:
            analyst = CompetitiveAnalyst()
            report = analyst.generate_report(result)
            print("\nEXECUTIVE SUMMARY:")
            print("-" * 80)
            print(report)
            print("-" * 80)
    else:
        print("Analysis failed. No data found for the specified companies.")

def create_excel(args):
    """Generate Excel outputs"""
    if not args.companies:
        print("Error: At least one company name is required.")
        return
    
    company_names = args.companies.split(',')
    output_path = args.output_path if args.output_path else None
    
    if len(company_names) == 1 and not args.landscape:
        # Single company profile
        print(f"Generating Excel profile for {company_names[0]}...")
        data = load_competitor_data(company_names[0])
        if not data:
            print(f"Error: No data found for company {company_names[0]}")
            return
        
        output_file = generate_excel(data, "competitor_profile", output_path)
        print(f"Excel file generated: {output_file}")
    else:
        # Multiple company landscape
        print(f"Generating competitive landscape Excel for {', '.join(company_names)}...")
        output_file = generate_competitive_landscape_excel(company_names, output_path)
        if output_file:
            print(f"Excel file generated: {output_file}")
        else:
            print("Failed to generate Excel file. No data found for the specified companies.")

def create_viz(args):
    """Generate visualizations"""
    if not args.companies:
        print("Error: At least one company name is required.")
        return
    
    if not args.chart_type:
        print("Error: Chart type is required.")
        return
    
    company_names = args.companies.split(',')
    output_path = args.output_path if args.output_path else None
    
    print(f"Generating {args.chart_type} visualization for {', '.join(company_names)}...")
    
    companies_data = load_competitor_data(company_names)
    if not companies_data:
        print(f"Error: No data found for companies {', '.join(company_names)}")
        return
    
    output_file = create_visualization(companies_data, args.chart_type, output_path)
    if output_file:
        print(f"Visualization generated: {output_file}")
    else:
        print("Failed to generate visualization.")

def list_companies(args):
    """List available companies in the database"""
    # List primary competitors
    primary_dir = RAW_DIR / "competitors" / "primary"
    primary_companies = [d.name for d in primary_dir.iterdir() if d.is_dir()]
    
    # List adjacent competitors
    adjacent_dir = RAW_DIR / "competitors" / "adjacent"
    adjacent_companies = [d.name for d in adjacent_dir.iterdir() if d.is_dir()]
    
    print("\nAvailable Companies:")
    print("-" * 80)
    
    print("\nPrimary Competitors:")
    for company in sorted(primary_companies):
        print(f"  - {company}")
    
    print("\nAdjacent Competitors:")
    for company in sorted(adjacent_companies):
        print(f"  - {company}")
    
    print("\nTotal: {} companies ({} primary, {} adjacent)".format(
        len(primary_companies) + len(adjacent_companies),
        len(primary_companies),
        len(adjacent_companies)
    ))

def process_raw_data(args):
    """Process raw data into structured format"""
    if not args.company:
        print("Error: Company name is required.")
        return
    
    if not args.source_type:
        print("Error: Source type is required (pdf or web).")
        return
    
    company_name = args.company
    source_type = args.source_type.lower()
    is_primary = not args.adjacent
    
    # Determine directories
    category = "primary" if is_primary else "adjacent"
    raw_dir = RAW_DIR / "competitors" / category / company_name
    processed_dir = PROCESSED_DIR / "competitors" / category / company_name
    
    # Ensure directories exist
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    if source_type == "pdf":
        # Process PDF files
        pdf_files = list(raw_dir.glob("**/*.pdf"))
        if not pdf_files:
            print(f"No PDF files found for {company_name}")
            return
        
        print(f"Processing {len(pdf_files)} PDF files for {company_name}...")
        for pdf_file in pdf_files:
            print(f"  - {pdf_file.name}")
            output_path = processed_dir / f"{pdf_file.stem}_extracted.json"
            extract_from_pdf(pdf_file, output_path)
        
        print("PDF processing complete.")
    
    elif source_type == "web":
        # Process web data
        web_data_dir = raw_dir / "web_data"
        web_files = list(web_data_dir.glob("*.json")) if web_data_dir.exists() else []
        
        if not web_files:
            print(f"No web data found for {company_name}")
            return
        
        print(f"Processing web data for {company_name}...")
        
        # Simply copy web data to processed directory
        for web_file in web_files:
            print(f"  - {web_file.name}")
            output_path = processed_dir / f"{web_file.stem}_processed.json"
            with open(web_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        
        print("Web data processing complete.")
    
    else:
        print(f"Unknown source type: {source_type}")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Constructiv AI Competitive Analysis Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Extract PDF command
    pdf_parser = subparsers.add_parser("extract-pdf", help="Extract data from a PDF file")
    pdf_parser.add_argument("pdf_path", help="Path to the PDF file")
    pdf_parser.add_argument("-o", "--output-path", help="Path to save the extracted data")
    pdf_parser.set_defaults(func=extract_pdf)
    
    # Scrape website command
    web_parser = subparsers.add_parser("scrape-website", help="Scrape data from a competitor website")
    web_parser.add_argument("url", help="Website URL to scrape")
    web_parser.add_argument("-o", "--output-path", help="Path to save the scraped data")
    web_parser.set_defaults(func=scrape_website)
    
    # Process raw data command
    process_parser = subparsers.add_parser("process", help="Process raw data into structured format")
    process_parser.add_argument("company", help="Company name")
    process_parser.add_argument("source_type", help="Source type (pdf or web)")
    process_parser.add_argument("--adjacent", action="store_true", help="Process as adjacent competitor")
    process_parser.set_defaults(func=process_raw_data)
    
    # Generate analysis command
    analysis_parser = subparsers.add_parser("analyze", help="Generate analysis for companies")
    analysis_parser.add_argument("companies", help="Comma-separated list of company names")
    analysis_parser.add_argument("--adjacent", action="store_true", help="Analyze as adjacent competitors")
    analysis_parser.add_argument("--summary", action="store_true", help="Print executive summary")
    analysis_parser.set_defaults(func=generate_analysis)
    
    # Generate Excel command
    excel_parser = subparsers.add_parser("excel", help="Generate Excel outputs")
    excel_parser.add_argument("companies", help="Comma-separated list of company names")
    excel_parser.add_argument("-o", "--output-path", help="Path to save the Excel file")
    excel_parser.add_argument("--landscape", action="store_true", help="Generate competitive landscape Excel")
    excel_parser.set_defaults(func=create_excel)
    
    # Generate visualization command
    viz_parser = subparsers.add_parser("visualize", help="Generate visualizations")
    viz_parser.add_argument("chart_type", choices=["funding_timeline", "market_positioning", "funding_comparison", "tech_comparison"], 
                          help="Type of chart to create")
    viz_parser.add_argument("companies", help="Comma-separated list of company names")
    viz_parser.add_argument("-o", "--output-path", help="Path to save the visualization")
    viz_parser.set_defaults(func=create_viz)
    
    # List companies command
    list_parser = subparsers.add_parser("list", help="List available companies")
    list_parser.set_defaults(func=list_companies)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if setup is correct
    if not check_setup():
        sys.exit(1)
    
    # Run the specified command
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 