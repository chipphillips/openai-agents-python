# Getting Started with the Competitive Analysis Tool

This guide will walk you through the process of setting up and using the Constructiv AI Competitive Analysis Tool for your competitive intelligence needs.

## Initial Setup

1. **Install Dependencies**

   Start by installing all required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   > **Note for Windows ARM64 users**: You may encounter compilation issues with some packages on ARM64 devices. Consider using the tool on an x64 Windows system or Linux environment for full functionality. Alternatively, you can look for pre-built wheels for ARM64 from the package maintainers or use services like [PyPI](https://pypi.org/) to find compatible versions.

2. **Configure API Key**

   Copy the example environment file and add your OpenAI API key:

   ```bash
   cp .env.example .env
   ```

   Then edit the `.env` file with your API key.

3. **Create Directory Structure**

   The system needs specific directories to store data. Run this command to create them:

   ```bash
   # If using Windows PowerShell
   mkdir -Force -p "data/raw/competitors/primary" "data/raw/competitors/adjacent" "data/raw/industry" "data/processed/competitors/primary" "data/processed/competitors/adjacent" "data/processed/industry" "data/analysis/excel" "data/analysis/reports" "data/analysis/visualizations"
   
   # If using Linux/Mac/Git Bash
   mkdir -p data/raw/competitors/primary data/raw/competitors/adjacent data/raw/industry data/processed/competitors/primary data/processed/competitors/adjacent data/processed/industry data/analysis/excel data/analysis/reports data/analysis/visualizations
   ```

4. **Run System Test**

   Verify your setup is working correctly:

   ```bash
   python test_system.py
   ```

   This will confirm that your directories, imports, and API connection are all functioning properly.

## Where to Add PDF Files

PDF reports should be placed in specific directories based on the competitor type:

1. **Create competitor directories**:

   ```bash
   # For a primary competitor (direct competitor)
   mkdir -p "data/raw/competitors/primary/competitor_name/pdf_reports"
   
   # For an adjacent competitor (indirect competitor)
   mkdir -p "data/raw/competitors/adjacent/competitor_name/pdf_reports"
   ```

   Replace `competitor_name` with the actual name of the competitor (e.g., "procore" or "buildertrend").

2. **Add PDF files** to the appropriate `pdf_reports` directory. For example:
   
   ```
   data/raw/competitors/primary/procore/pdf_reports/procore_cb_insights_2023.pdf
   ```

3. Then you can process these PDF files using the extract-pdf command as shown in the workflow below.

## Workflow for Competitive Analysis

### Step 1: Gather Raw Data

First, collect raw data about your competitors from PDF reports and websites.

#### From PDF Reports:

```bash
# Extract data from a CB Insights report
python -m src.ui.cli extract-pdf data/raw/competitors/primary/procore/pdf_reports/procore_cb_insights.pdf
```

This will extract structured data from the PDF and save it to the appropriate location in the data directory.

#### From Websites:

```bash
# Scrape data from a competitor's website
python -m src.ui.cli scrape-website https://www.procore.com
```

This will scrape publicly available information from the website and save it as structured data.

### Step 2: Process Raw Data

Process the extracted data into a standardized format:

```bash
# Process PDF data for a competitor
python -m src.ui.cli process competitor_name pdf

# Process web data for a competitor
python -m src.ui.cli process competitor_name web
```

### Step 3: Analyze Competitors

Generate analysis for individual competitors or comparative analysis for multiple competitors:

```bash
# Analyze multiple competitors and print a summary
python -m src.ui.cli analyze competitor1,competitor2,competitor3 --summary
```

The analysis results will be saved to the `data/analysis/reports` directory.

### Step 4: Generate Excel Reports

Create Excel workbooks for presentation and further analysis:

```bash
# Generate a profile for a single competitor
python -m src.ui.cli excel competitor_name

# Generate a competitive landscape for multiple competitors
python -m src.ui.cli excel competitor1,competitor2,competitor3 --landscape
```

The Excel files will be saved to the `data/analysis/excel` directory.

### Step 5: Create Visualizations

Generate visualizations to better understand the competitive landscape:

```bash
# Create a funding comparison chart
python -m src.ui.cli visualize funding_comparison competitor1,competitor2,competitor3

# Create a market positioning map
python -m src.ui.cli visualize market_positioning competitor1,competitor2,competitor3

# Create a technology stack comparison
python -m src.ui.cli visualize tech_comparison competitor1,competitor2,competitor3
```

The visualizations will be saved to the `data/analysis/visualizations` directory.

## Example Workflow

Here's a complete example workflow:

```bash
# 0. Set up directories for competitors
mkdir -p "data/raw/competitors/primary/procore/pdf_reports"
mkdir -p "data/raw/competitors/primary/buildertrend/pdf_reports"

# 1. Add your PDF files to these directories
# (Manually copy your PDF files to the directories above)

# 2. Extract data from PDFs
python -m src.ui.cli extract-pdf data/raw/competitors/primary/procore/pdf_reports/procore_cb_insights.pdf
python -m src.ui.cli extract-pdf data/raw/competitors/primary/buildertrend/pdf_reports/buildertrend_cb_insights.pdf

# 3. Scrape websites
python -m src.ui.cli scrape-website https://www.procore.com
python -m src.ui.cli scrape-website https://www.buildertrend.com

# 4. Process the raw data
python -m src.ui.cli process procore pdf
python -m src.ui.cli process procore web
python -m src.ui.cli process buildertrend pdf
python -m src.ui.cli process buildertrend web

# 5. Analyze the competitors
python -m src.ui.cli analyze procore,buildertrend --summary

# 6. Generate Excel reports
python -m src.ui.cli excel procore,buildertrend --landscape

# 7. Create visualizations
python -m src.ui.cli visualize funding_comparison procore,buildertrend
python -m src.ui.cli visualize market_positioning procore,buildertrend
```

## Managing Your Competitor Database

### Listing Available Competitors

To see which competitors are already in your database:

```bash
python -m src.ui.cli list
```

### Adding New Competitors

To add a new competitor:

1. Create directories for the raw data:

```bash
mkdir -p "data/raw/competitors/primary/new_competitor_name/pdf_reports"
mkdir -p "data/raw/competitors/primary/new_competitor_name/web_data"
```

2. Add PDF reports to the pdf_reports directory

3. Extract and process the data following the workflow above

## Troubleshooting

1. **Directory Creation Issues**: If you encounter issues creating directories with the `mkdir -p` command in PowerShell, try using the `-Force` parameter or create directories one by one.

2. **OpenAI API Key**: If the system test fails to connect to OpenAI, double-check your API key in the `.env` file.

3. **Missing PDF Reports**: If you get errors about missing PDF files, verify the paths and ensure the files exist in the specified locations.

4. **Module Import Errors**: If you encounter import errors, make sure you've installed all dependencies with `pip install -r requirements.txt`.

## Tips for Best Results

1. **Consistent Naming**: Use consistent company names across all commands.

2. **Quality Sources**: Use high-quality sources like CB Insights reports for the most reliable data.

3. **Regular Updates**: Update your competitor data regularly to keep your analysis current.

4. **Combining Data Sources**: For the most comprehensive analysis, combine data from both PDFs and websites.

5. **Verify AI Outputs**: While the AI analysis is powerful, always review the outputs for accuracy and relevance to your specific business context. 