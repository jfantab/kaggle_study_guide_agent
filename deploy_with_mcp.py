#!/usr/bin/env python3
"""
Deploy study guide agent to Vertex AI Agent Engine with MCP support.

This script uses the Agent Engine API directly to enable custom installation
scripts for Node.js/npx required by Firecrawl MCP server.
"""

import os
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-west1")
AGENT_NAME = "study-guide-agent"
STAGING_BUCKET = f"gs://{PROJECT_ID}-agent-staging"  # Or use existing bucket

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

print(f"Deploying {AGENT_NAME} to Vertex AI Agent Engine...")
print(f"Project: {PROJECT_ID}")
print(f"Location: {LOCATION}")

# Import the agent
from study_guide_agent.agent import root_agent

# Deploy agent with custom installation script for Node.js/MCP
remote_agent = agent_engines.create(
    root_agent,  # Pass agent as positional argument
    display_name=AGENT_NAME,
    description="Study guide generator with Firecrawl MCP web research",
    requirements=[
        "google-adk",
        "opentelemetry-instrumentation-google-genai",
        "mcp",
        "python-dotenv",
        "google-cloud-aiplatform",
    ],
    extra_packages=[
        "study_guide_agent/installation_scripts/install_nodejs_mcp.sh",
    ],
    env_vars={
        "FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY", ""),
    },
    build_options={
        "installation": [
            "bash study_guide_agent/installation_scripts/install_nodejs_mcp.sh",
        ],
    },
)

print(f"\n✅ Agent deployed successfully!")
print(f"Resource name: {remote_agent.resource_name}")
print(f"\nThe agent is now deployed with Node.js/npx support for Firecrawl MCP!")
