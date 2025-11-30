from google.adk.agents import Agent
import vertexai
import os
import asyncio
from dotenv import load_dotenv
from vertexai import agent_engines

# Load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

## Set your PROJECT_ID and LOCATION
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION

if PROJECT_ID == "your-project-id" or not PROJECT_ID:
    raise ValueError("⚠️ Please replace 'your-project-id' with your actual Google Cloud Project ID.")

print(f"✅ Project ID set to: {PROJECT_ID}")

vertexai.init(
    project=os.environ["GOOGLE_CLOUD_PROJECT"],
    location=os.environ["GOOGLE_CLOUD_LOCATION"],
)

def delete_agents_by_name(agent_names: list[str]):
    """
    Delete agents that match the specified names.

    Args:
        agent_names: List of agent names to delete (e.g., ["study_guide_agent", "my_agent"])
    """
    agents_list = list(agent_engines.list())

    if not agents_list:
        print("❌ No agents found.")
        return

    # Display all available agents
    print(f"\n📋 Found {len(agents_list)} agent(s):")
    for idx, agent in enumerate(agents_list):
        print(f"  {idx + 1}. {agent.display_name} - {agent.resource_name}")

    # Filter agents by name
    agent_names_set = set(agent_names)
    agents_to_delete = [agent for agent in agents_list if agent.display_name in agent_names_set]

    if not agents_to_delete:
        print(f"\n❌ No agents found with names: {agent_names}")
        return

    # Delete matching agents
    print(f"\n🗑️  Deleting {len(agents_to_delete)} agent(s)...")
    for agent in agents_to_delete:
        try:
            agent_engines.delete(resource_name=agent.resource_name, force=True)
            print(f"  ✅ Deleted: {agent.display_name} ({agent.resource_name})")
        except Exception as e:
            print(f"  ❌ Failed to delete {agent.display_name}: {e}")

    print("\n✅ Cleanup complete!")


if __name__ == "__main__":
    import sys

    # Check if agent names were provided as command line arguments
    if len(sys.argv) > 1:
        # Use agent names from command line: python cleanup.py agent1 agent2
        agent_names_to_delete = sys.argv[1:]
    else:
        # Default: no agents to delete (must specify via command line)
        print("⚠️ Usage: python cleanup.py <agent_name1> [agent_name2] ...")
        print("   Example: python cleanup.py study_guide_agent")
        sys.exit(1)

    print(f"🎯 Targeting agents: {agent_names_to_delete}")
    delete_agents_by_name(agent_names_to_delete)
