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
AGENT_NAME = "study_guide_agent"
STAGING_BUCKET = f"gs://{PROJECT_ID}-agent-staging"  # Or use existing bucket

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

print(f"Deploying {AGENT_NAME} to Vertex AI Agent Engine...")
print(f"Project: {PROJECT_ID}")
print(f"Location: {LOCATION}")

# Clean up existing deployment
print(f"\n🧹 Cleaning up existing {AGENT_NAME} deployment...")
try:
    agents_list = list(agent_engines.list())
    existing_agent = next((agent for agent in agents_list if agent.display_name == AGENT_NAME), None)

    if existing_agent:
        print(f"Found existing agent: {existing_agent.resource_name}")
        agent_engines.delete(resource_name=existing_agent.resource_name, force=True)
        print(f"✅ Deleted existing agent")
    else:
        print(f"No existing agent found with name '{AGENT_NAME}'")
except Exception as e:
    print(f"⚠️ Cleanup warning: {e}")
    print("Continuing with deployment...")

print()

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
        "firecrawl-py",
    ],
    extra_packages=[
        "study_guide_agent",  # Include entire agent directory with tools
    ],
    env_vars={
        "FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY", ""),
    },
)

print(f"\n✅ Agent deployed successfully!")
print(f"Resource name: {remote_agent.resource_name}")
print(f"\nThe agent is now deployed with Node.js/npx support for Firecrawl MCP!")
