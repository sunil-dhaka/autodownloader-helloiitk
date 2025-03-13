"""
PDF converter for HTML files.
"""
import os
from typing import Dict, Any, Optional
import pdfkit

from src.utils.config import DEFAULT_PDF_OPTIONS, CSS_FILE


class PdfConverter:
    """
    Class for converting HTML files to PDF format.
    
    This class provides methods to convert HTML files to PDF documents
    using wkhtmltopdf via the pdfkit library.
    """
    
    def __init__(self, options: Optional[Dict[str, Any]] = None, css_file: Optional[str] = None):
        """
        Initialize the PDF converter with options.
        
        Parameters
        ----------
        options : Optional[Dict[str, Any]], optional
            PDF conversion options for pdfkit, by default None
        css_file : Optional[str], optional
            Path to CSS file for styling, by default None
        """
        self.options = options or DEFAULT_PDF_OPTIONS
        self.css_file = css_file or CSS_FILE
        
    def convert_html_file(self, html_path: str, pdf_path: Optional[str] = None) -> str:
        """
        Convert an HTML file to PDF.
        
        Parameters
        ----------
        html_path : str
            Path to the HTML file
        pdf_path : Optional[str], optional
            Path for the output PDF file, by default None (derived from HTML path)
            
        Returns
        -------
        str
            Path to the generated PDF file
            
        Raises
        ------
        FileNotFoundError
            If the HTML file doesn't exist
        RuntimeError
            If the conversion fails
        """
        if not os.path.exists(html_path):
            raise FileNotFoundError(f"HTML file not found: {html_path}")
        
        # If no PDF path is provided, derive it from the HTML path
        if pdf_path is None:
            pdf_path = os.path.splitext(html_path)[0] + ".pdf"
            
        try:
            # Check if CSS file exists and is accessible
            css = self.css_file if os.path.exists(self.css_file) else None
            
            # Convert HTML to PDF
            pdfkit.from_file(
                html_path,
                pdf_path,
                options=self.options,
                css=css
            )
            
            return pdf_path
        except Exception as e:
            raise RuntimeError(f"Failed to convert HTML to PDF: {str(e)}")
            
    def convert_html_string(self, html_content: str, output_path: str) -> str:
        """
        Convert HTML content string to PDF.
        
        Parameters
        ----------
        html_content : str
            HTML content to convert
        output_path : str
            Path for the output PDF file
            
        Returns
        -------
        str
            Path to the generated PDF file
            
        Raises
        ------
        RuntimeError
            If the conversion fails
        """
        try:
            # Check if CSS file exists and is accessible
            css = self.css_file if os.path.exists(self.css_file) else None
            
            # Convert HTML string to PDF
            pdfkit.from_string(
                html_content,
                output_path,
                options=self.options,
                css=css
            )
            
            return output_path
        except Exception as e:
            raise RuntimeError(f"Failed to convert HTML string to PDF: {str(e)}")