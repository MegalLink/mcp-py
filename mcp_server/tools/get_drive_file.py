"""
Get Drive File Tool
MCP Tool for reading Google Drive file content from URL
"""
import re
from services.drive_service import DriveService


# Initialize service
drive_service = DriveService()


def extract_file_id(url: str) -> str:
    """
    Extract the file ID from a Google Drive URL
    
    Args:
        url: The complete Google Drive URL or just the file ID
        
    Returns:
        The extracted file ID
        
    Examples:
        >>> extract_file_id("https://docs.google.com/document/d/1h9sRNgBe.../edit")
        "1h9sRNgBe..."
        >>> extract_file_id("1h9sRNgBe...")
        "1h9sRNgBe..."
    """
    # If it's already just an ID (no slashes), return as is
    if '/' not in url:
        return url
    
    # Pattern to match Google Drive file IDs in URLs
    # Matches: /d/{file_id}/ or /d/{file_id}? or /d/{file_id}#
    pattern = r'/d/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    
    # If no pattern matched, assume it's already a file ID
    return url


async def get_drive_file(url: str, return_json: bool = True) -> str:
    """
    MCP Tool: Get the content of a Google Drive file from its URL
    
    Args:
        url: The complete Google Drive URL or file ID
             Examples:
             - https://docs.google.com/document/d/FILE_ID/edit?usp=sharing
             - https://drive.google.com/file/d/FILE_ID/view
             - FILE_ID (direct ID also works)
        return_json: If True, convert Google Docs/Sheets to structured JSON format.
                    If False, return raw markdown/csv content.
        
    Returns:
        The file content as a string (JSON format for Google Workspace files by default)
        
    JSON Structure for Google Docs:
        {
            "file_name": "Document Name",
            "type": "google_docs",
            "format": "json",
            "sections": [
                {
                    "type": "heading",
                    "title": "Section Title",
                    "level": 1,
                    "content": "Section content..."
                }
            ],
            "raw_content": "Original markdown content"
        }
        
    JSON Structure for Google Sheets:
        {
            "file_name": "Sheet Name",
            "type": "google_sheets",
            "format": "json",
            "rows": 100,
            "columns": ["Column1", "Column2"],
            "data": [{"Column1": "value1", "Column2": "value2"}]
        }
    """
    file_id = extract_file_id(url)
    print(f"[FastMCP] Tool request 'get_drive_file' for URL: {url}")
    print(f"[FastMCP] Extracted file_id: {file_id}")
    print(f"[FastMCP] return_json: {return_json}")
    return await drive_service.get_file_content(file_id, return_json)
