from dataclasses import dataclass
from typing import Optional

@dataclass
class AWSConfig:
    region: str = "us-west-2"
    bucket: str = "my-ocr-bucket"
    role_arn: str = "arn:aws:iam::ACCOUNT:role/SageMakerExecutionRole"
    instance_type: str = "ml.t3.xlarge"
    max_parallel_jobs: int = 10
    files_per_job: int = 10

@dataclass
class OCRConfig:
    output_format: str = "parquet"
    partition_key: str = "document_id"
    tesseract_config: Optional[dict] = None