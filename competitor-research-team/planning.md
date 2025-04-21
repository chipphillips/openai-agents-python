# AI System for Construction Tech Competitive Analysis
## Lightweight Single-Agent Implementation Plan

## Overview

This document outlines the implementation approach for a lightweight, single-agent AI system to automate competitive intelligence gathering and analysis for Constructiv AI. The goal is to create an efficient system that can process competitor data from CB Insights and other sources to inform strategic decision-making and provide investors with science-backed market analysis.

## Strategic Goals

1. **Automate data extraction** from CB Insights reports and web sources
2. **Standardize competitor information** into structured formats
3. **Identify competitive clusters** and market positioning
4. **Generate strategic insights** and recommendations
5. **Produce investor-ready visualizations** and Excel workbooks

## System Architecture

### Core Components

1. **Central AI Agent**
   - Powered by GPT-4 with specialized prompting
   - Handles all analysis tasks through different prompt templates
   - Maintains conversation context for multi-step analysis

2. **Function Tools**
   - PDF Extraction Tool: Converts PDF reports to structured text
   - Excel Generation Tool: Creates standardized Excel outputs
   - Web Scraping Tool: Gathers basic website information
   - Visualization Tool: Generates charts and graphs

3. **User Interface**
   - Simple command-line interface initially
   - Optional Streamlit web interface in later phase

4. **Storage System**
   - Organized file directory structure
   - JSON for intermediate data storage
   - Git for version control

## Implementation Details

### 1. Central AI Agent Design

The core of the system will be a single AI agent with specialized instructions for different analysis tasks. This agent will use context switching between different "expert personas" rather than actually using separate agents.

**Agent Personas:**
- **Data Extraction Specialist**: Extracts structured data from text
- **Competitive Analyst**: Identifies key insights and competitor positioning
- **Strategy Advisor**: Generates recommendations based on competitive data
- **Reporting Specialist**: Formats data for presentation

**Core Prompt Template:**
```
You are an AI assistant specialized in construction technology competitive analysis. You help analyze CB Insights reports and other sources to extract valuable competitive intelligence.

Based on the current task, you will adopt one of these expert personas:
1. Data Extraction Specialist: When extracting structured data from text
2. Competitive Analyst: When identifying insights and positioning
3. Strategy Advisor: When generating strategic recommendations
4. Reporting Specialist: When formatting data for presentation

Current task: {task_description}

Current persona: {current_persona}

Additional context: {context}

User query: {query}
```

### 2. Function Tool Implementation

The system will leverage several Python functions that the AI agent can "call" to perform specific tasks:

#### PDF Extraction Tool
```python
def extract_from_pdf(pdf_path):
    """
    Extract structured text from PDF maintaining hierarchical information.
    
    Parameters:
    - pdf_path: Path to the PDF file
    
    Returns:
    - Dictionary with structured content
    """
    # Implementation using PyMuPDF (fitz)
    # Will preserve headings, paragraphs, and tables
    # ...
```

#### Excel Generation Tool
```python
def generate_excel(competitor_data, template_name, output_path):
    """
    Generate a formatted Excel workbook with competitor data.
    
    Parameters:
    - competitor_data: Dictionary of competitor information
    - template_name: Which Excel template to use
    - output_path: Where to save the file
    
    Returns:
    - Path to generated Excel file
    """
    # Implementation using pandas and openpyxl
    # Will create sheets for dashboard, competitors, etc.
    # ...
```

#### Web Scraping Tool
```python
def scrape_competitor_website(url):
    """
    Extract basic information from a competitor website.
    
    Parameters:
    - url: Website URL to scrape
    
    Returns:
    - Dictionary with key website information
    """
    # Implementation using requests and BeautifulSoup
    # Will extract company description, features, etc.
    # ...
```

