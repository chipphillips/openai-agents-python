# Agentic Team for Construction Tech Competitive Intelligence Analysis

## System Architecture Overview

A comprehensive agent-based system for converting CB Insights PDFs and web sources into structured competitive intelligence data with strategic analysis output.

## Core Components

### 1. Data Acquisition Agents

#### PDF Extraction Agent
- **Function**: Converts PDF reports to structured text while preserving hierarchical information
- **Technology**: Python with PyMuPDF (fitz) and advanced text parsing algorithms
- **Input/Output**: PDF files → Structured text documents
- **Key Features**: 
  * Multi-column recognition
  * Table structure preservation
  * Image metadata extraction
  * Heading hierarchy detection

#### Web Intelligence Agent
- **Function**: Extracts competitor data from websites, social profiles, and public databases
- **Technology**: Crawl4AI with custom configuration and rate limiting
- **Input/Output**: URLs → Structured web data JSON
- **Key Features**:
  * Dynamic content rendering
  * Anti-detection mechanisms
  * Selective data targeting
  * SERP result processing

### 2. Data Processing Agents

#### Schema Mapping Agent
- **Function**: Transforms unstructured text into standardized competitive intelligence schema
- **Technology**: Python with LLM-assisted extraction and rule-based validation
- **Input/Output**: Raw text → Structured JSON following competitive analysis schema
- **Key Features**:
  * Consistent entity recognition
  * Financial data normalization
  * Historical trend detection
  * Confidence scoring for extracted data

#### Integration Agent
- **Function**: Merges data from multiple sources with priority resolution
- **Technology**: Python with pandas and custom data reconciliation algorithms
- **Input/Output**: Multiple data sources → Unified competitor profiles
- **Key Features**:
  * Source prioritization
  * Conflict resolution
  * Data completeness assessment
  * Time-based data versioning

### 3. Analysis & Output Agents

#### Competitive Classification Agent
- **Function**: Categorizes competitors and identifies market positioning
- **Technology**: Machine learning classification with LLM analysis
- **Input/Output**: Competitor profiles → Strategic categorization
- **Key Features**:
  * Market segment assignment
  * Competitor clustering
  * Threat level assessment
  * Gap opportunity identification

#### Strategic Intelligence Agent
- **Function**: Generates high-level strategic insights and recommendations
- **Technology**: Advanced LLM with specialized prompting for strategic analysis
- **Input/Output**: Structured competitor data → Strategic analysis reports
- **Key Features**:
  * Pattern recognition across competitors
  * Investment trend analysis
  * Product differentiation assessment
  * Market opportunity identification

#### Excel Generation Agent
- **Function**: Creates professional, analyst-ready Excel workbooks
- **Technology**: Python with openpyxl for advanced Excel formatting
- **Input/Output**: Structured data → Multi-tabbed Excel workbook
- **Key Features**:
  * Custom visualization templates
  * Interactive filtering
  * Conditional formatting
  * Executive summary generation

## Centralized Data Management

### Competitor Directory Structure
```
data/
├── raw/
│   ├── competitors/                # Primary directory for all competitor data
│   │   ├── primary/                # Direct competitors
│   │   │   ├── company_A/          # Individual company directories
│   │   │   │   ├── pdf_reports/
│   │   │   │   ├── web_data/
│   │   │   │   └── metadata.json
│   │   │   └── ...
│   │   └── adjacent/               # Related/adjacent competitors
│   │       ├── company_X/
│   │       └── ...
│   └── industry/                   # Industry-wide data
├── processed/                      # Standardized data after processing
│   ├── competitors/
│   │   ├── primary/
│   │   └── adjacent/
│   └── industry/
└── analysis/                       # Generated analysis outputs
    ├── excel/                      # Excel workbooks
    ├── reports/                    # Strategic analysis documents
    └── visualizations/             # Competitive landscape visualizations
```

### Central Spreadsheet Management
- **Master Data File**: `competitive_intelligence.xlsx`
- **Update Protocol**: Incremental, source-tracked updates via centralized agent
- **Version Control**: Git-based history with automatic commit messages
- **Access Control**: Role-based permissions for different agent operations

## Implementation Workflow

