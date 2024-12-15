# Distributed OCR Pipeline

A scalable, distributed OCR (Optical Character Recognition) pipeline built with AWS SageMaker for processing large volumes of documents efficiently. The pipeline leverages SageMaker's processing jobs to distribute workload across multiple instances and uses Tesseract for OCR processing.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Development](#development)
- [Testing](#testing)
- [Infrastructure](#infrastructure)
- [Monitoring and Logging](#monitoring-and-logging)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Distributed Processing**: Automatically distributes document processing across multiple SageMaker instances
- **Flexible Output**: Support for both text extraction and image processing
- **Configurable Pipeline**: Easy-to-customize processing parameters
- **S3 Integration**: Seamless integration with AWS S3 for document storage
- **Monitoring**: Built-in logging and monitoring capabilities
- **Error Handling**: Robust error handling and retry mechanisms
- **Infrastructure as Code**: Complete Terraform configurations for AWS resources

## Architecture

### Component Overview

1. **Core Components** (`src/core/`)
   - `processor.py`: Handles document processing and OCR
   - `storage.py`: Manages S3 interactions and data storage

2. **Orchestration** (`src/orchestration/`)
   - `pipeline.py`: Manages the distributed processing pipeline
   - Handles job distribution and scheduling

3. **Configuration** (`src/config/`)
   - `settings.py`: Contains all configuration classes
   - Supports environment-specific settings

### Flow Diagram

```
Input Documents (S3)
      ↓
Document Discovery
      ↓
Job Distribution
      ↓
SageMaker Processing Jobs
      ↓
OCR Processing
      ↓
Results Storage (S3)
```

## Prerequisites

- Python 3.9+
- AWS Account with appropriate permissions
- Docker
- Terraform (for infrastructure deployment)

Required AWS Permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*",
                "sagemaker:*",
                "ecr:*",
                "iam:PassRole"
            ],
            "Resource": "*"
        }
    ]
}
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/distributed-ocr-pipeline.git
cd distributed-ocr-pipeline
```

2. Install the package:
```bash
make install
```

3. Set up AWS credentials:
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-west-2"
```

## Usage

### Basic Usage

```python
from distributed_ocr_pipeline.config.settings import AWSConfig, OCRConfig
from distributed_ocr_pipeline.orchestration.pipeline import OCRPipeline

# Initialize configurations
aws_config = AWSConfig(
    region="us-west-2",
    bucket="my-document-bucket",
    role_arn="arn:aws:iam::account:role/SageMakerExecutionRole"
)

ocr_config = OCRConfig(
    output_format="parquet",
    partition_key="document_id"
)

# Create and run pipeline
pipeline = OCRPipeline(aws_config, ocr_config)
pipeline.run(input_prefix="documents/")
```

### CLI Usage

```bash
# Run pipeline from command line
python -m distributed_ocr_pipeline.main \
    --input-prefix documents/ \
    --output-type both \
    --max-parallel-jobs 5
```

## Configuration

### AWS Configuration

Configure AWS settings in `config/settings.py`:

```python
@dataclass
class AWSConfig:
    region: str = "us-west-2"
    bucket: str = "my-ocr-bucket"
    role_arn: str = "arn:aws:iam::ACCOUNT:role/SageMakerExecutionRole"
    instance_type: str = "ml.t3.xlarge"
    max_parallel_jobs: int = 10
    files_per_job: int = 10
```

### OCR Configuration

Configure OCR settings:

```python
@dataclass
class OCRConfig:
    output_format: str = "parquet"
    partition_key: str = "document_id"
    tesseract_config: Optional[dict] = None
```

## Development

### Setting Up Development Environment

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

### Code Style

The project uses:
- Black for code formatting
- isort for import sorting
- mypy for type checking
- pylint for linting

Run all style checks:
```bash
make format  # Format code
make lint    # Run linters
```

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run specific test
pytest tests/unit/test_processor.py -v

# Run with coverage
pytest --cov=src tests/
```

### Writing Tests

Example test:

```python
def test_document_processor():
    processor = DocumentProcessor(output_type="both")
    result = processor.process_document(
        "test.pdf",
        document_id="test123"
    )
    assert "text" in result
    assert "image_paths" in result
```

## Infrastructure

### Building Docker Image

```bash
make build-image
```

### Deploying Infrastructure

1. Initialize Terraform:
```bash
cd infrastructure/terraform
terraform init
```

2. Deploy:
```bash
make deploy
```

## Monitoring and Logging

### Logging Configuration

The pipeline uses Python's logging module with customizable handlers:

```python
from distributed_ocr_pipeline.utils.logging import setup_logging

setup_logging(
    level=logging.INFO,
    log_file="pipeline.log"
)
```

### Monitoring Metrics

Key metrics available:
- Documents processed
- Processing time per document
- Error rates
- SageMaker instance utilization

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Troubleshooting

Common issues and solutions:

1. **SageMaker Role Permissions**
   - Ensure the SageMaker execution role has necessary permissions
   - Check CloudWatch logs for permission errors

2. **Document Processing Errors**
   - Verify PDF file format compatibility
   - Check Tesseract installation in Docker image
   - Review instance memory allocation

3. **Infrastructure Deployment**
   - Verify AWS credentials
   - Check Terraform state
   - Review ECR repository permissions

[Previous README content remains the same until the Usage section, where we add:]

## Local Development with SageMaker Local Mode

### Prerequisites for Local Mode

1. Install Docker
2. Install the SageMaker Local Mode requirements:
```bash
pip install sagemaker-local
```

3. Configure local AWS credentials:
```bash
# ~/.aws/credentials
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# ~/.aws/config
[default]
region = us-west-2
```

### Setting Up Local Development Environment

1. Create a local development configuration:

```python
# src/config/local_settings.py
from dataclasses import dataclass
from .settings import AWSConfig, OCRConfig

