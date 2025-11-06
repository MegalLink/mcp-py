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


async def get_drive_file(url: str) -> str:
    """
    MCP Tool: Get the text content of a Google Drive file from its URL
    
    Args:
        url: The complete Google Drive URL or file ID
             Examples:
             - https://docs.google.com/document/d/FILE_ID/edit?usp=sharing
             - https://drive.google.com/file/d/FILE_ID/view
             - FILE_ID (direct ID also works)
        
    Returns:
        The file content as a string
    """
    file_id = extract_file_id(url)
    print(f"[FastMCP] Tool request 'get_drive_file' for URL: {url}")
    print(f"[FastMCP] Extracted file_id: {file_id}")
    return await drive_service.get_file_content(file_id)