### 1. Initial Setup
```python
# setup.py
import os
import json
from pathlib import Path

def create_directory_structure(base_dir):
    """Create standardized directory structure for competitor analysis."""
    directories = [
        "raw/competitors/primary",
        "raw/competitors/adjacent",
        "raw/industry",
        "processed/competitors/primary",
        "processed/competitors/adjacent",
        "processed/industry",
        "analysis/excel",
        "analysis/reports",
        "analysis/visualizations"
    ]
    
    for directory in directories:
        Path(os.path.join(base_dir, directory)).mkdir(parents=True, exist_ok=True)
    
    # Create initial configuration file
    config = {
        "version": "1.0.0",
        "primary_competitors": [],
        "adjacent_competitors": [],
        "last_updated": "",
        "excel_master_file": "competitive_intelligence.xlsx",
        "schema_version": "1.0.0"
    }
    
    with open(os.path.join(base_dir, "config.json"), 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Directory structure and configuration initialized at: {base_dir}")

if __name__ == "__main__":
    base_dir = "path/to/competitive_intelligence_data"
    create_directory_structure(base_dir)
```

### 2. PDF Processing Pipeline

```python
# pdf_processing_pipeline.py
import os
import fitz
import json
import time
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pdf_processing.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("PDFProcessor")

class PDFProcessor:
    """Enhanced PDF extraction with multi-level content analysis."""
    
    def __init__(self, config_path, threads=4):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.base_dir = os.path.dirname(config_path)
        self.threads = threads
        self.competitor_types = ["primary", "adjacent"]
    
    def extract_text_with_structure(self, pdf_path):
        """Extract text while preserving structural elements."""
        try:
            doc = fitz.open(pdf_path)
            structured_content = {
                "metadata": {
                    "title": doc.metadata.get("title", ""),
                    "author": doc.metadata.get("author", ""),
                    "subject": doc.metadata.get("subject", ""),
                    "keywords": doc.metadata.get("keywords", ""),
                    "page_count": len(doc),
                    "creation_date": str(doc.metadata.get("creationDate", "")),
                },
                "content": []
            }
            
            # Process each page
            for page_num, page in enumerate(doc):
                # Extract text with layout recognition
                blocks = page.get_text("dict")["blocks"]
                page_content = {
                    "page_number": page_num + 1,
                    "sections": []
                }
                
                # Process blocks to identify sections
                current_section = None
                for block in blocks:
                    if block["type"] == 0:  # Text block
                        # Check if this is a heading based on font size
                        is_heading = False
                        for line in block["lines"]:
                            for span in line["spans"]:
                                if span["size"] > 12:  # Assume larger text is heading
                                    is_heading = True
                                    current_section = {
                                        "heading": span["text"],
                                        "content": [],
                                        "level": self._determine_heading_level(span["size"])
                                    }
                                    page_content["sections"].append(current_section)
                                    break
                            if is_heading:
                                break
                        
                        # If not a heading, add content to current section
                        if not is_heading and current_section:
                            text = ""
                            for line in block["lines"]:
                                for span in line["spans"]:
                                    text += span["text"] + " "
                                text += "\n"
                            current_section["content"].append(text.strip())
                
                structured_content["content"].append(page_content)
            
            return structured_content
        
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {str(e)}")
            raise
    
    def _determine_heading_level(self, font_size):
        """Determine heading level based on font size."""
        if font_size > 18:
            return 1
        elif font_size > 16:
            return 2
        elif font_size > 14:
            return 3
        else:
            return 4
    
    def process_competitor_pdfs(self, competitor_type, competitor_name):
        """Process all PDFs for a specific competitor."""
        pdf_dir = os.path.join(self.base_dir, "raw", "competitors", competitor_type, competitor_name, "pdf_reports")
        output_dir = os.path.join(self.base_dir, "processed", "competitors", competitor_type, competitor_name)
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Get all PDF files
        pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
        if not pdf_files:
            logger.warning(f"No PDF files found for {competitor_name} in {pdf_dir}")
            return
        
        # Process each PDF
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_dir, pdf_file)
            output_file = os.path.join(output_dir, f"{os.path.splitext(pdf_file)[0]}_structured.json")
            
            # Check if already processed and not modified since
            if os.path.exists(output_file):
                pdf_mtime = os.path.getmtime(pdf_path)
                output_mtime = os.path.getmtime(output_file)
                if pdf_mtime <= output_mtime:
                    logger.info(f"Skipping {pdf_file} as it's already processed and not modified")
                    continue
            
            logger.info(f"Processing {pdf_file} for {competitor_name}")
            try:
                start_time = time.time()
                structured_content = self.extract_text_with_structure(pdf_path)
                
                # Save structured content
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(structured_content, f, indent=2)
                
                elapsed_time = time.time() - start_time
                logger.info(f"Processed {pdf_file} in {elapsed_time:.2f} seconds")
            
            except Exception as e:
                logger.error(f"Failed to process {pdf_file}: {str(e)}")
    
    def process_all_competitors(self):
        """Process PDFs for all competitors."""
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for competitor_type in self.competitor_types:
                competitor_dir = os.path.join(self.base_dir, "raw", "competitors", competitor_type)
                if not os.path.exists(competitor_dir):
                    logger.warning(f"Directory not found: {competitor_dir}")
                    continue
                
                competitors = [d for d in os.listdir(competitor_dir) if os.path.isdir(os.path.join(competitor_dir, d))]
                for competitor in competitors:
                    executor.submit(self.process_competitor_pdfs, competitor_type, competitor)

if __name__ == "__main__":
    config_path = "path/to/competitive_intelligence_data/config.json"
    processor = PDFProcessor(config_path)
    processor.process_all_competitors()
```

