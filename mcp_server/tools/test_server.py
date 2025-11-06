"""
Test Server Tool
MCP Tool for testing server connectivity
"""


async def test_server() -> str:
    """
    MCP Tool: Simple connection test to verify the server is responding
    
    Returns:
        Success message
    """
    print("[FastMCP] Tool request 'test_server' received.")
    return "Test de mcp py exitosa"
