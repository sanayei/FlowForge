from typing import List
import sagemaker
from sagemaker.processing import ScriptProcessor
import math
from ..config.settings import AWSConfig, OCRConfig
from ..core.storage import StorageManager

class OCRPipeline:
    def __init__(
        self,
        aws_config: AWSConfig,
        ocr_config: OCRConfig
    ):
        self.aws_config = aws_config
        self.ocr_config = ocr_config
        self.storage = StorageManager(
            aws_config.bucket,
            "input"
        )
        self.sagemaker_session = sagemaker.Session()
    
    def run(self, input_prefix: str) -> None:
        """Run the distributed OCR pipeline."""
        # List documents to process
        documents = self.storage.list_documents()
        
        if not documents:
            print("No documents found to process")
            return
        
        # Calculate job distribution
        num_jobs = min(
            math.ceil(len(documents) / self.aws_config.files_per_job),
            self.aws_config.max_parallel_jobs
        )
        
        # Create processor
        processor = ScriptProcessor(
            role=self.aws_config.role_arn,
            image_uri=self._get_image_uri(),
            command=["python3"],
            instance_type=self.aws_config.instance_type,
            instance_count=1,
            sagemaker_session=self.sagemaker_session
        )
        
        # Launch distributed processing jobs
        self._launch_jobs(processor, documents, num_jobs)
    
    def _get_image_uri(self) -> str:
        """Get the ECR image URI for the processor."""
        account = self.sagemaker_session.boto_session.client(
            'sts'
        ).get_caller_identity()['Account']
        
        return f"{account}.dkr.ecr.{self.aws_config.region}.amazonaws.com/ocr-processor:latest"
    
    def _launch_jobs(
        self,
        processor: ScriptProcessor,
        documents: List[str],
        num_jobs: int
    ) -> None:
        """Launch distributed processing jobs."""
        docs_per_job = math.ceil(len(documents) / num_jobs)
        
        for job_id in range(num_jobs):
            start_idx = job_id * docs_per_job
            end_idx = min(start_idx + docs_per_job, len(documents))
            
            job_docs = documents[start_idx:end_idx]
            
            processor.run(
                code="process_batch.py",
                arguments=[
                    "--documents", ",".join(job_docs),
                    "--output-type", self.ocr_config.output_format,
                    "--partition-key", self.ocr_config.partition_key
                ],
                wait=False
            )