### 3. Central Excel Updater

```python
# excel_updater.py
import os
import json
import pandas as pd
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("excel_updater.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ExcelUpdater")

class ExcelUpdater:
    """Updates the master Excel file with latest competitor data."""
    
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.base_dir = os.path.dirname(config_path)
        self.excel_path = os.path.join(
            self.base_dir, 
            "analysis", 
            "excel", 
            self.config["excel_master_file"]
        )
        
        # Create or load the workbook
        if not os.path.exists(self.excel_path):
            self._create_initial_workbook()
        else:
            self.workbook = load_workbook(self.excel_path)
    
    def _create_initial_workbook(self):
        """Create a new Excel workbook with all required sheets."""
        self.workbook = Workbook()
        
        # Define sheets
        sheets = [
            "Dashboard",
            "Primary Competitors",
            "Adjacent Competitors",
            "Funding Details",
            "Product Offerings",
            "Market Positioning",
            "Leadership & Investors",
            "Strategic Analysis"
        ]
        
        # Set up all sheets
        default_sheet = self.workbook.active
        default_sheet.title = sheets[0]
        
        for sheet_name in sheets[1:]:
            self.workbook.create_sheet(sheet_name)
        
        # Apply basic formatting to all sheets
        for sheet_name in sheets:
            sheet = self.workbook[sheet_name]
            
            # Apply column widths
            for col in range(1, 20):
                sheet.column_dimensions[chr(64 + col)].width = 15
            
            # Style header row
            header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF", size=12)
            header_alignment = Alignment(horizontal="center", vertical="center")
            
            # Setup common headers based on sheet type
            if sheet_name == "Dashboard":
                headers = ["Competitor", "Type", "Founded", "HQ", "Funding", "Latest Round", "Valuation", "Key Products", "Target Market"]
            elif sheet_name in ["Primary Competitors", "Adjacent Competitors"]:
                headers = ["Company", "Website", "Founded", "HQ", "Total Funding", "Latest Round", "Valuation", "Key Products", "Target Market", "Differentiator"]
            elif sheet_name == "Funding Details":
                headers = ["Company", "Type", "Total Funding", "Last Round", "Last Round Date", "Last Round Amount", "Notable Investors", "Total Rounds"]
            elif sheet_name == "Product Offerings":
                headers = ["Company", "Type", "Product Name", "Category", "Key Features", "Pricing Model", "Target Segment", "USP"]
            elif sheet_name == "Market Positioning":
                headers = ["Company", "Type", "Target Industry", "Customer Size", "Geographic Focus", "Value Proposition", "Go-to-Market", "Competitive Advantage"]
            elif sheet_name == "Leadership & Investors":
                headers = ["Company", "Type", "CEO", "Leadership Team", "Board", "Lead Investors", "Total Investors", "Notable Exits"]
            elif sheet_name == "Strategic Analysis":
                headers = ["Category", "Insight", "Implications", "Opportunity/Threat", "Recommended Action"]
            
            # Apply headers
            for col, header in enumerate(headers, 1):
                cell = sheet.cell(row=1, column=col, value=header)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
        
        # Save the workbook
        self.workbook.save(self.excel_path)
        logger.info(f"Created new Excel workbook at {self.excel_path}")
    
    def update_competitor_data(self, competitor_type, competitor_name):
        """Update Excel with the latest data for a specific competitor."""
        competitor_dir = os.path.join(
            self.base_dir, 
            "processed", 
            "competitors", 
            competitor_type, 
            competitor_name
        )
        
        if not os.path.exists(competitor_dir):
            logger.warning(f"Processed directory not found for {competitor_name}")
            return
        
        # Collect all processed data files
        data_files = [f for f in os.listdir(competitor_dir) if f.endswith('_structured.json') or f.endswith('_enhanced.json')]
        
        if not data_files:
            logger.warning(f"No processed data files found for {competitor_name}")
            return
        
        # Aggregate data from all files
        competitor_data = self._aggregate_competitor_data(competitor_dir, data_files)
        
        # Update relevant sheets
        self._update_dashboard(competitor_data, competitor_type)
        self._update_competitor_sheet(competitor_data, competitor_type)
        self._update_funding_details(competitor_data, competitor_type)
        self._update_product_offerings(competitor_data, competitor_type)
        self._update_market_positioning(competitor_data, competitor_type)
        self._update_leadership_investors(competitor_data, competitor_type)
        
        logger.info(f"Updated Excel data for {competitor_name}")
    
    def _aggregate_competitor_data(self, competitor_dir, data_files):
        """Aggregate data from multiple files into a consolidated competitor profile."""
        aggregated_data = {
            "company_name": "",
            "website": "",
            "overview": {
                "description": "",
                "founded": "",
                "funding": "",
                "valuation": "",
                "headquarters": "",
            },
            "products": [],
            "funding_rounds": [],
            "investors": [],
            "leadership": [],
            "market_focus": {
                "target_industry": "",
                "customer_size": "",
                "geographic_focus": "",
                "value_proposition": ""
            }
        }
        
        # Process each file and merge data
        for file_name in data_files:
            file_path = os.path.join(competitor_dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
            
            # Update aggregated data based on file content
            # This would be a more complex merge logic in a real implementation
            if "company_name" in file_data and file_data["company_name"]:
                aggregated_data["company_name"] = file_data["company_name"]
            
            if "overview" in file_data:
                for key in aggregated_data["overview"]:
                    if key in file_data["overview"] and file_data["overview"][key]:
                        aggregated_data["overview"][key] = file_data["overview"][key]
            
            # Similar logic for other data sections
        
        return aggregated_data
    
    def _update_dashboard(self, competitor_data, competitor_type):
        """Update the Dashboard sheet with the latest competitor data."""
        sheet = self.workbook["Dashboard"]
        
        # Find if competitor already exists
        company_name = competitor_data["company_name"]
        existing_row = None
        
        for row in range(2, sheet.max_row + 1):
            if sheet.cell(row=row, column=1).value == company_name:
                existing_row = row
                break
        
        # If not found, add at the end
        if not existing_row:
            existing_row = sheet.max_row + 1
        
        # Update data
        sheet.cell(row=existing_row, column=1, value=company_name)
        sheet.cell(row=existing_row, column=2, value=competitor_type.capitalize())
        sheet.cell(row=existing_row, column=3, value=competitor_data["overview"]["founded"])
        sheet.cell(row=existing_row, column=4, value=competitor_data["overview"]["headquarters"])
        sheet.cell(row=existing_row, column=5, value=competitor_data["overview"]["funding"])
        
        # Latest round would come from funding_rounds
        latest_round = "N/A"
        if competitor_data["funding_rounds"]:
            latest_round = sorted(competitor_data["funding_rounds"], key=lambda x: x.get("date", ""), reverse=True)[0]
            latest_round = f"{latest_round.get('date', '')} - {latest_round.get('round_type', '')}"
        
        sheet.cell(row=existing_row, column=6, value=latest_round)
        sheet.cell(row=existing_row, column=7, value=competitor_data["overview"]["valuation"])
        
        # Key products
        products = ", ".join([p.get("name", "") for p in competitor_data["products"][:3]])
        sheet.cell(row=existing_row, column=8, value=products)
        
        # Target market
        target_market = f"{competitor_data['market_focus']['target_industry']} - {competitor_data['market_focus']['customer_size']}"
        sheet.cell(row=existing_row, column=9, value=target_market)
    
    def _update_competitor_sheet(self, competitor_data, competitor_type):
        """Update the primary or adjacent competitor sheet."""
        sheet_name = f"{competitor_type.capitalize()} Competitors"
        sheet = self.workbook[sheet_name]
        
        # Implementation similar to _update_dashboard
        # Would include more detailed competitor information
    
    def _update_funding_details(self, competitor_data, competitor_type):
        """Update the Funding Details sheet."""
        # Implementation for updating funding details
        pass
    
    def _update_product_offerings(self, competitor_data, competitor_type):
        """Update the Product Offerings sheet."""
        # Implementation for updating product offerings
        pass
    
    def _update_market_positioning(self, competitor_data, competitor_type):
        """Update the Market Positioning sheet."""
        # Implementation for updating market positioning
        pass
    
    def _update_leadership_investors(self, competitor_data, competitor_type):
        """Update the Leadership & Investors sheet."""
        # Implementation for updating leadership and investors
        pass
    
    def update_all_competitors(self):
        """Update Excel with data for all competitors."""
        for competitor_type in ["primary", "adjacent"]:
            competitor_dir = os.path.join(self.base_dir, "processed", "competitors", competitor_type)
            if not os.path.exists(competitor_dir):
                logger.warning(f"Directory not found: {competitor_dir}")
                continue
            
            competitors = [d for d in os.listdir(competitor_dir) if os.path.isdir(os.path.join(competitor_dir, d))]
            for competitor in competitors:
                self.update_competitor_data(competitor_type, competitor)
        
        # Save the workbook after all updates
        self.workbook.save(self.excel_path)
        logger.info(f"Excel workbook updated successfully")

if __name__ == "__main__":
    config_path = "path/to/competitive_intelligence_data/config.json"
    updater = ExcelUpdater(config_path)
    updater.update_all_competitors()
```

