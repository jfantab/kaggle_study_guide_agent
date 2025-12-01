"""
Firecrawl FunctionTool for deployment compatibility.

This uses the Firecrawl Python SDK directly instead of MCP, which allows
it to be serialized and deployed to Vertex AI Agent Engine.
"""

import os
from google.adk.tools import FunctionTool
from typing import Optional


def firecrawl_search(query: str, limit: int = 5) -> str:
    """Search the web using Firecrawl and return relevant content.

    Args:
        query: Search query to find relevant educational content
        limit: Maximum number of results to return (default: 5)

    Returns:
        Formatted string with search results including titles, URLs, and content
    """
    try:
        # Import here to avoid issues if firecrawl-py is not installed
        from firecrawl import FirecrawlApp

        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            return "Error: FIRECRAWL_API_KEY environment variable not set"

        app = FirecrawlApp(api_key=api_key)

        # Perform search with markdown format
        results = app.search(query, params={
            "limit": limit,
            "scrapeOptions": {"formats": ["markdown"]}
        })

        # Format results
        if not results or "data" not in results:
            return f"No results found for query: {query}"

        formatted_results = []
        for idx, item in enumerate(results.get("data", [])[:limit], 1):
            title = item.get("title", "No title")
            url = item.get("url", "No URL")
            content = item.get("markdown", item.get("content", "No content available"))

            # Truncate content to first 500 characters
            if len(content) > 500:
                content = content[:500] + "..."

            formatted_results.append(
                f"{idx}. {title}\n"
                f"   URL: {url}\n"
                f"   Content: {content}\n"
            )

        return "\n".join(formatted_results)

    except ImportError:
        return "Error: firecrawl-py package not installed. Install with: pip install firecrawl-py"
    except Exception as e:
        return f"Error performing search: {str(e)}"


def firecrawl_scrape(url: str) -> str:
    """Scrape content from a specific URL using Firecrawl.

    Args:
        url: The URL to scrape content from

    Returns:
        Scraped content in markdown format
    """
    try:
        from firecrawl import FirecrawlApp

        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            return "Error: FIRECRAWL_API_KEY environment variable not set"

        app = FirecrawlApp(api_key=api_key)

        # Scrape the URL
        result = app.scrape_url(url, params={
            "formats": ["markdown"]
        })

        if not result:
            return f"Failed to scrape URL: {url}"

        content = result.get("markdown", result.get("content", "No content available"))

        # Truncate if too long
        if len(content) > 2000:
            content = content[:2000] + "...\n\n[Content truncated]"

        return f"Content from {url}:\n\n{content}"

    except ImportError:
        return "Error: firecrawl-py package not installed. Install with: pip install firecrawl-py"
    except Exception as e:
        return f"Error scraping URL: {str(e)}"


# Create FunctionTool instances
firecrawl_search_tool = FunctionTool(firecrawl_search)
firecrawl_scrape_tool = FunctionTool(firecrawl_scrape)


def get_firecrawl_function_tools():
    """Returns list of Firecrawl FunctionTools for deployment.

    These tools work in both local development and production deployment,
    unlike MCP tools which only work locally.
    """
    return [firecrawl_search_tool, firecrawl_scrape_tool]
