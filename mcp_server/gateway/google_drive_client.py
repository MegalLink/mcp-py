"""
Google Drive Gateway
Handles all interactions with Google Drive API
"""
import io
import os
import json
import csv
from typing import Optional, Dict, Any

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


class GoogleDriveClient:
    """Client for interacting with Google Drive API"""
    
    def __init__(self):
        self.service = None
        self._initialize_service()
    
    def _initialize_service(self) -> None:
        """Initialize Google Drive service with credentials"""
        app_env = os.getenv('APP_ENV', 'development')
        
        if app_env == 'production':
            print("Modo: PRODUCCIÓN (leyendo secreto de Docker)")
            service_account_file = '/run/secrets/google_creds'
        else:
            print("Modo: DESARROLLO (leyendo 'credentials.json' local)")
            service_account_file = 'credentials.json'
        
        scopes = ['https://www.googleapis.com/auth/drive']
        
        try:
            if not os.path.exists(service_account_file):
                print(f"Error: No se encontró el archivo de credenciales en '{service_account_file}'")
                if app_env == 'development':
                    print("Asegúrate de que 'credentials.json' esté en la misma carpeta que main.py")
                return
            
            creds = service_account.Credentials.from_service_account_file(
                service_account_file, scopes=scopes
            )
            self.service = build('drive', 'v3', credentials=creds)
            print("Servicio de Google Drive inicializado correctamente.")
        except Exception as e:
            print(f"Error fatal al inicializar Google Drive: {e}")
    
    def _convert_markdown_to_json(self, markdown_content: str, file_name: str) -> str:
        """
        Convert Markdown content to structured JSON format
        
        Args:
            markdown_content: The markdown text content
            file_name: Name of the file
            
        Returns:
            JSON string with structured content
        """
        lines = markdown_content.split('\n')
        sections = []
        current_section = None
        current_content = []
        
        for line in lines:
            # Detect headers
            if line.startswith('#'):
                # Save previous section if exists
                if current_section is not None:
                    sections.append({
                        "type": current_section["type"],
                        "title": current_section["title"],
                        "level": current_section["level"],
                        "content": '\n'.join(current_content).strip()
                    })
                
                # Start new section
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                current_section = {
                    "type": "heading",
                    "title": title,
                    "level": level
                }
                current_content = []
            else:
                # Add content to current section
                if line.strip():
                    current_content.append(line)
        
        # Add last section
        if current_section is not None:
            sections.append({
                "type": current_section["type"],
                "title": current_section["title"],
                "level": current_section["level"],
                "content": '\n'.join(current_content).strip()
            })
        
        # If no sections were found, treat all content as body
        if not sections:
            sections.append({
                "type": "body",
                "content": markdown_content.strip()
            })
        
        result = {
            "file_name": file_name,
            "type": "google_docs",
            "format": "json",
            "sections": sections,
            "raw_content": markdown_content
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def _convert_csv_to_json(self, csv_content: str, file_name: str) -> str:
        """
        Convert CSV content to JSON array
        
        Args:
            csv_content: The CSV text content
            file_name: Name of the file
            
        Returns:
            JSON string with array of objects
        """
        lines = csv_content.strip().split('\n')
        if not lines:
            return json.dumps({"file_name": file_name, "type": "google_sheets", "data": []})
        
        reader = csv.DictReader(lines)
        data = list(reader)
        
        result = {
            "file_name": file_name,
            "type": "google_sheets",
            "format": "json",
            "rows": len(data),
            "columns": list(data[0].keys()) if data else [],
            "data": data
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def read_file(self, file_id: str, return_json: bool = True) -> str:
        """
        Read content from a Google Drive file
        
        Supports both:
        - Binary files (PDFs, images, etc.) - downloaded directly
        - Google Workspace files - exported and optionally converted to JSON:
          * Google Docs → JSON structured format (sections, headings, content)
          * Google Sheets → JSON array of objects
          * Google Slides → Plain text
        
        Args:
            file_id: The ID of the file to read
            return_json: If True, converts Google Docs and Sheets to JSON format
            
        Returns:
            The file content as a string (JSON for Docs/Sheets if return_json=True)
            
        Raises:
            Exception: If the service is not initialized or read fails
        """
        if not self.service:
            raise Exception("Servicio de Drive no inicializado.")
        
        try:
            # First, get file metadata to determine the type
            file_metadata = self.service.files().get(
                fileId=file_id,
                fields='mimeType, name'
            ).execute()
            
            mime_type = file_metadata.get('mimeType', '')
            file_name = file_metadata.get('name', 'unknown')
            
            print(f"[Google Drive] Reading file: {file_name}")
            print(f"[Google Drive] MIME type: {mime_type}")
            
            # Map of Google Workspace MIME types to export formats
            google_docs_types = {
                'application/vnd.google-apps.document': 'text/markdown',  # Google Docs → Markdown → JSON (MEJOR OPCIÓN)
                # Alternativa HTML (más compleja de parsear):
                # 'application/vnd.google-apps.document': 'text/html',  # Google Docs → HTML → JSON
                'application/vnd.google-apps.spreadsheet': 'text/csv',  # Google Sheets → CSV → JSON
                'application/vnd.google-apps.presentation': 'text/plain',  # Google Slides → Plain text
                'application/vnd.google-apps.script': 'application/vnd.google-apps.script+json',  # Apps Script → JSON
            }
            
            # Check if it's a Google Workspace file that needs export
            if mime_type in google_docs_types:
                export_mime_type = google_docs_types[mime_type]
                print(f"[Google Drive] Exporting as: {export_mime_type}")
                
                request = self.service.files().export_media(
                    fileId=file_id,
                    mimeType=export_mime_type
                )
            else:
                # Regular binary file - download directly
                print(f"[Google Drive] Downloading binary file")
                request = self.service.files().get_media(fileId=file_id)
            
            # Download the content
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            
            while not done:
                status, done = downloader.next_chunk()
            
            fh.seek(0)
            content = fh.read().decode('utf-8')
            
            # Convert to JSON if requested and applicable
            if return_json:
                if mime_type == 'application/vnd.google-apps.document':
                    print(f"[Google Drive] Converting to JSON format")
                    return self._convert_markdown_to_json(content, file_name)
                elif mime_type == 'application/vnd.google-apps.spreadsheet':
                    print(f"[Google Drive] Converting CSV to JSON format")
                    return self._convert_csv_to_json(content, file_name)
            
            return content
            
        except Exception as e:
            print(f"Error en lectura de Drive: {e}")
            raise e
    
    def write_file(self, file_id: str, content: str) -> dict:
        """
        Write content to a Google Drive file
        
        Args:
            file_id: The ID of the file to update
            content: The content to write
            
        Returns:
            Dictionary with status and file name
            
        Raises:
            Exception: If the service is not initialized or write fails
        """
        if not self.service:
            raise Exception("Servicio de Drive no inicializado.")
        
        try:
            fh = io.BytesIO(content.encode('utf-8'))
            media_body = MediaFileUpload(
                fh.name,
                mimetype='text/plain',
                resumable=True,
                fd=fh
            )
            
            updated_file = self.service.files().update(
                fileId=file_id,
                media_body=media_body,
                fields='id, name'
            ).execute()
            
            return {
                "status": "success",
                "file_name": updated_file.get('name')
            }
        except Exception as e:
            print(f"Error en escritura de Drive: {e}")
            raise e