### 4. Main Quality Control Agent

```python
# quality_control_agent.py
import os
import json
import logging
import datetime
import subprocess
import openai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("quality_control.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("QualityControlAgent")

class QualityControlAgent:
    """Oversees the complete competitive intelligence process and ensures output quality."""
    
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.base_dir = os.path.dirname(config_path)
        openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    def run_pipeline(self):
        """Execute the complete competitive intelligence pipeline with quality checks."""
        logger.info("Starting competitive intelligence pipeline")
        
        # 1. PDF processing
        logger.info("Step 1: Processing PDF documents")
        self._run_process("pdf_processing_pipeline.py", self.base_dir)
        
        # 2. Web data extraction
        logger.info("Step 2: Extracting web intelligence")
        self._run_process("web_intelligence_pipeline.py", self.base_dir)
        
        # 3. Data integration
        logger.info("Step 3: Integrating data sources")
        self._run_process("data_integration_pipeline.py", self.base_dir)
        
        # 4. Excel generation
        logger.info("Step 4: Updating Excel workbook")
        self._run_process("excel_updater.py", self.base_dir)
        
        # 5. Strategic analysis
        logger.info("Step 5: Generating strategic analysis")
        self._run_process("strategic_analyzer.py", self.base_dir)
        
        # 6. Quality control
        logger.info("Step 6: Performing quality control checks")
        quality_report = self._perform_quality_checks()
        
        # 7. Update configuration with timestamp
        self._update_configuration()
        
        logger.info("Competitive intelligence pipeline completed")
        return quality_report
    
    def _run_process(self, script_name, working_dir):
        """Run a Python script as a subprocess."""
        try:
            result = subprocess.run(
                ["python", script_name],
                cwd=working_dir,
                check=True,
                capture_output=True,
                text=True
            )
            logger.info(f"Successfully ran {script_name}")
            logger.debug(f"Output: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running {script_name}: {e}")
            logger.error(f"Error output: {e.stderr}")
            return False
    
    def _perform_quality_checks(self):
        """Perform quality checks on generated data and outputs."""
        quality_report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "excel_validation": self._validate_excel(),
            "data_completeness": self._check_data_completeness(),
            "strategic_analysis_review": self._review_strategic_analysis(),
            "overall_status": "Pending"
        }
        
        # Determine overall status
        all_passed = all([
            quality_report["excel_validation"]["status"] == "Pass",
            quality_report["data_completeness"]["status"] == "Pass",
            quality_report["strategic_analysis_review"]["status"] == "Pass"
        ])
        
        quality_report["overall_status"] = "Pass" if all_passed else "Fail"
        
        # Save quality report
        report_path = os.path.join(
            self.base_dir,
            "analysis",
            "quality_reports",
            f"quality_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(quality_report, f, indent=2)
        
        return quality_report
    
    def _validate_excel(self):
        """Validate the Excel workbook for completeness and formatting."""
        excel_path = os.path.join(
            self.base_dir,
            "analysis",
            "excel",
            self.config["excel_master_file"]
        )
        
        if not os.path.exists(excel_path):
            return {
                "status": "Fail",
                "message": "Excel file not found",
                "issues": ["Missing Excel workbook"]
            }
        
        # Add more sophisticated Excel validation logic here
        # For example, check for empty cells, formatting issues, etc.
        
        return {
            "status": "Pass",
            "message": "Excel validation passed",
            "issues": []
        }
    
    def _check_data_completeness(self):
        """Check for completeness of processed data."""
        issues = []
        
        # Check for primary competitors
        primary_dir = os.path.join(self.base_dir, "processed", "competitors", "primary")
        if os.path.exists(primary_dir):
            primary_competitors = [d for d in os.listdir(primary_dir) if os.path.isdir(os.path.join(primary_dir, d))]
            
            if not primary_competitors:
                issues.append("No processed data for primary competitors")
            
            for competitor in primary_competitors:
                competitor_dir = os.path.join(primary_dir, competitor)
                data_files = [f for f in os.listdir(competitor_dir) if f.endswith('_structured.json') or f.endswith('_enhanced.json')]
                
                if not data_files:
                    issues.append(f"No processed data files for primary competitor: {competitor}")
        else:
            issues.append("Primary competitors directory not found")
        
        # Similar checks for adjacent competitors
        
        status = "Pass" if not issues else "Fail"
        return {
            "status": status,
            "message": "Data completeness check " + ("passed" if status == "Pass" else "failed"),
            "issues": issues
        }
    
    def _review_strategic_analysis(self):
        """Review strategic analysis for quality and insights."""
        strategic_dir = os.path.join(self.base_dir, "analysis", "reports")
        
        if not os.path.exists(strategic_dir):
            return {
                "status": "Fail",
                "message": "Strategic analysis directory not found",
                "issues": ["Missing strategic analysis reports"]
            }
        
        report_files = [f for f in os.listdir(strategic_dir) if f.endswith('.md') or f.endswith('.txt')]
        
        if not report_files:
            return {
                "status": "Fail",
                "message": "No strategic analysis reports found",
                "issues": ["Missing strategic analysis reports"]
            }
        
        # For each report, perform a quality check using LLM
        issues = []
        for report_file in report_files:
            report_path = os.path.join(strategic_dir, report_file)
            with open(report_path, 'r', encoding='utf-8') as f:
                report_content = f.read()
            
            # Use LLM to assess report quality
            try:
                quality_assessment = self._assess_report_quality(report_file, report_content)
                if quality_assessment["overall_quality"] < 7:
                    issues.append(f"Report {report_file} received low quality score: {quality_assessment['overall_quality']}/10")
                    issues.extend(quality_assessment["improvement_suggestions"])
            except Exception as e:
                logger.error(f"Error assessing report quality: {str(e)}")
                issues.append(f"Failed to assess quality of report: {report_file}")
        
        status = "Pass" if not issues else "