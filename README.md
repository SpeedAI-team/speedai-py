# SpeedAI Python Package

Official Python package for SpeedAI document and text processing API.

## Installation

### Install from PyPI

```bash
pip install speedai
```

## Quick Start

```python
from speedai import SpeedAIClient, Language, Platform, ProcessingMode

# Initialize client
client = SpeedAIClient(
    api_key="your_api_key",
    token="your_token"
)

# Rewrite text
result = client.rewrite_text(
    text="您的文本内容",
    language=Language.CHINESE,
    platform=Platform.ZHIWANG
)
print(f"Rewritten: {result.processed}")

# Process document
output_path = client.process_document(
    file_path="document.docx",
    output_path="processed_document.docx",
    mode=ProcessingMode.REWRITE,
    progress_callback=lambda p, s: print(f"Progress: {p}% - {s}")
)
```

## Features

- 🚀 Simple and intuitive API
- 📄 Support for .doc and .docx files
- 🌏 Multiple language support (Chinese/English)
- 🎯 Multiple platform targeting (知网/维普/格子达)
- ⚡ Automatic status polling for document processing
- 🔄 Progress tracking with callbacks
- 🛡️ Comprehensive error handling
- 🔌 Context manager support

## API Reference

### Client Initialization

```python
from speedai import SpeedAIClient

client = SpeedAIClient(
    api_key="your_api_key",    # Required
    token="your_token",         # Required
    base_url="https://api3.speedai.chat",  # Optional
    timeout=60                  # Optional, in seconds
)
```

### Text Processing

#### Rewrite Text (降重)

```python
from speedai import Language, Platform

result = client.rewrite_text(
    text="需要降重的文本",
    language=Language.CHINESE,
    platform=Platform.ZHIWANG
)

print(f"Original: {result.original}")
print(f"Processed: {result.processed}")
print(f"Characters: {result.characters}")
```

#### Reduce AI Detection (降AIGC)

```python
result = client.deai_text(
    text="AI generated text",
    language=Language.ENGLISH,
    platform=Platform.WEIPU
)
```

### Document Processing

#### Simple Processing (with auto-polling)

```python
from speedai import ProcessingMode

# Process document with automatic polling
output_path = client.process_document(
    file_path="input.docx",
    output_path="output.docx",
    mode=ProcessingMode.REWRITE,
    platform=Platform.ZHIWANG,
    skip_english=True,
    progress_callback=lambda progress, status: print(f"{progress}% - {status}")
)
```

#### Manual Processing (step by step)

```python
# 1. Upload document
upload_result = client.upload_document(
    file_path="document.docx",
    mode=ProcessingMode.DEAI,
    platform=Platform.GEZIDA
)
document_id = upload_result.document_id

# 2. Check status
import time
while True:
    status = client.check_document_status(document_id)
    print(f"Progress: {status.progress}%")
    
    if status.status == ProcessingStatus.COMPLETED:
        break
    elif status.status == ProcessingStatus.ERROR:
        print(f"Error: {status.error}")
        break
    
    time.sleep(2)

# 3. Download processed document
if status.status == ProcessingStatus.COMPLETED:
    output_path = client.download_document(
        document_id=document_id,
        output_path="processed.docx"
    )
```

### Using Enums

The SDK provides enums for better type safety:

```python
from speedai import Language, Platform, ProcessingMode, ProcessingStatus

# Languages
Language.CHINESE  # "Chinese"
Language.ENGLISH  # "English"

# Platforms
Platform.ZHIWANG  # "zhiwang" - 知网
Platform.WEIPU    # "weipu" - 维普
Platform.GEZIDA   # "gezida" - 格子达

# Processing Modes
ProcessingMode.REWRITE  # "rewrite" - 降重
ProcessingMode.DEAI     # "deai" - 降AIGC

# Processing Status
ProcessingStatus.PROCESSING  # Document is being processed
ProcessingStatus.COMPLETED   # Processing completed
ProcessingStatus.ERROR       # Processing failed
```

### Context Manager

The client supports context manager for automatic resource cleanup:

```python
with SpeedAIClient(api_key="key", token="token") as client:
    result = client.rewrite_text("text")
    # Session is automatically closed when exiting the context
```

### Error Handling

The SDK provides specific exception types:

```python
from speedai import (
    SpeedAIError,
    AuthenticationError,
    ValidationError,
    ProcessingError,
    NetworkError
)

try:
    result = client.rewrite_text("")
except ValidationError as e:
    print(f"Invalid input: {e}")
except ProcessingError as e:
    print(f"Processing failed: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
except SpeedAIError as e:
    print(f"General error: {e}")
```

## Examples

### Batch Text Processing

```python
texts = [
    "第一段文本",
    "第二段文本",
    "第三段文本"
]

for text in texts:
    try:
        result = client.rewrite_text(text)
        print(f"Processed: {result.processed}")
    except Exception as e:
        print(f"Error processing text: {e}")
```

### Processing Multiple Documents

```python
import os
from pathlib import Path

input_dir = Path("documents")
output_dir = Path("processed")
output_dir.mkdir(exist_ok=True)

for doc_path in input_dir.glob("*.docx"):
    print(f"Processing {doc_path.name}...")
    
    try:
        output_path = output_dir / f"processed_{doc_path.name}"
        client.process_document(
            file_path=str(doc_path),
            output_path=str(output_path),
            progress_callback=lambda p, s: print(f"  {p}% - {s}")
        )
        print(f"  Saved to: {output_path}")
    except Exception as e:
        print(f"  Error: {e}")
```

### Custom Progress Tracking

```python
from datetime import datetime

def progress_tracker(progress, status):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] Progress: {progress}% - Status: {status}")

output_path = client.process_document(
    file_path="large_document.docx",
    output_path="processed_large.docx",
    progress_callback=progress_tracker,
    poll_interval=3,  # Check every 3 seconds
    max_wait_time=600  # Max 10 minutes
)
```

## Environment Variables

You can use environment variables for credentials:

```python
import os
from speedai import SpeedAIClient

client = SpeedAIClient(
    api_key=os.getenv("SPEEDAI_API_KEY"),
    token=os.getenv("SPEEDAI_TOKEN")
)
```

## Rate Limiting and Best Practices

1. **Batch Processing**: Process multiple texts in sequence, not in parallel
2. **Error Handling**: Always handle exceptions appropriately
3. **Resource Management**: Use context managers or close sessions explicitly
4. **Timeouts**: Adjust timeout values for large documents
5. **Progress Tracking**: Implement callbacks for better user experience

## Requirements

- Python 3.6 or higher
- requests >= 2.25.0
- aiohttp >= 3.8.0 (for async support)
- typing-extensions >= 4.0.0

## Development

### Running Tests

```bash
pip install -e .[dev]
pytest
```

### Code Formatting

```bash
black speedai
flake8 speedai
```

## License

MIT License

## Support

For issues and feature requests, please visit:
- GitHub Issues: https://github.com/yourusername/speedai/issues
- Documentation: https://github.com/yourusername/speedai/wiki