from typing import List, Dict, Any
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os

class DocumentProcessor:
    def __init__(self, output_type: str = "both"):
        self.output_type = output_type
        self._validate_output_type()
    
    def _validate_output_type(self):
        valid_types = {"text", "image", "both"}
        if self.output_type not in valid_types:
            raise ValueError(
                f"Output type must be one of {valid_types}"
            )
    
    def process_document(
        self,
        file_path: str,
        document_id: str
    ) -> Dict[str, Any]:
        """Process a single document for OCR."""
        images = convert_from_path(file_path)
        result = {
            "document_id": document_id,
            "filename": os.path.basename(file_path),
            "page_count": len(images),
            "processed_at": pd.Timestamp.now(),
            "ocr_tool": f"tesseract-{pytesseract.__version__}"
        }
        
        if self.output_type in ("text", "both"):
            result["text"] = self._extract_text(images)
            
        if self.output_type in ("image", "both"):
            result["image_paths"] = self._save_images(
                images, document_id
            )
            
        return result
    
    def _extract_text(self, images: List[Image.Image]) -> List[str]:
        """Extract text from images using Tesseract."""
        with ThreadPoolExecutor() as executor:
            texts = list(executor.map(
                pytesseract.image_to_string, images
            ))
        return texts
    
    def _save_images(
        self,
        images: List[Image.Image],
        document_id: str
    ) -> List[str]:
        """Save images as PNG files."""
        paths = []
        for idx, image in enumerate(images):
            path = f"output/{document_id}_page_{idx+1}.png"
            image.save(path, "PNG")
            paths.append(path)
        return paths
