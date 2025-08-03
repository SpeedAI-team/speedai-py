"""
Advanced usage examples for SpeedAI package
"""

import os
import time
from pathlib import Path
from datetime import datetime
from speedai import (
    SpeedAIClient,
    Language,
    Platform,
    ProcessingMode,
    ProcessingStatus,
    ValidationError,
    ProcessingError,
    NetworkError
)


class DocumentProcessor:
    """Advanced document processor with logging and error recovery."""
    
    def __init__(self, api_key: str, token: str):
        self.client = SpeedAIClient(api_key=api_key, token=token)
        self.processed_count = 0
        self.error_count = 0
    
    def process_with_retry(self, file_path: str, output_path: str, max_retries: int = 3):
        """Process document with automatic retry on failure."""
        for attempt in range(max_retries):
            try:
                print(f"Processing {file_path} (attempt {attempt + 1}/{max_retries})")
                
                result = self.client.process_document(
                    file_path=file_path,
                    output_path=output_path,
                    mode=ProcessingMode.REWRITE,
                    platform=Platform.ZHIWANG,
                    progress_callback=self._progress_callback
                )
                
                self.processed_count += 1
                return result
                
            except NetworkError as e:
                print(f"Network error: {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    self.error_count += 1
                    raise
            except Exception as e:
                self.error_count += 1
                raise
    
    def _progress_callback(self, progress: int, status: str):
        """Custom progress callback with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Progress: {progress}% - Status: {status}")
    
    def process_directory(self, input_dir: str, output_dir: str):
        """Process all documents in a directory."""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        doc_files = list(input_path.glob("*.docx")) + list(input_path.glob("*.doc"))
        
        print(f"Found {len(doc_files)} documents to process")
        
        for doc_file in doc_files:
            output_file = output_path / f"processed_{doc_file.name}"
            
            try:
                self.process_with_retry(str(doc_file), str(output_file))
                print(f"✓ Successfully processed: {doc_file.name}")
            except Exception as e:
                print(f"✗ Failed to process {doc_file.name}: {e}")
        
        print(f"\nSummary: {self.processed_count} processed, {self.error_count} errors")
    
    def close(self):
        """Close the client session."""
        self.client.close()


def batch_text_processing_example():
    """Example of batch processing multiple texts."""
    print("=== Batch Text Processing Example ===")
    
    client = SpeedAIClient(
        api_key=os.getenv("SPEEDAI_API_KEY", "your_api_key"),
        token=os.getenv("SPEEDAI_TOKEN", "your_token")
    )
    
    # Sample texts in different languages
    texts = [
        ("这是第一段需要处理的中文文本。", Language.CHINESE),
        ("This is the second text in English.", Language.ENGLISH),
        ("人工智能技术正在改变世界。", Language.CHINESE),
    ]
    
    results = []
    
    for text, language in texts:
        try:
            # Try rewriting first
            result = client.rewrite_text(text, language, Platform.ZHIWANG)
            results.append({
                "original": text,
                "processed": result.processed,
                "mode": "rewrite",
                "success": True
            })
        except Exception as e:
            # If rewrite fails, try deai
            try:
                result = client.deai_text(text, language, Platform.ZHIWANG)
                results.append({
                    "original": text,
                    "processed": result.processed,
                    "mode": "deai",
                    "success": True
                })
            except Exception as e2:
                results.append({
                    "original": text,
                    "error": str(e2),
                    "success": False
                })
    
    # Print results
    for i, result in enumerate(results, 1):
        print(f"\nText {i}:")
        if result["success"]:
            print(f"  Mode: {result['mode']}")
            print(f"  Original: {result['original']}")
            print(f"  Processed: {result['processed']}")
        else:
            print(f"  Error: {result['error']}")
    
    client.close()


def manual_document_processing_example():
    """Example of manual step-by-step document processing."""
    print("=== Manual Document Processing Example ===")
    
    with SpeedAIClient(
        api_key=os.getenv("SPEEDAI_API_KEY", "your_api_key"),
        token=os.getenv("SPEEDAI_TOKEN", "your_token")
    ) as client:
        
        file_path = "test_document.docx"
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
        
        try:
            # Step 1: Upload
            print("Uploading document...")
            upload_result = client.upload_document(
                file_path=file_path,
                mode=ProcessingMode.DEAI,
                platform=Platform.WEIPU
            )
            
            document_id = upload_result.document_id
            print(f"Document uploaded successfully. ID: {document_id}")
            
            # Step 2: Monitor status
            print("Processing document...")
            max_checks = 30
            check_count = 0
            
            while check_count < max_checks:
                status_result = client.check_document_status(document_id)
                
                print(f"\rProgress: {status_result.progress}%", end="", flush=True)
                
                if status_result.status == ProcessingStatus.COMPLETED:
                    print("\nProcessing completed!")
                    
                    # Step 3: Download
                    output_path = "manually_processed_document.docx"
                    client.download_document(document_id, output_path)
                    print(f"Document downloaded to: {output_path}")
                    break
                    
                elif status_result.status == ProcessingStatus.ERROR:
                    print(f"\nProcessing failed: {status_result.error}")
                    break
                
                time.sleep(2)
                check_count += 1
            
            if check_count >= max_checks:
                print("\nProcessing timeout!")
                
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Run all examples."""
    # Example 1: Batch text processing
    batch_text_processing_example()
    print("\n" + "="*50 + "\n")
    
    # Example 2: Manual document processing
    # Uncomment to run
    # manual_document_processing_example()
    # print("\n" + "="*50 + "\n")
    
    # Example 3: Directory processing
    # Uncomment to run
    # processor = DocumentProcessor(
    #     api_key=os.getenv("SPEEDAI_API_KEY", "your_api_key"),
    #     token=os.getenv("SPEEDAI_TOKEN", "your_token")
    # )
    # processor.process_directory("input_documents", "output_documents")
    # processor.close()


if __name__ == "__main__":
    main()