from typing import List, Optional
import boto3
import s3fs
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
import uuid

class StorageManager:
    def __init__(self, bucket: str, prefix: str):
        self.bucket = bucket
        self.prefix = prefix
        self.s3_client = boto3.client('s3')
        self.s3fs = s3fs.S3FileSystem()
    
    def list_documents(self, extension: str = ".pdf") -> List[str]:
        """List all documents with given extension in the bucket/prefix."""
        response = self.s3_client.list_objects_v2(
            Bucket=self.bucket,
            Prefix=self.prefix
        )
        return [
            obj['Key'] for obj in response.get('Contents', [])
            if obj['Key'].endswith(extension)
        ]
    
    def save_results(
        self,
        data: pd.DataFrame,
        partition_key: str,
        output_prefix: str
    ) -> None:
        """Save results to S3 in partitioned parquet format."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_id = uuid.uuid4().hex[:8]
        
        for partition_value, partition_df in data.groupby(partition_key):
            output_path = (
                f"s3://{self.bucket}/{output_prefix}/"
                f"{partition_key}={partition_value}/"
                f"batch_{timestamp}_{file_id}.parquet"
            )
            
            table = pa.Table.from_pandas(
                partition_df.drop(columns=[partition_key])
            )
            
            with self.s3fs.open(output_path, 'wb') as f:
                pq.write_table(table, f)
