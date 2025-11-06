"""
MCP Server - Google Drive Integration
Entry point for the Model Context Protocol server
"""
from mcp.server.fastmcp import FastMCP

# Import tools
from tools.get_drive_file import get_drive_file
from tools.update_drive_file import update_drive_file
from tools.test_server import test_server


# Create FastMCP server instance
mcp = FastMCP("Google Drive Server")


# Register tools
@mcp.tool()
async def get_drive_file_tool(url: str, return_json: bool = True) -> str:
    """
    Tool: Get the content of a Google Drive file from its URL
    
    Args:
        url: The complete Google Drive URL or file ID
             Examples:
             - https://docs.google.com/document/d/FILE_ID/edit?usp=sharing
             - https://drive.google.com/file/d/FILE_ID/view
             - FILE_ID (direct ID also works)
        return_json: If True (default), convert Google Docs/Sheets to structured JSON.
                    If False, return raw markdown/csv content.
                    
    Returns:
        String containing the file content (JSON format for Google Workspace files by default)
    """
    return await get_drive_file(url, return_json)


@mcp.tool()
async def update_drive_file_tool(file_id: str, content: str) -> dict:
    """
    Tool: Update the content of a specific file in Google Drive
    """
    return await update_drive_file(file_id, content)


@mcp.tool()
async def test_server_tool() -> str:
    """
    Tool: Execute a simple connection test to verify the server is responding
    """
    return await test_server()