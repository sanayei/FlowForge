from typing import Any, List
import os

def validate_file_extension(
    filepath: str,
    allowed_extensions: List[str]
) -> bool:
    """Validate file extension."""
    ext = os.path.splitext(filepath)[1].lower()
    return ext in allowed_extensions

def validate_s3_path(path: str) -> bool:
    """Validate S3 path format."""
    return path.startswith("s3://")

def validate_config(config: Any) -> bool:
    """Validate configuration object."""
    required_attrs = [
        "region", "bucket", "role_arn",
        "instance_type", "max_parallel_jobs"
    ]
    return all(hasattr(config, attr) for attr in required_attrs)
