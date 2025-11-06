"""
Google Drive Service
Contains business logic for Google Drive operations
"""
import asyncio
from typing import Dict

from gateway.google_drive_client import GoogleDriveClient


class DriveService:
    """Service layer for Google Drive operations"""
    
    def __init__(self):
        self.client = GoogleDriveClient()
    
    async def get_file_content(self, file_id: str, return_json: bool = True) -> str:
        """
        Get the content of a file from Google Drive asynchronously
        
        Args:
            file_id: The ID of the file to read
            return_json: If True, convert Google Docs/Sheets to structured JSON format
            
        Returns:
            The file content as a string (JSON format for Docs/Sheets, or raw content)
            
        Raises:
            ValueError: If the file cannot be read
        """
        try:
            content = await asyncio.to_thread(self.client.read_file, file_id, return_json)
            return content
        except Exception as e:
            raise ValueError(f"No se pudo leer el archivo '{file_id}': {e}")
    
    async def update_file_content(self, file_id: str, content: str) -> Dict[str, str]:
        """
        Update the content of a file in Google Drive asynchronously
        
        Args:
            file_id: The ID of the file to update
            content: The new content for the file
            
        Returns:
            Dictionary with status and file information
            
        Raises:
            ValueError: If the file cannot be updated
        """
        try:
            result = await asyncio.to_thread(self.client.write_file, file_id, content)
            return result
        except Exception as e:
            raise ValueError(f"No se pudo actualizar el archivo '{file_id}': {e}")
