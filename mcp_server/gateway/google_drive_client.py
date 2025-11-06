"""
Google Drive Gateway
Handles all interactions with Google Drive API
"""
import io
import os
from typing import Optional

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
    
    def read_file(self, file_id: str) -> str:
        """
        Read content from a Google Drive file
        
        Supports both:
        - Binary files (PDFs, images, etc.) - downloaded directly
        - Google Workspace files (Docs, Sheets, Slides) - exported as text/plain
        
        Args:
            file_id: The ID of the file to read
            
        Returns:
            The file content as a string
            
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
                'application/vnd.google-apps.document': 'text/plain',  # Google Docs
                'application/vnd.google-apps.spreadsheet': 'text/csv',  # Google Sheets
                'application/vnd.google-apps.presentation': 'text/plain',  # Google Slides
                'application/vnd.google-apps.script': 'application/vnd.google-apps.script+json',  # Apps Script
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
            return fh.read().decode('utf-8')
            
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