@dataclass
class LocalAWSConfig(AWSConfig):
    endpoint_url: str = "http://localhost:8080"
    use_local_mode: bool = True
    
    # Override defaults for local testing
    instance_type: str = "local"
    instance_count: int = 1
    max_parallel_jobs: int = 2
    
    # Local storage paths
    local_input_path: str = "./data/input"
    local_output_path: str = "./data/output"

@dataclass
class LocalTestConfig:
    sample_documents_path: str = "./tests/data/sample_docs"
    test_output_path: str = "./tests/data/output"
    mock_s3: bool = True
```

2. Create a local test script:

```python
# src/local_test.py
import os
import shutil
from pathlib import Path
from config.local_settings import LocalAWSConfig, LocalTestConfig, OCRConfig
from orchestration.pipeline import OCRPipeline
from utils.logging import setup_logging
import logging

def setup_local_directories(config: LocalTestConfig):
    """Create necessary directories for local testing."""
    directories = [
        config.sample_documents_path,
        config.test_output_path
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def cleanup_local_directories(config: LocalTestConfig):
    """Clean up test directories."""
    shutil.rmtree(config.test_output_path, ignore_errors=True)

def main():
    # Setup logging
    setup_logging(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    # Initialize configurations
    local_aws_config = LocalAWSConfig()
    ocr_config = OCRConfig()
    test_config = LocalTestConfig()
    
    try:
        # Setup test environment
        setup_local_directories(test_config)
        
        # Initialize pipeline with local config
        pipeline = OCRPipeline(
            aws_config=local_aws_config,
            ocr_config=ocr_config
        )
        
        # Run pipeline on test documents
        pipeline.run(input_prefix=test_config.sample_documents_path)
        
        logger.info(
            "Pipeline completed. Check results in: %s",
            test_config.test_output_path
        )
        
    except Exception as e:
        logger.error("Local test failed: %s", str(e))
        raise
    finally:
        if not os.getenv("KEEP_TEST_FILES"):
            cleanup_local_directories(test_config)

if __name__ == "__main__":
    main()
```

3. Create a local test environment:

```bash
# scripts/setup_local_env.sh
#!/usr/bin/env bash
set -euo pipefail

# Create test directories
mkdir -p ./tests/data/sample_docs
mkdir -p ./tests/data/output

# Download sample PDFs for testing
wget -P ./tests/data/sample_docs \
    https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf

# Build local Docker image
docker build -t sagemaker-ocr-processor:local \
    -f infrastructure/docker/Dockerfile.local .
```

### Running Tests in Local Mode

1. Start the local SageMaker runtime:
```bash
# Start local SageMaker runtime container
docker run -d --name sagemaker-local \
    -p 8080:8080 \
    -v ~/.aws:/root/.aws \
    -v $(pwd)/data:/opt/ml \
    sagemaker-ocr-processor:local
```

2. Run local tests:
```bash
# Run local test script
python src/local_test.py
```

3. Check the results:
```bash
# View processed files
ls -l tests/data/output
```

### Docker Configuration for Local Mode

Create a local Dockerfile:

```dockerfile
# infrastructure/docker/Dockerfile.local
FROM public.ecr.aws/ubuntu/ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install SageMaker Local requirements
RUN pip3 install sagemaker-training

# Install project requirements
COPY requirements.txt /opt/ml/code/
RUN pip3 install -r /opt/ml/code/requirements.txt

# Copy project code
COPY src /opt/ml/code/src

WORKDIR /opt/ml/code
ENV PYTHONPATH=/opt/ml/code

# Entry point for local mode
ENTRYPOINT ["python3", "-m", "src.process_batch"]
```

### Makefile Targets for Local Development

Add these targets to your Makefile:

```makefile
.PHONY: local-setup local-test local-clean

local-setup:
	./scripts/setup_local_env.sh

local-test:
	python src/local_test.py

local-clean:
	docker rm -f sagemaker-local || true
	rm -rf tests/data/output/*
```

### Debugging in Local Mode

1. Enable detailed logging:
```python
# In your local test script
import logging
logging.getLogger('sagemaker').setLevel(logging.DEBUG)
```

2. Access container logs:
```bash
# View container logs
docker logs sagemaker-local

# Access container shell
docker exec -it sagemaker-local /bin/bash
```

3. Monitor local processing:
```bash
# Watch output directory
watch -n 1 "ls -l tests/data/output"
```

### Sample Test Documents

For testing, you can use these document types:
- Single-page PDFs
- Multi-page PDFs
- Scanned documents
- Documents with mixed content (text and images)

Place test documents in `tests/data/sample_docs/`.

Example test document structure:
```
tests/data/sample_docs/
├── single_page.pdf
├── multi_page.pdf
├── scanned_doc.pdf
└── mixed_content.pdf
```

### Local Testing Best Practices

1. Start small:
   - Begin with 1-2 simple documents
   - Verify basic processing works
   - Gradually add more complex documents

2. Test error handling:
   - Try malformed PDFs
   - Test network interruptions
   - Verify error logging

3. Performance testing:
   - Monitor memory usage
   - Check processing times
   - Test with different batch sizes

4. Clean up:
   - Remove test containers
   - Clear test data
   - Reset local environment

[Rest of the README remains the same]

