import os
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters


def get_firecrawl_toolset():
    """Returns configured Firecrawl MCP toolset for web search and content extraction

    Returns:
        McpToolset: Configured Firecrawl MCP tools including:
            - firecrawl_search: Web search with content extraction
            - firecrawl_scrape: Extract content from URLs
            - firecrawl_batch_scrape: Process multiple URLs
            - firecrawl_map: Discover site structure
            - firecrawl_extract: Structured data extraction

    Raises:
        ValueError: If FIRECRAWL_API_KEY is not set
    """
    # Load Firecrawl API key from environment
    firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")

    if not firecrawl_api_key:
        raise ValueError("FIRECRAWL_API_KEY environment variable is required for Firecrawl toolset")

    # Configure Firecrawl MCP toolset
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "firecrawl-mcp"],
                env={
                    "FIRECRAWL_API_KEY": firecrawl_api_key,
                    "FIRECRAWL_RETRY_MAX_ATTEMPTS": "3",
                    "FIRECRAWL_CREDIT_WARNING_THRESHOLD": "1000"
                }
            ),
            timeout=30,
        ),
    )
