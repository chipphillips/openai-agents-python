"""
Competitive Analysis Agent for Constructiv AI

This module provides the core AI functionality for analyzing competitor data.
It uses the OpenAI API to process extracted data and generate insights.
"""
import os
import json
from pathlib import Path
import openai
from typing import Dict, List, Any, Optional, Tuple
import time

# Import configuration
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config import PROCESSED_DIR, ANALYSIS_DIR, OPENAI_API_KEY, PERSONAS

# Set up OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

class CompetitiveAnalyst:
    """Class for analyzing competitor data using OpenAI API"""
    
    def __init__(self, model="gpt-4o"):
        """
        Initialize the competitive analyst
        
        Parameters:
        - model: Which OpenAI model to use
        """
        self.model = model
        self.messages = []
        self.current_persona = None
    
    def set_persona(self, persona_type):
        """
        Set the current persona for the analysis
        
        Parameters:
        - persona_type: Type of persona to use ('data_extraction', 'competitive_analyst', etc.)
        """
        if persona_type not in PERSONAS:
            raise ValueError(f"Unknown persona: {persona_type}")
        
        self.current_persona = persona_type
        system_message = PERSONAS[persona_type]
        
        # Reset conversation
        self.messages = [{"role": "system", "content": system_message}]
    
    def analyze_with_ai(self, prompt, temperature=0.2, max_tokens=4000):
        """
        Analyze data with the OpenAI API
        
        Parameters:
        - prompt: Text prompt for the OpenAI model
        - temperature: Creativity parameter (0.0 to 1.0)
        - max_tokens: Maximum response length
        
        Returns:
        - Response text from the model
        """
        # Add user message to conversation
        self.messages.append({"role": "user", "content": prompt})
        
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Get response content
            response_text = response.choices[0].message.content
            
            # Add assistant message to conversation
            self.messages.append({"role": "assistant", "content": response_text})
            
            return response_text
        
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None
    
    def analyze_company_profile(self, company_data):
        """
        Analyze a company profile and extract key insights
        
        Parameters:
        - company_data: Dictionary with company information
        
        Returns:
        - Dictionary with analysis results
        """
        # Set appropriate persona
        self.set_persona("competitive_analyst")
        
        # Create prompt with company information
        prompt = f"""
        Please analyze the following company profile and extract key insights.
        
        Company Name: {company_data.get('name', 'N/A')}
        Website: {company_data.get('website', 'N/A')}
        Founded: {company_data.get('founded', 'N/A')}
        Headquarters: {company_data.get('headquarters', 'N/A')}
        
        Description:
        {company_data.get('description', 'No description available.')}
        
        Products/Services:
        {json.dumps(company_data.get('products_services', []), indent=2)}
        
        Funding History:
        {json.dumps(company_data.get('funding', []), indent=2)}
        
        Please provide:
        1. A summary of the company's business model and value proposition
        2. Key strengths and weaknesses
        3. Market positioning analysis
        4. Potential threats to our business
        5. Opportunities for differentiation
        
        Format your response as JSON with the following structure:
        {{
            "business_model_summary": "text here",
            "strengths": ["strength 1", "strength 2", ...],
            "weaknesses": ["weakness 1", "weakness 2", ...],
            "market_positioning": "text here",
            "threats": ["threat 1", "threat 2", ...],
            "opportunities": ["opportunity 1", "opportunity 2", ...],
            "key_differentiators": ["differentiator 1", "differentiator 2", ...]
        }}
        """
        
        # Get analysis from OpenAI
        response = self.analyze_with_ai(prompt)
        
        # Parse JSON response
        try:
            analysis = json.loads(response)
            return analysis
        except json.JSONDecodeError:
            # If response is not valid JSON, return raw text
            return {"raw_analysis": response}
    
    def compare_competitors(self, companies_data):
        """
        Compare multiple competitors and identify patterns
        
        Parameters:
        - companies_data: List of dictionaries with company information
        
        Returns:
        - Dictionary with comparative analysis
        """
        # Set appropriate persona
        self.set_persona("competitive_analyst")
        
        # Create simplified data for comparison (to avoid token limits)
        simplified_data = []
        
        for company in companies_data:
            simplified = {
                "name": company.get("name", "Unknown"),
                "description": company.get("description", ""),
                "founded": company.get("founded", "Unknown"),
                "products": [p.get("name", "") + ": " + p.get("description", "")[:100] + "..." 
                            for p in company.get("products_services", [])[:3]],
                "funding": [{"round": f.get("round", ""), "amount": f.get("amount", "")} 
                           for f in company.get("funding", [])],
                "tech_stack": company.get("technology_stack", [])[:5]
            }
            simplified_data.append(simplified)
        
        # Create prompt with comparison request
        prompt = f"""
        Please analyze the following companies and provide a competitive comparison.
        
        Company data:
        {json.dumps(simplified_data, indent=2)}
        
        Please provide:
        1. Comparative analysis of business models and target markets
        2. Funding analysis and growth trajectory comparison
        3. Technology and product capability comparison
        4. Competitive advantage analysis for each company
        5. Market opportunity mapping
        6. Strategic grouping/clustering of the companies
        
        Format your response as JSON with the following structure:
        {{
            "business_model_comparison": "text here",
            "funding_analysis": "text here",
            "technology_comparison": "text here",
            "competitive_advantages": {{
                "company_name1": ["advantage 1", "advantage 2", ...],
                "company_name2": ["advantage 1", "advantage 2", ...],
                ...
            }},
            "market_opportunities": ["opportunity 1", "opportunity 2", ...],
            "strategic_groups": {{
                "group1": ["company1", "company2", ...],
                "group2": ["company3", "company4", ...],
                ...
            }},
            "market_positioning_scores": {{
                "company_name1": {{
                    "product_complexity": score from 0-100,
                    "market_focus_score": score from 0-100,
                    "price_point": score from 0-100,
                    "customer_size_score": score from 0-100
                }},
                ...
            }}
        }}
        """
        
        # Get analysis from OpenAI
        response = self.analyze_with_ai(prompt, temperature=0.4, max_tokens=4000)
        
        # Parse JSON response
        try:
            analysis = json.loads(response)
            return analysis
        except json.JSONDecodeError:
            # If response is not valid JSON, return raw text
            return {"raw_analysis": response}
    
    def generate_strategic_recommendations(self, comparative_analysis):
        """
        Generate strategic recommendations based on competitive analysis
        
        Parameters:
        - comparative_analysis: Output from compare_competitors method
        
        Returns:
        - Dictionary with strategic recommendations
        """
        # Set appropriate persona
        self.set_persona("strategy_advisor")
        
        # Create prompt with request for strategic recommendations
        prompt = f"""
        Based on the following competitive analysis, please provide strategic recommendations for our construction technology company.
        
        Competitive Analysis:
        {json.dumps(comparative_analysis, indent=2)}
        
        Please provide:
        1. Strategic positioning recommendations
        2. Product differentiation opportunities
        3. Market entry or expansion strategies
        4. Technology investment recommendations
        5. Partnership or acquisition opportunities
        6. Key metrics to track for competitive intelligence
        
        Format your response as JSON with the following structure:
        {{
            "strategic_positioning": "text here",
            "product_differentiation": ["opportunity 1", "opportunity 2", ...],
            "market_strategies": ["strategy 1", "strategy 2", ...],
            "technology_investments": ["investment 1", "investment 2", ...],
            "partnership_opportunities": ["opportunity 1", "opportunity 2", ...],
            "key_metrics": ["metric 1", "metric 2", ...]
        }}
        """
        
        # Get recommendations from OpenAI
        response = self.analyze_with_ai(prompt, temperature=0.4)
        
        # Parse JSON response
        try:
            recommendations = json.loads(response)
            return recommendations
        except json.JSONDecodeError:
            # If response is not valid JSON, return raw text
            return {"raw_recommendations": response}
    
    def extract_structured_data(self, raw_text, data_type="company_profile"):
        """
        Extract structured data from raw text
        
        Parameters:
        - raw_text: Raw text to process
        - data_type: Type of data to extract ('company_profile', 'product_details', etc.)
        
        Returns:
        - Dictionary with structured data
        """
        # Set appropriate persona
        self.set_persona("data_extraction")
        
        # Create schema based on data type
        schema = {
            "company_profile": {
                "name": "Company name",
                "website": "Website URL",
                "founded": "Year founded",
                "headquarters": "Company headquarters location",
                "description": "Company description",
                "funding": [
                    {
                        "date": "Funding date",
                        "round": "Funding round (Seed, Series A, etc.)",
                        "amount": "Funding amount",
                        "investors": ["Investor names"]
                    }
                ],
                "products_services": [
                    {
                        "name": "Product name",
                        "description": "Product description",
                        "category": "Product category",
                        "target_audience": "Target audience"
                    }
                ],
                "key_executives": [
                    {
                        "name": "Executive name",
                        "title": "Executive title",
                        "background": "Professional background"
                    }
                ],
                "competitors": ["Competitor names"],
                "technology_stack": ["Technologies used"]
            },
            "product_details": {
                "name": "Product name",
                "version": "Current version",
                "release_date": "Release date",
                "description": "Product description",
                "features": ["Feature descriptions"],
                "pricing": {
                    "model": "Pricing model (subscription, one-time, etc.)",
                    "tiers": [
                        {
                            "name": "Tier name",
                            "price": "Price",
                            "features": ["Features included"]
                        }
                    ]
                },
                "target_audience": "Target audience description",
                "use_cases": ["Primary use cases"]
            }
        }
        
        # Create prompt with extraction request
        prompt = f"""
        Please extract structured information from the following text according to the specified schema.
        Try to fill in as many fields as possible based on the information provided.
        If information for a field is not available, use empty string, empty list, or appropriate default.
        
        TEXT TO PROCESS:
        ```
        {raw_text[:10000]}  # Limit to avoid token issues
        ```
        
        SCHEMA TO EXTRACT ({data_type}):
        {json.dumps(schema.get(data_type, {}), indent=2)}
        
        Return ONLY the extracted data as a valid JSON object following the schema structure.
        """
        
        # Get structured data from OpenAI
        response = self.analyze_with_ai(prompt, temperature=0.1)
        
        # Parse JSON response
        try:
            extracted_data = json.loads(response)
            return extracted_data
        except json.JSONDecodeError:
            # If response is not valid JSON, return raw text
            return {"raw_extraction": response}
    
    def generate_report(self, analysis_data, report_type="executive_summary"):
        """
        Generate a formatted report based on analysis data
        
        Parameters:
        - analysis_data: Dictionary with analysis results
        - report_type: Type of report to generate
        
        Returns:
        - Formatted report text
        """
        # Set appropriate persona
        self.set_persona("reporting_specialist")
        
        # Create prompt with report request
        prompt = f"""
        Please generate a {report_type} based on the following competitive analysis data.
        
        Analysis Data:
        {json.dumps(analysis_data, indent=2)}
        
        For an executive summary, include:
        1. Overview of the competitive landscape
        2. Key findings and insights
        3. Strategic implications
        4. Recommended next steps
        
        Format the report in a professional, concise style suitable for executives.
        Include appropriate headings and bullet points for readability.
        """
        
        # Get report from OpenAI
        return self.analyze_with_ai(prompt, temperature=0.5)

