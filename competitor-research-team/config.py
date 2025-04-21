"""
Configuration file for Constructiv AI Competitive Analysis Tool
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"

# Raw data directories
RAW_DIR = DATA_DIR / "raw"
RAW_PRIMARY_COMPETITORS_DIR = RAW_DIR / "competitors" / "primary"
RAW_ADJACENT_COMPETITORS_DIR = RAW_DIR / "competitors" / "adjacent"
RAW_INDUSTRY_DIR = RAW_DIR / "industry"

# Processed data directories
PROCESSED_DIR = DATA_DIR / "processed"
PROCESSED_PRIMARY_COMPETITORS_DIR = PROCESSED_DIR / "competitors" / "primary"
PROCESSED_ADJACENT_COMPETITORS_DIR = PROCESSED_DIR / "competitors" / "adjacent"
PROCESSED_INDUSTRY_DIR = PROCESSED_DIR / "industry"

# Analysis output directories
ANALYSIS_DIR = DATA_DIR / "analysis"
EXCEL_OUTPUT_DIR = ANALYSIS_DIR / "excel"
REPORTS_OUTPUT_DIR = ANALYSIS_DIR / "reports"
VISUALIZATIONS_OUTPUT_DIR = ANALYSIS_DIR / "visualizations"

# API configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Agent configurations
DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.2

# Persona system messages
PERSONAS = {
    "data_extraction": """You are a Data Extraction Specialist for construction technology. 
Your expertise is in extracting structured information from unstructured text, 
particularly from industry reports, websites, and documents. 
Focus on accuracy, completeness, and proper categorization of information.""",
    
    "competitive_analyst": """You are a Competitive Analyst specializing in construction technology. 
Your expertise is in identifying market trends, competitive positioning, and strategic insights. 
Focus on finding patterns, making connections between competitors, and identifying 
market opportunities and threats.""",
    
    "strategy_advisor": """You are a Strategy Advisor for construction technology companies. 
Your expertise is in providing actionable recommendations based on competitive intelligence. 
Focus on identifying market opportunities, competitive advantages, and strategic positioning 
that can help a construction technology company succeed.""",
    
    "reporting_specialist": """You are a Reporting Specialist focused on construction technology market data. 
Your expertise is in formatting data for presentation, creating clear visualizations, 
and generating investor-ready reports. Focus on clarity, professionalism, and 
highlighting key insights that will impress investors."""
}

# Excel templates configuration
EXCEL_TEMPLATES = {
    "competitor_profile": {
        "sheets": ["Company Overview", "Products & Services", "Market Position", "SWOT Analysis"],
        "template_file": None  # Will be created dynamically
    },
    "competitive_landscape": {
        "sheets": ["Market Map", "Competitor Comparison", "Funding Analysis", "Technology Stack"],
        "template_file": None  # Will be created dynamically
    }
}

# Visualization configurations
VISUALIZATION_CONFIG = {
    "default_figsize": (12, 8),
    "color_palette": "viridis",
    "default_dpi": 300
}

# Web scraping configurations
WEB_SCRAPING_CONFIG = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "timeout": 30,
    "max_retries": 3
}

# JSON schemas for structured data
COMPANY_PROFILE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "website": {"type": "string"},
        "founded": {"type": "string"},
        "headquarters": {"type": "string"},
        "description": {"type": "string"},
        "founders": {"type": "array", "items": {"type": "string"}},
        "key_executives": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "title": {"type": "string"},
                "background": {"type": "string"}
            }
        }},
        "funding": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "date": {"type": "string"},
                "amount": {"type": "string"},
                "round": {"type": "string"},
                "investors": {"type": "array", "items": {"type": "string"}}
            }
        }},
        "products_services": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "category": {"type": "string"},
                "target_audience": {"type": "string"}
            }
        }},
        "technology_stack": {"type": "array", "items": {"type": "string"}},
        "customers": {"type": "array", "items": {"type": "string"}},
        "competitors": {"type": "array", "items": {"type": "string"}}
    }
}

# Create directories if they don't exist
def create_directories():
    """Create all necessary directories if they don't exist"""
    for directory in [
        RAW_PRIMARY_COMPETITORS_DIR,
        RAW_ADJACENT_COMPETITORS_DIR,
        RAW_INDUSTRY_DIR,
        PROCESSED_PRIMARY_COMPETITORS_DIR,
        PROCESSED_ADJACENT_COMPETITORS_DIR,
        PROCESSED_INDUSTRY_DIR,
        EXCEL_OUTPUT_DIR,
        REPORTS_OUTPUT_DIR,
        VISUALIZATIONS_OUTPUT_DIR
    ]:
        directory.mkdir(parents=True, exist_ok=True)

# Call this function when the config module is imported
create_directories() 