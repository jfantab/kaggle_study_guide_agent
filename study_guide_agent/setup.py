import os
import vertexai


def setup_environment():
    """Initialize environment variables and Vertex AI

    Note: When deployed to Agent Engine, environment variables should already be set.
    For local testing, use .env file with python-dotenv.
    """
    # Increase timeout for authentication and API calls (helps with network issues)
    os.environ.setdefault('GOOGLE_AUTH_TOKEN_URI_TIMEOUT', '300')  # 5 minutes
    os.environ.setdefault('GOOGLE_API_TIMEOUT', '300')  # 5 minutes

    # Try to load dotenv for local development (optional)
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        # dotenv not available - that's fine for deployed environments
        pass

    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
    FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

    if not PROJECT_ID:
        raise ValueError("⚠️ GOOGLE_CLOUD_PROJECT not found in environment variables")
    if not LOCATION:
        raise ValueError("⚠️ GOOGLE_CLOUD_LOCATION not found in environment variables")
    if not FIRECRAWL_API_KEY:
        print("⚠️ Warning: FIRECRAWL_API_KEY not found. Research agent will not function properly.")

    if PROJECT_ID == "your-project-id":
        raise ValueError("⚠️ Please replace 'your-project-id' with your actual Google Cloud Project ID.")

    print(f"✅ Project ID set to: {PROJECT_ID}")
    if FIRECRAWL_API_KEY:
        print(f"✅ Firecrawl API key configured")

    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION,
    )