def load_processed_data(company_name, is_primary=True):
    """
    Load processed data for a company
    
    Parameters:
    - company_name: Name of the company
    - is_primary: Whether this is a primary competitor
    
    Returns:
    - Dictionary with company data
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

def save_analysis_results(company_name, analysis_data, analysis_type="company_profile"):
    """
    Save analysis results to a file
    
    Parameters:
    - company_name: Name of the company
    - analysis_data: Dictionary with analysis results
    - analysis_type: Type of analysis performed
    
    Returns:
    - Path to the saved file
    """
    # Create output directory
    output_dir = ANALYSIS_DIR / "reports" / company_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create output filename
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"{analysis_type}_{timestamp}.json"
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2)
    
    return output_file

def analyze_competitors(company_names, is_primary=True):
    """
    Analyze multiple competitors
    
    Parameters:
    - company_names: List of company names
    - is_primary: Whether these are primary competitors
    
    Returns:
    - Dictionary with comparative analysis
    """
    analyst = CompetitiveAnalyst()
    
    # Load data for each company
    companies_data = []
    for name in company_names:
        data = load_processed_data(name, is_primary)
        if data:
            companies_data.append(data)
    
    if not companies_data:
        return None
    
    # Perform comparative analysis
    comparative_analysis = analyst.compare_competitors(companies_data)
    
    # Generate strategic recommendations
    recommendations = analyst.generate_strategic_recommendations(comparative_analysis)
    
    # Combine results
    result = {
        "comparative_analysis": comparative_analysis,
        "strategic_recommendations": recommendations
    }
    
    # Save results
    save_analysis_results("multiple", result, "competitive_comparison")
    
    return result

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python competitive_analyst.py <company_name1,company_name2,...>")
        sys.exit(1)
    
    company_names = sys.argv[1].split(',')
    
    result = analyze_competitors(company_names)
    if result:
        print(f"Analysis completed and saved.")
    else:
        print(f"No data found for companies: {company_names}") 