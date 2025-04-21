"""
PDF Extraction Tool for Constructiv AI Competitive Analysis

This module provides functions to extract structured content from PDF files,
particularly focused on CB Insights reports and other competitive intelligence sources.
"""
import json
import os
from pathlib import Path
import fitz  # PyMuPDF
import re

# Import configuration
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config import RAW_DIR, PROCESSED_DIR

class PDFExtractor:
    """Class for extracting structured content from PDF files"""
    
    def __init__(self, pdf_path):
        """
        Initialize the PDF extractor with a PDF file path
        
        Parameters:
        - pdf_path: Path to the PDF file
        """
        self.pdf_path = Path(pdf_path)
        self.document = None
        self.content = {
            "metadata": {},
            "toc": [],
            "sections": [],
            "tables": [],
            "figures": [],
            "extracted_text": ""
        }
        
    def load_document(self):
        """Load the PDF document"""
        try:
            self.document = fitz.open(self.pdf_path)
            self.content["metadata"] = {
                "title": self.document.metadata.get("title", ""),
                "author": self.document.metadata.get("author", ""),
                "subject": self.document.metadata.get("subject", ""),
                "keywords": self.document.metadata.get("keywords", ""),
                "creator": self.document.metadata.get("creator", ""),
                "producer": self.document.metadata.get("producer", ""),
                "pages": len(self.document),
                "filename": self.pdf_path.name
            }
            return True
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return False
            
    def extract_toc(self):
        """Extract table of contents if available"""
        if not self.document:
            return False
        
        try:
            toc = self.document.get_toc()
            if toc:
                self.content["toc"] = [
                    {"level": level, "title": title, "page": page} 
                    for level, title, page in toc
                ]
            return True
        except Exception as e:
            print(f"Error extracting TOC: {e}")
            return False
    
    def extract_text_with_formatting(self):
        """Extract text with basic formatting information"""
        if not self.document:
            return False
        
        all_text = ""
        sections = []
        current_section = {"title": "", "content": "", "subsections": []}
        
        for page_num, page in enumerate(self.document):
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if block["type"] == 0:  # Text block
                    for line in block["lines"]:
                        line_text = ""
                        
                        # Extract text from spans
                        for span in line["spans"]:
                            text = span["text"]
                            font_size = span["size"]
                            font_name = span["font"]
                            is_bold = "bold" in font_name.lower() or "heavy" in font_name.lower()
                            
                            # Detect headings based on font size and formatting
                            if font_size > 14 or (font_size > 12 and is_bold):
                                # Likely a heading - start new section
                                if current_section["title"] and current_section["content"]:
                                    sections.append(current_section)
                                    current_section = {"title": text, "content": "", "subsections": []}
                                else:
                                    current_section["title"] = text
                            else:
                                # Regular content
                                line_text += text
                                current_section["content"] += text + " "
                        
                        all_text += line_text + "\n"
            
            # Add page break marker
            all_text += "\f"
        
        # Add the last section if not empty
        if current_section["title"] or current_section["content"]:
            sections.append(current_section)
        
        self.content["sections"] = sections
        self.content["extracted_text"] = all_text
        return True
    
    def extract_tables(self):
        """Extract tables from the PDF"""
        if not self.document:
            return False
        
        tables = []
        
        for page_num, page in enumerate(self.document):
            # Simple table detection based on horizontal and vertical lines
            # This is a basic approach - for production use, consider libraries like camelot or tabula
            
            # Get drawings (lines) on the page
            drawings = page.get_drawings()
            horizontal_lines = []
            vertical_lines = []
            
            for drawing in drawings:
                for item in drawing["items"]:
                    if item[0] == "l":  # Line
                        x0, y0, x1, y1 = item[1:5]
                        if abs(y1 - y0) < 2:  # Horizontal line
                            horizontal_lines.append((min(x0, x1), y0, max(x0, x1), y1))
                        elif abs(x1 - x0) < 2:  # Vertical line
                            vertical_lines.append((x0, min(y0, y1), x1, max(y0, y1)))
            
            # Identify table regions based on intersecting lines
            # This is a simplistic approach - would need refinement for production
            if horizontal_lines and vertical_lines:
                # Basic algorithm to detect tables based on grid patterns
                # For each intersection of horizontal and vertical lines, check if it forms a cell
                
                # Get text in the table region
                text = page.get_text("text", clip=(x0, y0, x1, y1))
                
                tables.append({
                    "page": page_num + 1,
                    "content": text,
                    "bbox": [x0, y0, x1, y1]
                })
        
        self.content["tables"] = tables
        return True
    
    def extract_figures(self):
        """Extract figures and images from the PDF"""
        if not self.document:
            return False
        
        figures = []
        
        for page_num, page in enumerate(self.document):
            # Extract images
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                
                try:
                    base_image = self.document.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Get position information if available
                    for img_info in page.get_image_info():
                        if img_info["xref"] == xref:
                            figures.append({
                                "page": page_num + 1,
                                "index": img_index,
                                "bbox": img_info.get("bbox", [0, 0, 0, 0]),
                                "size_bytes": len(image_bytes)
                            })
                            break
                except Exception as e:
                    print(f"Error extracting image: {e}")
        
        self.content["figures"] = figures
        return True
    
    def extract_all(self):
        """Extract all content from the PDF"""
        if not self.load_document():
            return False
        
        self.extract_toc()
        self.extract_text_with_formatting()
        self.extract_tables()
        self.extract_figures()
        
        return self.content
    
    def save_extracted_content(self, output_path=None):
        """
        Save the extracted content to a JSON file
        
        Parameters:
        - output_path: Path to save the JSON file (optional)
        """
        if not output_path:
            # Create output path in processed directory
            company_name = self.content["metadata"].get("title", "").strip()
            if not company_name:
                company_name = self.pdf_path.stem
            
            # Sanitize filename
            company_name = re.sub(r'[^\w\-\. ]', '_', company_name)
            output_dir = PROCESSED_DIR / "competitors" / "primary" / company_name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / f"{self.pdf_path.stem}_extracted.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.content, f, indent=2, ensure_ascii=False)
        
        return output_path

def extract_from_pdf(pdf_path, output_path=None):
    """
    Extract structured text from PDF maintaining hierarchical information.
    
    Parameters:
    - pdf_path: Path to the PDF file
    - output_path: Optional path to save the extracted content
    
    Returns:
    - Dictionary with structured content
    """
    extractor = PDFExtractor(pdf_path)
    content = extractor.extract_all()
    
    if content and output_path:
        extractor.save_extracted_content(output_path)
    
    return content

def extract_text_only(pdf_path):
    """
    Extract only text from a PDF without additional structural information.
    Useful for quick processing by LLMs.
    
    Parameters:
    - pdf_path: Path to the PDF file
    
    Returns:
    - String containing all text from the PDF
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        
        for page in doc:
            text += page.get_text()
            text += "\n\n"
        
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pdf_extractor.py <pdf_file_path> [output_path]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    content = extract_from_pdf(pdf_path, output_path)
    if content:
        print(f"Successfully extracted content from {pdf_path}")
        if output_path:
            print(f"Saved to {output_path}")
    else:
        print(f"Failed to extract content from {pdf_path}") 