#### Visualization Tool
```python
def create_visualization(data, chart_type, output_path):
    """
    Generate a visualization based on competitor data.
    
    Parameters:
    - data: The data to visualize
    - chart_type: Type of chart to create
    - output_path: Where to save the image
    
    Returns:
    - Path to generated image
    """
    # Implementation using matplotlib or seaborn
    # Will create various chart types for competitive analysis
    # ...
```

### 3. Data Storage Structure

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
    ├── reports/                    # Analysis reports
    └── visualizations/             # Charts and graphs
```

### 4. Core Analysis Workflows

The system will implement several key workflows based on your competitive analysis template:

1. **Basic Company Profile Analysis**
   - Extract company profile information
   - Standardize and store in structured format
   - Generate summary profile

2. **Product and Service Analysis**
   - Extract product/service details
   - Categorize features and capabilities
   - Identify market positioning

3. **Funding and Investment Analysis**
   - Extract funding history
   - Identify key investors
   - Analyze funding trajectory

4. **Leadership Team Assessment**
   - Extract leadership information
   - Analyze team composition
   - Identify strategic implications

5. **Competitive Landscape Analysis**
   - Group related competitors
   - Identify direct vs. adjacent competitors
   - Generate positioning map

6. **Strategic Recommendations**
   - Identify market opportunities
   - Generate competitive advantage suggestions
   - Recommend strategic positioning

### 5. User Interface

Initial implementation will use a simple command-line interface:

```python
def main():
    print("Welcome to Constructiv AI Competitive Analysis Tool")
    
    while True:
        print("\nAvailable commands:")
        print("1. Analyze PDF")
        print("2. Analyze website")
        print("3. Generate Excel report")
        print("4. Generate visualization")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        # Handle different choices
        # ...
```

Optional Streamlit web interface can be added in a later phase for easier user interaction.

## Implementation Timeline

### Week 1: Core Infrastructure
- Set up project structure and data directories
- Implement PDF extraction function
- Create basic command-line interface
- Design initial prompt templates

### Week 2: Analysis Capabilities
- Implement company profile extraction
- Implement product/service analysis
- Create JSON schema for standardized data
- Build initial Excel generation tool

### Week 3: Enrichment and Integration
- Implement basic web scraping function
- Create competitor clustering logic
- Implement market positioning analysis
- Enhance Excel generation with formatting

### Week 4: Visualization and Reporting
- Implement visualization functions
- Create strategic analysis capabilities
- Build report generation feature
- Integrate all components into seamless workflow

### Week 5 (Optional): Enhancement and Testing
- Add Streamlit web interface
- Implement user feedback system
- Add additional data sources
- Comprehensive testing and refinement

## Required Technologies

- **Python 3.9+** (core programming language)
- **OpenAI API** (for GPT-4 access)
- **PyMuPDF (fitz)** (for PDF processing)
- **Pandas & Openpyxl** (for Excel generation)
- **Matplotlib/Seaborn** (for visualizations)
- **Requests & BeautifulSoup** (for web scraping)
- **Streamlit** (optional, for web interface)

## Expected Outcomes

By implementing this lightweight single-agent system, you will have:

1. An automated system to process CB Insights reports and competitor websites
2. A standardized database of competitor information
3. Strategic analysis reports with actionable insights
4. Professional Excel workbooks for investor presentations
5. Visual competitive landscape maps

## Next Steps

1. Set up development environment with required dependencies
2. Create the core file structure for data storage
3. Implement the PDF extraction function as first milestone
4. Design and test initial prompt templates
5. Begin building the command-line interface

## Future Expansion Possibilities

While starting with a lightweight approach, the system is designed to be expandable:

1. **Additional Data Sources**: Add capabilities to process more data sources
2. **Advanced Visualizations**: Implement interactive dashboards
3. **Automated Monitoring**: Add features to automatically track competitors
4. **Integration with Business Tools**: Connect with CRM or other systems
5. **Web Interface Enhancements**: Add more interactive features to the UI 