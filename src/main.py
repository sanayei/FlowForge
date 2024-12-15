from orchestration.pipeline import ProcessingPipeline
from processors.ocr_processor import OCRProcessor
from processors.image_processor import ImageProcessor

def main():
    from config.settings import AWSConfig, ProcessorConfig
    
    # Initialize configurations
    aws_config = AWSConfig(
        region="us-west-2",
        bucket="my-bucket",
        role_arn="my-role"
    )
    
    processor_config = ProcessorConfig()
    
    # Create pipeline
    pipeline = ProcessingPipeline(aws_config, processor_config)
    
    # Register processors
    pipeline.register_processor("ocr", OCRProcessor)
    pipeline.register_processor("image", ImageProcessor)
    
    # Run specific processor
    pipeline.run_processor(
        "ocr",
        input_prefix="s3://my-bucket/documents/",
        output_type="text"
    )

if __name__ == "__main__":
    main()