"""
Visualization Tool for Constructiv AI Competitive Analysis

This module provides functions to generate visualizations based on competitor data.
"""
import os
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd
from datetime import datetime

# Import configuration
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config import PROCESSED_DIR, ANALYSIS_DIR, VISUALIZATIONS_OUTPUT_DIR, VISUALIZATION_CONFIG

class VisualizationGenerator:
    """Class for generating visualizations based on competitor data"""
    
    def __init__(self):
        """Initialize the visualization generator"""
        # Set default style
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # Use consistent branding colors
        self.color_palette = sns.color_palette(VISUALIZATION_CONFIG.get('color_palette', 'viridis'), 10)
        sns.set_palette(self.color_palette)
        
        # Default figure size
        self.default_figsize = VISUALIZATION_CONFIG.get('default_figsize', (12, 8))
        
        # Default DPI for saved images
        self.default_dpi = VISUALIZATION_CONFIG.get('default_dpi', 300)
    
    def create_funding_timeline(self, companies_data, output_path=None):
        """
        Create a funding timeline visualization comparing multiple companies
        
        Parameters:
        - companies_data: List of dictionaries with company information
        - output_path: Path to save the visualization (optional)
        
        Returns:
        - Path to the generated visualization
        """
        plt.figure(figsize=self.default_figsize)
        
        # Extract funding data
        data = []
        
        for company in companies_data:
            company_name = company.get('name', 'Unknown')
            funding_rounds = company.get('funding', [])
            
            for round_data in funding_rounds:
                # Parse date
                try:
                    date_str = round_data.get('date', '')
                    date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else None
                except ValueError:
                    # Try other date formats
                    try:
                        date = datetime.strptime(date_str, '%b %Y')
                    except ValueError:
                        try:
                            date = datetime.strptime(date_str, '%Y')
                        except ValueError:
                            date = None
                
                if date:
                    # Parse amount
                    amount_str = round_data.get('amount', '0')
                    amount = self._parse_funding_amount(amount_str)
                    
                    data.append({
                        'company': company_name,
                        'date': date,
                        'amount': amount,
                        'round': round_data.get('round', 'Unknown')
                    })
        
        if not data:
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        df = df.sort_values('date')
        
        # Plot the data
        plt.figure(figsize=self.default_figsize)
        ax = plt.gca()
        
        # Plot each company's funding timeline
        for i, (company, group) in enumerate(df.groupby('company')):
            plt.plot(group['date'], group['amount'], 'o-', label=company, color=self.color_palette[i % len(self.color_palette)])
            
            # Add labels for each funding round
            for _, row in group.iterrows():
                plt.text(row['date'], row['amount'], f"${row['amount']/1e6:.1f}M\n{row['round']}", 
                        ha='center', va='bottom', fontsize=9)
        
        # Format y-axis as millions
        ax.yaxis.set_major_formatter(lambda x, pos: f'${x/1e6:.0f}M')
        
        plt.title('Funding Timeline Comparison', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Funding Amount', fontsize=12)
        plt.legend(title='Company', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # Save the figure if output_path is provided
        if output_path:
            plt.savefig(output_path, dpi=self.default_dpi, bbox_inches='tight')
        else:
            # Create default output path
            output_dir = VISUALIZATIONS_OUTPUT_DIR
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"funding_timeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(output_path, dpi=self.default_dpi, bbox_inches='tight')
        
        plt.close()
        
        return output_path
    
    def create_market_positioning_map(self, companies_data, x_dimension='product_complexity', y_dimension='market_focus', output_path=None):
        """
        Create a market positioning map
        
        Parameters:
        - companies_data: List of dictionaries with company information
        - x_dimension: Dimension to plot on x-axis
        - y_dimension: Dimension to plot on y-axis
        - output_path: Path to save the visualization (optional)
        
        Returns:
        - Path to the generated visualization
        """
        # Create the dimensions if they don't exist
        dimension_mapping = {
            'product_complexity': {
                'label': 'Product Complexity',
                'description': 'Simple to Complex',
                'get_value': lambda x: x.get('product_complexity', 50)  # Default to middle
            },
            'market_focus': {
                'label': 'Market Focus',
                'description': 'Narrow to Broad',
                'get_value': lambda x: x.get('market_focus_score', 50)
            },
            'price_point': {
                'label': 'Price Point',
                'description': 'Low to High',
                'get_value': lambda x: x.get('price_point', 50)
            },
            'customer_size': {
                'label': 'Customer Size',
                'description': 'Small to Enterprise',
                'get_value': lambda x: x.get('customer_size_score', 50)
            },
            'funding_size': {
                'label': 'Funding Size',
                'description': 'Bootstrap to Well-funded',
                'get_value': lambda x: self._calculate_funding_score(x)
            }
        }
        
        plt.figure(figsize=self.default_figsize)
        
        # Extract positioning data
        x_values = []
        y_values = []
        company_names = []
        bubble_sizes = []
        
        for company in companies_data:
            x_values.append(dimension_mapping[x_dimension]['get_value'](company))
            y_values.append(dimension_mapping[y_dimension]['get_value'](company))
            company_names.append(company.get('name', 'Unknown'))
            
            # Calculate bubble size based on total funding or another metric
            total_funding = sum([self._parse_funding_amount(f.get('amount', '0')) for f in company.get('funding', [])])
            bubble_size = np.sqrt(total_funding) / 1e4 if total_funding > 0 else 30
            bubble_sizes.append(bubble_size)
        
        # Plot the data
        plt.figure(figsize=self.default_figsize)
        scatter = plt.scatter(x_values, y_values, s=bubble_sizes, c=range(len(company_names)), 
                              cmap='viridis', alpha=0.7)
        
        # Add labels for each company
        for i, company in enumerate(company_names):
            plt.annotate(company, (x_values[i], y_values[i]), 
                         xytext=(5, 5), textcoords='offset points', fontsize=9)
        
        plt.title('Competitive Positioning Map', fontsize=16)
        plt.xlabel(f"{dimension_mapping[x_dimension]['label']} ({dimension_mapping[x_dimension]['description']})", fontsize=12)
        plt.ylabel(f"{dimension_mapping[y_dimension]['label']} ({dimension_mapping[y_dimension]['description']})", fontsize=12)
        
        # Set axis limits
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        
        # Add grid
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Divide the chart into quadrants
        plt.axhline(y=50, color='gray', linestyle='-', linewidth=1, alpha=0.5)
        plt.axvline(x=50, color='gray', linestyle='-', linewidth=1, alpha=0.5)
        
        # Add quadrant labels
        plt.text(25, 75, 'Quadrant 1', ha='center', va='center', fontsize=12, alpha=0.7)
        plt.text(75, 75, 'Quadrant 2', ha='center', va='center', fontsize=12, alpha=0.7)
        plt.text(25, 25, 'Quadrant 3', ha='center', va='center', fontsize=12, alpha=0.7)
        plt.text(75, 25, 'Quadrant 4', ha='center', va='center', fontsize=12, alpha=0.7)
        
        plt.tight_layout()
        
        # Save the figure if output_path is provided
        if output_path:
            plt.savefig(output_path, dpi=self.default_dpi, bbox_inches='tight')
        else:
            # Create default output path
            output_dir = VISUALIZATIONS_OUTPUT_DIR
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"market_positioning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(output_path, dpi=self.default_dpi, bbox_inches='tight')
        
        plt.close()
        
        return output_path
    
    def create_funding_comparison_chart(self, companies_data, output_path=None):
        """
        Create a bar chart comparing funding amounts across companies
        
        Parameters:
        - companies_data: List of dictionaries with company information
        - output_path: Path to save the visualization (optional)
        
        Returns:
        - Path to the generated visualization
        """
        plt.figure(figsize=self.default_figsize)
        
        # Extract funding data
        company_names = []
        total_funding = []
        latest_round = []
        
        for company in companies_data:
            company_names.append(company.get('name', 'Unknown'))
            
            # Calculate total funding
            funding_total = sum([self._parse_funding_amount(f.get('amount', '0')) for f in company.get('funding', [])])
            total_funding.append(funding_total)
            
            # Get latest round
            funding_rounds = company.get('funding', [])
            latest = funding_rounds[-1] if funding_rounds else {}
            latest_round.append(latest.get('round', 'Unknown'))
        
        # Sort by total funding
        sorted_indices = np.argsort(total_funding)[::-1]  # Descending order
        company_names = [company_names[i] for i in sorted_indices]
        total_funding = [total_funding[i] for i in sorted_indices]
        latest_round = [latest_round[i] for i in sorted_indices]
        
        # Convert to millions for display
        total_funding_m = [f / 1e6 for f in total_funding]
        
        # Plot the data
        plt.figure(figsize=self.default_figsize)
        bars = plt.bar(company_names, total_funding_m, color=self.color_palette)
        
        # Add data labels
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'${total_funding_m[i]:.1f}M\n{latest_round[i]}',
                    ha='center', va='bottom', fontsize=10)
        
        plt.title('Total Funding Comparison', fontsize=16)
        plt.xlabel('Company', fontsize=12)
        plt.ylabel('Total Funding (USD Millions)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        # Save the figure if output_path is provided
        if output_path:
            plt.savefig(output_path, dpi=self.default_dpi, bbox_inches='tight')
        else:
            # Create default output path
            output_dir = VISUALIZATIONS_OUTPUT_DIR
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"funding_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(output_path, dpi=self.default_dpi, bbox_inches='tight')
        
        plt.close()
        
        return output_path
    
    def create_technology_stack_comparison(self, companies_data, output_path=None):
        """
        Create a visualization comparing technology stacks across companies
        
        Parameters:
        - companies_data: List of dictionaries with company information
        - output_path: Path to save the visualization (optional)
        
        Returns:
        - Path to the generated visualization
        """
        # Extract technology data
        all_tech = set()
        company_tech = {}
        
        for company in companies_data:
            company_name = company.get('name', 'Unknown')
            tech_stack = company.get('technology_stack', [])
            
            company_tech[company_name] = tech_stack
            all_tech.update(tech_stack)
        
        # Sort technologies by frequency
        tech_list = list(all_tech)
        tech_counts = {tech: sum(1 for techs in company_tech.values() if tech in techs) for tech in tech_list}
        tech_list.sort(key=lambda x: tech_counts[x], reverse=True)
        
        # Create a binary matrix of companies x technologies
        matrix = np.zeros((len(companies_data), len(tech_list)))
        
        for i, company in enumerate(companies_data):
            company_name = company.get('name', 'Unknown')
            for j, tech in enumerate(tech_list):
                if tech in company_tech[company_name]:
                    matrix[i, j] = 1
        
        # Plot the data as a heatmap
        plt.figure(figsize=(max(12, len(tech_list) * 0.5), max(8, len(companies_data) * 0.5)))
        
        # Limit to top 20 technologies if there are too many
        if len(tech_list) > 20:
            tech_list = tech_list[:20]
            matrix = matrix[:, :20]
        
        company_names = [company.get('name', 'Unknown') for company in companies_data]
        
        sns.heatmap(matrix, annot=True, cmap="YlGnBu", cbar=False, linewidths=0.5,
                   xticklabels=tech_list, yticklabels=company_names, fmt='')
        
        plt.title('Technology Stack Comparison', fontsize=16)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save the figure if output_path is provided
        if output_path:
            plt.savefig(output_path, dpi=self.default_dpi, bbox_inches='tight')
        else:
            # Create default output path
            output_dir = VISUALIZATIONS_OUTPUT_DIR
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"tech_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(output_path, dpi=self.default_dpi, bbox_inches='tight')
        
        plt.close()
        
        return output_path
    
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
    
    def _calculate_funding_score(self, company_data):
        """Calculate a funding score from 0-100 based on total funding"""
        funding_total = sum([self._parse_funding_amount(f.get('amount', '0')) for f in company_data.get('funding', [])])
        
        # Score calculation (adjust thresholds as needed)
        if funding_total == 0:
            return 10  # Bootstrap
        elif funding_total < 1000000:
            return 20  # Seed (< $1M)
        elif funding_total < 5000000:
            return 40  # Early stage ($1M - $5M)
        elif funding_total < 20000000:
            return 60  # Series A/B ($5M - $20M)
        elif funding_total < 100000000:
            return 80  # Series C/D ($20M - $100M)
        else:
            return 95  # Well-funded (> $100M)

def create_visualization(data, chart_type, output_path=None):
    """
    Generate a visualization based on competitor data.
    
    Parameters:
    - data: The data to visualize
    - chart_type: Type of chart to create
    - output_path: Where to save the image
    
    Returns:
    - Path to generated image
    """
    generator = VisualizationGenerator()
    
    # Convert to list if single company
    if not isinstance(data, list):
        data = [data]
    
    if chart_type == "funding_timeline":
        return generator.create_funding_timeline(data, output_path)
    
    elif chart_type == "market_positioning":
        return generator.create_market_positioning_map(data, output_path=output_path)
    
    elif chart_type == "funding_comparison":
        return generator.create_funding_comparison_chart(data, output_path)
    
    elif chart_type == "tech_comparison":
        return generator.create_technology_stack_comparison(data, output_path)
    
    else:
        raise ValueError(f"Unknown chart type: {chart_type}")

def load_competitor_data(company_names):
    """
    Load competitor data from processed files
    
    Parameters:
    - company_names: List of company names or single company name
    
    Returns:
    - List of dictionaries with competitor data
    """
    if isinstance(company_names, str):
        company_names = [company_names]
    
    companies_data = []
    
    for company_name in company_names:
        # Try as primary competitor first
        company_dir = PROCESSED_DIR / "competitors" / "primary" / company_name
        
        if not company_dir.exists():
            # Try as adjacent competitor
            company_dir = PROCESSED_DIR / "competitors" / "adjacent" / company_name
        
        if not company_dir.exists():
            continue
        
        # Find JSON files
        json_files = list(company_dir.glob("*.json"))
        
        if not json_files:
            continue
        
        # Load and combine data from all JSON files
        combined_data = {}
        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                combined_data.update(data)
        
        companies_data.append(combined_data)
    
    return companies_data

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python visualization.py <chart_type> <company_name1,company_name2,...> [output_path]")
        sys.exit(1)
    
    chart_type = sys.argv[1]
    company_names = sys.argv[2].split(',')
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Load company data
    companies_data = load_competitor_data(company_names)
    
    if not companies_data:
        print(f"No data found for companies: {company_names}")
        sys.exit(1)
    
    # Generate visualization
    viz_path = create_visualization(companies_data, chart_type, output_path)
    
    if viz_path:
        print(f"Visualization saved to: {viz_path}")
    else:
        print("Failed to create visualization") 