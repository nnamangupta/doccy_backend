import os
import tempfile
from typing import List, Optional, Union, BinaryIO, Dict, Any
from pathlib import Path
import logging

# PDF processing
import pdfplumber

# Document processing
from docx import Document

# Image processing and OCR
import pytesseract
from PIL import Image

# Excel processing
import pandas as pd

# Text extraction helpers
import csv
import json

logger = logging.getLogger(__name__)

class DocumentPreprocessor:
    """
    Handles preprocessing of various document types to extract plain text.
    Supported formats: PDF, DOCX, DOC, JPG, PNG, TIFF, XLSX, CSV, TXT, JSON
    """
    
    def __init__(self, ocr_lang: str = 'eng'):
        """
        Initialize the document preprocessor.
        
        Args:
            ocr_lang: Language for OCR processing (default: 'eng')
        """
        self.ocr_lang = ocr_lang
        
    def process_file(self, file_path: Union[str, Path, BinaryIO], 
                     file_type: Optional[str] = None) -> str:
        """
        Process a file and extract plain text.
        
        Args:
            file_path: Path to file or file-like object
            file_type: Optional file type override (e.g., 'pdf', 'docx')
            
        Returns:
            Extracted plain text from the document
        """
        if isinstance(file_path, (str, Path)):
            file_path = Path(file_path)
            if not file_type:
                file_type = file_path.suffix.lower().lstrip('.')
        elif not file_type:
            raise ValueError("When providing a file object, file_type must be specified")
            
        # Route to appropriate handler based on file type
        if file_type in ('pdf'):
            return self._extract_from_pdf(file_path)
        elif file_type in ('docx', 'doc'):
            return self._extract_from_doc(file_path)
        elif file_type in ('jpg', 'jpeg', 'png', 'tiff', 'bmp'):
            return self._extract_from_image(file_path)
        elif file_type in ('xlsx', 'xls', 'csv'):
            return self._extract_from_spreadsheet(file_path, file_type)
        elif file_type == 'txt':
            return self._extract_from_text(file_path)
        elif file_type == 'json':
            return self._extract_from_json(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def process_files(self, file_paths: List[Union[str, Path]], 
                     file_types: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Process multiple files and extract plain text from each.
        
        Args:
            file_paths: List of paths to files
            file_types: Optional list of file types
            
        Returns:
            Dictionary mapping file paths to extracted text
        """
        results = {}
        
        for i, file_path in enumerate(file_paths):
            file_type = file_types[i] if file_types and i < len(file_types) else None
            try:
                results[str(file_path)] = self.process_file(file_path, file_type)
            except Exception as e:
                logger.error(f"Error processing {file_path}: {str(e)}")
                results[str(file_path)] = ""
                
        return results
    
    def _extract_from_pdf(self, file_path: Union[str, Path, BinaryIO]) -> str:
        """Extract text from PDF files"""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
                text += "\n\n"
        return text.strip()
    
    def _extract_from_doc(self, file_path: Union[str, Path, BinaryIO]) -> str:
        """Extract text from Word documents"""
        doc = Document(file_path)
        return "\n\n".join([para.text for para in doc.paragraphs])
    
    def _extract_from_image(self, file_path: Union[str, Path, BinaryIO]) -> str:
        """Extract text from images using OCR"""
        image = Image.open(file_path)
        return pytesseract.image_to_string(image, lang=self.ocr_lang)
    
    def _extract_from_spreadsheet(self, file_path: Union[str, Path, BinaryIO], 
                                 file_type: str) -> str:
        """Extract text from Excel and CSV files"""
        if file_type in ('xlsx', 'xls'):
            df = pd.read_excel(file_path)
        else:  # csv
            df = pd.read_csv(file_path)
            
        # Convert dataframe to text representation
        return df.to_string(index=False)
    
    def _extract_from_text(self, file_path: Union[str, Path, BinaryIO]) -> str:
        """Extract text from plain text files"""
        if isinstance(file_path, (str, Path)):
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()
        else:
            return file_path.read().decode('utf-8', errors='replace')
    
    def _extract_from_json(self, file_path: Union[str, Path, BinaryIO]) -> str:
        """Extract text from JSON files"""
        if isinstance(file_path, (str, Path)):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = json.loads(file_path.read().decode('utf-8'))
            
        # Convert JSON to string representation
        return json.dumps(data, indent=2)


# Usage example
if __name__ == "__main__":
    processor = DocumentPreprocessor()
    
    # Example usage
    pdf_text = processor.process_file("example.pdf")
    print(f"Extracted {len(pdf_text)} characters from PDF")
    
    # Process multiple files
    results = processor.process_files(["doc1.pdf", "image.png", "data.xlsx"])
    for file_path, text in results.items():
        print(f"File: {file_path}, Extracted length: {len(text)}")