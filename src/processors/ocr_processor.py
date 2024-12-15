from typing import Any, Dict, List
import pytesseract
from pdf2image import convert_from_path
from .base import BaseProcessor

class OCRProcessor(BaseProcessor):
    """Processor for OCR operations."""
    
    def validate_input(self, input_data: str) -> bool:
        return input_data.lower().endswith('.pdf')
    
    def process(self, input_path: str) -> Dict[str, Any]:
        if not self.validate_input(input_path):
            raise ValueError(f"Invalid input file: {input_path}")
        
        images = convert_from_path(input_path)
        texts = []
        
        for image in images:
            text = pytesseract.image_to_string(image)
            texts.append(text)
        
        return {
            "text": texts,
            "page_count": len(images),
            "processor": "OCR"
        }
