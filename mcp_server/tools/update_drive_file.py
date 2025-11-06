"""
Update Drive File Tool
MCP Tool for updating Google Drive file content
"""
from typing import Dict

from services.drive_service import DriveService


# Initialize service
drive_service = DriveService()


async def update_drive_file(file_id: str, content: str) -> Dict[str, str]:
    """
    MCP Tool: Update the content of a specific file in Google Drive
    
    Args:
        file_id: The ID of the file to update
        content: The new content for the file
        
    Returns:
        Dictionary with status and file information
    """
    print(f"[FastMCP] Tool request 'update_drive_file' for: {file_id}")
    return await drive_service.update_file_content(file_id, content)
