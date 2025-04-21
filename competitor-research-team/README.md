# Constructiv AI Competitive Analysis Tool

A powerful AI-powered system for automating competitive intelligence gathering and analysis for the construction technology industry.

## Overview

This tool helps you:

1. Extract structured data from CB Insights reports and competitor websites
2. Analyze competitor information to identify market positioning and strategic insights
3. Generate professional Excel workbooks and visualizations for investor presentations
4. Produce strategic recommendations based on competitive intelligence

## Architecture

The system uses a lightweight single-agent approach with specialized prompting to perform different analysis tasks. It employs the OpenAI API (GPT-4) to analyze data, identify patterns, and generate insights.

### Key Components

- **PDF Extraction Tool**: Extracts structured data from PDF reports
- **Web Scraping Tool**: Gathers information from competitor websites
- **Excel Generation Tool**: Creates standardized Excel outputs
- **Visualization Tool**: Generates charts and graphs
- **Competitive Analysis Agent**: Uses AI to analyze and compare competitors

## Installation

### Prerequisites

- Python 3.9 or higher
- OpenAI API key

### Setup

1. Clone this repository:
```bash
git clone https://github.com/your-username/competitor-research-team.git
cd competitor-research-team
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:
```bash
cp .env.example .env
# Edit .env file and add your API key
```

## Usage

The tool provides a simple command-line interface for all operations:

### Extracting Data from PDF Reports

```bash
python -m src.ui.cli extract-pdf path/to/report.pdf
```

### Scraping Competitor Websites

```bash
python -m src.ui.cli scrape-website https://competitor-website.com
```

### Processing Raw Data

```bash
python -m src.ui.cli process company_name pdf
python -m src.ui.cli process company_name web
```

### Analyzing Competitors

```bash
python -m src.ui.cli analyze company1,company2,company3 --summary
```

### Generating Excel Reports

```bash
# Single company profile
python -m src.ui.cli excel company_name

# Competitive landscape
python -m src.ui.cli excel company1,company2,company3 --landscape
```

### Creating Visualizations

```bash
python -m src.ui.cli visualize funding_comparison company1,company2,company3
```

Available chart types:
- `funding_timeline`: Compare funding history across companies
- `market_positioning`: Create a positioning map
- `funding_comparison`: Compare total funding amounts
- `tech_comparison`: Compare technology stacks

### Listing Available Companies

```bash
python -m src.ui.cli list
```

## Data Structure

The system organizes data in a hierarchical structure:

```
data/
├── raw/                        # Raw data from PDFs and websites
│   ├── competitors/
│   │   ├── primary/            # Direct competitors
│   │   └── adjacent/           # Related/adjacent competitors
│   └── industry/               # Industry-wide data
├── processed/                  # Standardized data after processing
│   ├── competitors/
│   │   ├── primary/
│   │   └── adjacent/
│   └── industry/
└── analysis/                   # Generated analysis outputs
    ├── excel/                  # Excel workbooks
    ├── reports/                # Analysis reports
    └── visualizations/         # Charts and graphs
```

## Key Features

1. **Automated Extraction**: Extract structured information from PDFs and websites
2. **AI-Powered Analysis**: Leverage GPT-4 to identify patterns and generate insights
3. **Excel Report Generation**: Create professional investor-ready Excel workbooks
4. **Data Visualization**: Generate charts and graphs to visualize the competitive landscape
5. **Strategic Recommendations**: Get AI-generated strategic recommendations based on competitive data

## Future Enhancements

- Web-based UI using Streamlit
- Automated monitoring of competitor websites for changes
- Integration with other business intelligence tools
- Advanced visualization dashboards
- PDF report generation 