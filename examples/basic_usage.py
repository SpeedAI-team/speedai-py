"""
Basic usage example for SpeedAI package
"""

import os
from speedai import SpeedAIClient, Language, Platform, ProcessingMode

# Get credentials from environment or set directly
API_KEY = os.getenv("SPEEDAI_API_KEY", "your_api_key")
TOKEN = os.getenv("SPEEDAI_TOKEN", "your_token")


def main():
    # Initialize client
    client = SpeedAIClient(api_key=API_KEY, token=TOKEN)
    
    # Example 1: Rewrite Chinese text
    print("=== Example 1: Text Rewriting ===")
    chinese_text = "人工智能技术的快速发展正在深刻改变我们的生活方式。从智能手机到自动驾驶汽车，AI已经渗透到日常生活的方方面面。"
    
    try:
        result = client.rewrite_text(
            text=chinese_text,
            language=Language.CHINESE,
            platform=Platform.ZHIWANG
        )
        print(f"Original: {result.original}")
        print(f"Rewritten: {result.processed}")
        print(f"Characters processed: {result.characters}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Reduce AI detection for English text
    print("\n=== Example 2: AI Detection Reduction ===")
    english_text = "The rapid advancement of artificial intelligence technology is fundamentally transforming our daily lives."
    
    try:
        result = client.deai_text(
            text=english_text,
            language=Language.ENGLISH,
            platform=Platform.ZHIWANG
        )
        print(f"Original: {result.original}")
        print(f"Processed: {result.processed}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Document processing
    print("\n=== Example 3: Document Processing ===")
    print("Note: This example requires a document.docx file")
    
    # Uncomment to test document processing
    # try:
    #     output_path = client.process_document(
    #         file_path="document.docx",
    #         output_path="processed_document.docx",
    #         mode=ProcessingMode.REWRITE,
    #         platform=Platform.ZHIWANG,
    #         progress_callback=lambda p, s: print(f"Progress: {p}% - Status: {s}")
    #     )
    #     print(f"Document processed and saved to: {output_path}")
    # except Exception as e:
    #     print(f"Error: {e}")
    
    # Close the client session
    client.close()


if __name__ == "__main__":
    main()