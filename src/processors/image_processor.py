from typing import Any, Dict, List
from PIL import Image
from .base import BaseProcessor

class ImageProcessor(BaseProcessor):
    """Processor for image operations."""
    
    def validate_input(self, input_data: str) -> bool:
        return input_data.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg'))
    
    def process(self, input_path: str) -> Dict[str, Any]:
        if not self.validate_input(input_path):
            raise ValueError(f"Invalid input file: {input_path}")
        
        images = []
        if input_path.lower().endswith('.pdf'):
            images = convert_from_path(input_path)
        else:
            images = [Image.open(input_path)]
        
        processed_images = []
        for idx, image in enumerate(images):
            # Apply any image processing here
            processed_images.append(f"page_{idx+1}.png")
            image.save(processed_images[-1])
        
        return {
            "processed_images": processed_images,
            "page_count": len(images),
            "processor": "Image"
        }
