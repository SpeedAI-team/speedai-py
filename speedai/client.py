import os
import time
import requests
from typing import Optional, Dict, Any, Callable, BinaryIO
from pathlib import Path

from .exceptions import (
    SpeedAIError,
    AuthenticationError,
    ValidationError,
    ProcessingError,
    NetworkError
)
from .models import (
    TextResult,
    DocumentResult,
    ProcessingStatus,
    Language,
    Platform,
    ProcessingMode
)


class SpeedAIClient:
    """
    SpeedAI API Client for text and document processing.
    
    This client provides methods to:
    - Rewrite text to reduce plagiarism
    - Reduce AI detection rate of text
    - Process documents with automatic status polling
    """
    
    def __init__(
        self,
        api_key: str,
        token: str,
        base_url: str = "https://api3.speedai.chat",
        timeout: int = 60
    ):
        """
        Initialize SpeedAI client.
        
        Args:
            api_key: Your SpeedAI API key
            token: Your authentication token
            base_url: API base URL (optional)
            timeout: Request timeout in seconds (default: 30)
        """
        if not api_key or not token:
            raise AuthenticationError("API key and token are required")
        
        self.api_key = api_key
        self.token = token
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
    
    def rewrite_text(
        self,
        text: str,
        language: Language = Language.CHINESE,
        platform: Platform = Platform.ZHIWANG
    ) -> TextResult:
        """
        Rewrite text to reduce plagiarism.
        
        Args:
            text: Text to rewrite
            language: Language of the text (Chinese or English)
            platform: Target platform (zhiwang, weipu, or gezida)
            
        Returns:
            TextResult object containing the rewritten text and metadata
            
        Raises:
            ValidationError: If input parameters are invalid
            ProcessingError: If the API returns an error
            NetworkError: If network request fails
        """
        if not text:
            raise ValidationError("Text cannot be empty")
        
        url = f"{self.base_url}/v1/rewrite"
        payload = {
            "username": self.api_key,
            "info": text,
            "lang": language.value,
            "type": platform.value
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 200:
                return TextResult(
                    original=text,
                    processed=data.get("rewrite", ""),
                    mode=ProcessingMode.REWRITE
                )
            else:
                raise ProcessingError(data.get("message", "Rewrite failed"))
                
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}")
    
    def deai_text(
        self,
        text: str,
        language: Language = Language.CHINESE,
        platform: Platform = Platform.ZHIWANG
    ) -> TextResult:
        """
        Reduce AI detection rate of text.
        
        Args:
            text: Text to process
            language: Language of the text
            platform: Target platform
            
        Returns:
            TextResult object containing the processed text
        """
        if not text:
            raise ValidationError("Text cannot be empty")
        
        url = f"{self.base_url}/v1/deai"
        payload = {
            "username": self.api_key,
            "info": text,
            "lang": language.value,
            "type": platform.value
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 200:
                return TextResult(
                    original=text,
                    processed=data.get("rewrite", ""),
                    mode=ProcessingMode.DEAI
                )
            else:
                raise ProcessingError(data.get("message", "DeAI processing failed"))
                
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}")
    
    def upload_document(
        self,
        file_path: str,
        mode: ProcessingMode = ProcessingMode.REWRITE,
        platform: Platform = Platform.ZHIWANG,
        skip_english: bool = True
    ) -> DocumentResult:
        """
        Upload a document for processing.
        
        Args:
            file_path: Path to the document file (.doc or .docx)
            mode: Processing mode (rewrite or deai)
            platform: Target platform
            skip_english: Whether to skip English content
            
        Returns:
            DocumentResult object with document ID and status
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise ValidationError(f"File not found: {file_path}")
        
        if file_path.suffix.lower() not in ['.doc', '.docx']:
            raise ValidationError("Only .doc and .docx files are supported")
        
        url = f"{self.base_url}/v1/docx"
        
        with open(file_path, 'rb') as f:
            files = {
                'file': (file_path.name, f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            }
            data = {
                'FileName': file_path.name,
                'username': self.api_key,
                'mode': mode.value,
                'type_': platform.value,
                'changed_only': 'false',
                'skip_english': str(skip_english).lower()
            }
            
            try:
                response = self.session.post(
                    url,
                    files=files,
                    data=data,
                    timeout=self.timeout
                )
                response.raise_for_status()
                result = response.json()
                
                if result.get("status") == "processing":
                    return DocumentResult(
                        document_id=result.get("user_doc_id"),
                        status=ProcessingStatus.PROCESSING,
                        progress=0
                    )
                else:
                    raise ProcessingError(result.get("error", "Upload failed"))
                    
            except requests.exceptions.RequestException as e:
                raise NetworkError(f"Network error: {str(e)}")
    
    def check_document_status(self, document_id: str) -> DocumentResult:
        """
        Check the processing status of a document.
        
        Args:
            document_id: Document ID from upload response
            
        Returns:
            DocumentResult object with current status and progress
        """
        url = f"{self.base_url}/v1/docx/status"
        payload = {"user_doc_id": document_id}
        
        try:
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            status_map = {
                "processing": ProcessingStatus.PROCESSING,
                "completed": ProcessingStatus.COMPLETED,
                "error": ProcessingStatus.ERROR
            }
            
            return DocumentResult(
                document_id=document_id,
                status=status_map.get(data.get("status"), ProcessingStatus.ERROR),
                progress=data.get("progress", 0),
                error=data.get("error")
            )
            
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}")
    
    def download_document(
        self,
        document_id: str,
        output_path: str,
        file_name: Optional[str] = None
    ) -> str:
        """
        Download a processed document.
        
        Args:
            document_id: Document ID
            output_path: Path to save the downloaded file
            file_name: Optional custom filename for the request
            
        Returns:
            Path to the downloaded file
        """
        url = f"{self.base_url}/v1/download"
        payload = {
            "user_doc_id": document_id,
            "file_name": file_name or "processed_document"
        }
        
        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=self.timeout,
                stream=True
            )
            response.raise_for_status()
            
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return str(output_path)
            
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}")
    
    def process_document(
        self,
        file_path: str,
        output_path: str,
        mode: ProcessingMode = ProcessingMode.REWRITE,
        platform: Platform = Platform.ZHIWANG,
        skip_english: bool = True,
        progress_callback: Optional[Callable[[int, str], None]] = None,
        poll_interval: int = 2,
        max_wait_time: int = 300
    ) -> str:
        """
        Upload, process, and download a document with automatic polling.
        
        Args:
            file_path: Path to the input document
            output_path: Path to save the processed document
            mode: Processing mode
            platform: Target platform
            skip_english: Whether to skip English content
            progress_callback: Optional callback for progress updates
            poll_interval: Seconds between status checks
            max_wait_time: Maximum seconds to wait for processing
            
        Returns:
            Path to the downloaded processed document
        """
        # Upload document
        upload_result = self.upload_document(file_path, mode, platform, skip_english)
        document_id = upload_result.document_id
        
        if progress_callback:
            progress_callback(0, "Document uploaded")
        
        # Poll for completion
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            status_result = self.check_document_status(document_id)
            
            if progress_callback:
                progress_callback(status_result.progress, status_result.status.value)
            
            if status_result.status == ProcessingStatus.COMPLETED:
                # Download the processed document
                return self.download_document(document_id, output_path)
            elif status_result.status == ProcessingStatus.ERROR:
                raise ProcessingError(f"Document processing failed: {status_result.error}")
            
            time.sleep(poll_interval)
        
        raise ProcessingError("Processing timeout exceeded")
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()