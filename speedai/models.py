from enum import Enum
from dataclasses import dataclass
from typing import Optional


class Language(Enum):
    """Supported languages."""
    CHINESE = "Chinese"
    ENGLISH = "English"


class Platform(Enum):
    """Target platforms for processing."""
    ZHIWANG = "zhiwang"
    WEIPU = "weipu"
    GEZIDA = "gezida"


class ProcessingMode(Enum):
    """Processing modes."""
    REWRITE = "rewrite"
    DEAI = "deai"


class ProcessingStatus(Enum):
    """Document processing status."""
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class TextResult:
    """Result of text processing."""
    original: str
    processed: str
    mode: ProcessingMode


@dataclass
class DocumentResult:
    """Result of document processing."""
    document_id: str
    status: ProcessingStatus
    progress: int = 0
    error: Optional[str] = None