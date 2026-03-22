from fastmcp import FastMCP
from langchain_community.utilities import SearxSearchWrapper
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure SearxNG connection settings
SEARXNG_HOST = os.getenv("SEARXNG_HOST", "http://localhost")
SEARXNG_PORT = os.getenv("SEARXNG_PORT", "8080")
searx_url = f"{SEARXNG_HOST}:{SEARXNG_PORT}"

logger.info(f"Connecting to SearXNG at: {searx_url}")

try:
    search_wrapper = SearxSearchWrapper(searx_host=searx_url)
    logger.info("SearXNG connection established successfully")
except Exception as e:
    logger.error(f"Failed to connect to SearXNG: {e}")
    search_wrapper = None

mcp = FastMCP("SearXNG Web Search")

@mcp.tool
def internet_search(
    query: str,
    num_results: int = 5,
) -> list:
    """
    MCP Tool: Perform a web search and return structured JSON results.
    """
    if not search_wrapper:
        raise Exception("SearXNG connection not available. Check your configuration.")
    
    try:
        return search_wrapper.results(query=query, num_results=num_results)
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise Exception(f"Searx API returned an error: {str(e)}")

@mcp.tool
def internet_search_text(query: str) -> str:
    """
    MCP Tool: Perform a web search and return human-readable text summary.
    """
    if not search_wrapper:
        raise Exception("SearXNG connection not available. Check your configuration.")
    
    try:
        return search_wrapper.run(query=query)
    except Exception as e:
        logger.error(f"Search text error: {e}")
        raise Exception(f"Searx API returned an error: {str(e)}")

if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=int(os.getenv("SEARXNG_MCP_PORT", "8081")),
    )
