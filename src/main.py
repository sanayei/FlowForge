import logging
from config.settings import AWSConfig, OCRConfig
from orchestration.pipeline import OCRPipeline
from utils.logging import setup_logging

def main():
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize configurations
        aws_config = AWSConfig()
        ocr_config = OCRConfig()
        
        # Create and run pipeline
        pipeline = OCRPipeline(aws_config, ocr_config)
        pipeline.run(input_prefix="documents/")
        
    except Exception as e:
        logger.error("Pipeline execution failed: %s", str(e))
        raise

if __name__ == "__main__":
    main()