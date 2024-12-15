import argparse
from typing import List
import pandas as pd
from core.processor import DocumentProcessor
from core.storage import StorageManager
from config.settings import OCRConfig

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--documents",
        type=str,
        required=True,
        help="Comma-separated list of document paths"
    )
    parser.add_argument(
        "--output-type",
        choices=["text", "image", "both"],
        default="both"
    )
    parser.add_argument(
        "--partition-key",
        type=str,
        default="document_id"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    documents = args.documents.split(",")
    
    processor = DocumentProcessor(output_type=args.output_type)
    results = []
    
    for doc in documents:
        try:
            result = processor.process_document(
                doc,
                document_id=doc.split("/")[-1].split(".")[0]
            )
            results.append(result)
        except Exception as e:
            print(f"Error processing {doc}: {str(e)}")
    
    if results:
        df = pd.DataFrame(results)
        
        storage = StorageManager(
            bucket="my-ocr-bucket",
            prefix="output"
        )
        
        storage.save_results(
            data=df,
            partition_key=args.partition_key,
            output_prefix="processed"
        )

if __name__ == "__main__":
    main()