import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Change to the deployed_agent directory (parent of py_scripts/)
script_dir = Path(__file__).parent
deployed_agent_dir = script_dir.parent
os.chdir(deployed_agent_dir)

# Load environment variables from .env file
load_dotenv()

# Import these AFTER removing API key from environment
import vertexai
from vertexai import agent_engines

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

if not PROJECT_ID:
    raise ValueError("⚠️ GOOGLE_CLOUD_PROJECT not found in .env file")
if not LOCATION:
    raise ValueError("⚠️ GOOGLE_CLOUD_LOCATION not found in .env file")

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

# Get the study_guide_agent by name
agents_list = list(agent_engines.list())
remote_agent = None
for agent in agents_list:
    if agent.display_name == "study_guide_agent":
        remote_agent = agent
        break

if remote_agent:
    client = agent_engines
    print(f"✅ Connected to deployed agent: {remote_agent.resource_name}")
else:
    print("❌ study_guide_agent not found. Please deploy first.")
    exit(1)

async def main():
    sample_material = """
    Photosynthesis is the process by which plants convert light energy into chemical energy.
    During photosynthesis, plants use sunlight, water, and carbon dioxide to create oxygen and glucose.
    This process occurs in the chloroplasts of plant cells, specifically in structures called thylakoids.
    The overall equation is: 6CO2 + 6H2O + light energy → C6H12O6 + 6O2.
    """

    output_file = os.path.join("outputs", "study_guide_output.md")

    print("\n" + "="*80)
    print("🚀 Starting study guide generation...")
    print("="*80 + "\n")

    # Collect all events from the streaming query and print them in real-time
    events = []
    async for event in remote_agent.async_stream_query(
        message=f"Please create a study guide from this material:\n\n{sample_material}",
        user_id="user_42",
    ):
        events.append(event)

        # Print intermediate agent outputs in real-time
        if "content" in event and "parts" in event["content"]:
            for part in event["content"]["parts"]:
                # Print text responses from agents
                if "text" in part:
                    text = part["text"]
                    # Determine which agent is responding based on content
                    if text.strip():
                        print(f"\n📝 Agent Output:\n{text}\n")
                        print("-" * 80)

                # Print function responses
                elif "function_response" in part:
                    func_name = part.get("name", "unknown")
                    print(f"\n🔧 Function Called: {func_name}")
                    print("-" * 80)

    # Extract the final study guide from the last text output
    # The SequentialAgent returns multiple events:
    #   1. OverviewAgent output
    #   2. ElaborationLoop output (with multiple iterations)
    #   3. AssemblerAgent output
    #   4. JudgeAgent output (final polished study guide)
    # We want the final output from JudgeAgent (the last agent in the sequence)
    final_output = None

    # Search from the end to get the most recent text output
    for event in reversed(events):
        if "content" in event and "parts" in event["content"]:
            for part in event["content"]["parts"]:
                # Check for function_response containing the study guide
                if "function_response" in part:
                    response = part["function_response"].get("response", {})
                    if "result" in response:
                        final_output = response["result"]
                        break
                # Check for direct text responses (preferred - from SequentialAgent)
                elif "text" in part:
                    text = part["text"]
                    # Only accept text that looks like a complete study guide
                    # (has substantial content and quality seal)
                    if len(text) > 500 and "✅ Quality Verified" in text:
                        final_output = text
                        break
            if final_output:
                break

    # Write the final output
    if final_output:
        with open(output_file, "w") as f:
            f.write(final_output)
        print(f"✅ Study guide written to {output_file}")
    else:
        print("⚠️ No text output received from agent")
        print(f"Total events received: {len(events)}")
        if events:
            print(f"Last event: {events[-1]}")

if __name__ == "__main__":
    asyncio.run(main())
