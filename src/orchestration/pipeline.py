from typing import Dict, List, Type
from ..config.settings import AWSConfig, ProcessorConfig
from ..processors.base import BaseProcessor
import sagemaker
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput

class ProcessingPipeline:
    """Pipeline for managing different processors."""
    
    def __init__(
        self,
        aws_config: AWSConfig,
        processor_config: ProcessorConfig
    ):
        self.aws_config = aws_config
        self.processor_config = processor_config
        self.sagemaker_session = sagemaker.Session()
        self.processors: Dict[str, Type[BaseProcessor]] = {}
    
    def register_processor(
        self,
        name: str,
        processor_class: Type[BaseProcessor]
    ) -> None:
        """Register a new processor."""
        self.processors[name] = processor_class
    
    def run_processor(
        self,
        processor_name: str,
        input_prefix: str,
        **kwargs
    ) -> None:
        """Run a specific processor."""
        if processor_name not in self.processors:
            raise ValueError(f"Unknown processor: {processor_name}")
        
        processor_class = self.processors[processor_name]
        
        script_processor = ScriptProcessor(
            role=self.aws_config.role_arn,
            image_uri=self._get_processor_image(processor_name),
            command=["python3"],
            instance_type=self.aws_config.instance_type,
            instance_count=1,
            sagemaker_session=self.sagemaker_session
        )
        
        script_processor.run(
            code=f"processors/{processor_name}.py",
            inputs=[
                ProcessingInput(
                    source=input_prefix,
                    destination="/opt/ml/processing/input"
                )
            ],
            outputs=[
                ProcessingOutput(
                    source="/opt/ml/processing/output",
                    destination=f"{input_prefix}/processed-{processor_name}"
                )
            ],
            arguments=[
                "--processor", processor_name,
                *self._build_arguments(kwargs)
            ],
            wait=False
        )
    
    def _get_processor_image(self, processor_name: str) -> str:
        """Get the Docker image URI for the processor."""
        account = self.sagemaker_session.account_id()
        return f"{account}.dkr.ecr.{self.aws_config.region}" \
               f".amazonaws.com/processor-{processor_name}:latest"
    
    def _build_arguments(self, kwargs: Dict) -> List[str]:
        """Build command line arguments from kwargs."""
        args = []
        for key, value in kwargs.items():
            args.extend([f"--{key}", str(value)])
        return args