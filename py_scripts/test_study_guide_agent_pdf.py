import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Change to the deployed_agent directory (parent of scripts/)
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


def read_pdf_text(pdf_path):
    """Extract text from PDF file"""
    try:
        import PyPDF2

        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            return text
    except ImportError:
        print("⚠️ PyPDF2 not installed. Installing...")
        os.system("pip install PyPDF2")
        import PyPDF2
        return read_pdf_text(pdf_path)
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None


async def main():
    # Check for PDF path argument
    if len(sys.argv) < 2:
        print("Usage: python3 test_study_guide_agent_pdf.py <path_to_pdf>")
        print("\nExample:")
        print("  python3 test_study_guide_agent_pdf.py ./documents/biology_chapter.pdf")
        exit(1)

    pdf_path = sys.argv[1]

    # Verify PDF file exists
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        exit(1)

    print(f"📄 Reading PDF: {pdf_path}")

    # Extract text from PDF
    pdf_text = read_pdf_text(pdf_path)

    if not pdf_text or not pdf_text.strip():
        print("❌ No text could be extracted from the PDF")
        exit(1)

    print(f"✅ Extracted {len(pdf_text)} characters from PDF")

    # Truncate if too long (max ~30k characters to avoid context issues)
    max_chars = 30000
    if len(pdf_text) > max_chars:
        print(f"⚠️ PDF text is long ({len(pdf_text)} chars), truncating to {max_chars} chars")
        pdf_text = pdf_text[:max_chars] + "\n\n[Content truncated due to length]"

    print(f"📤 Sending to study guide agent...")

    # Create output filename based on PDF name
    pdf_name = Path(pdf_path).stem
    output_file = os.path.join("outputs", f"study_guide_{pdf_name}.md")

    # Ensure outputs directory exists
    os.makedirs("outputs", exist_ok=True)

    print("\n" + "="*80)
    print("🚀 Starting study guide generation...")
    print("="*80 + "\n")

    # Collect all events from the streaming query and print them in real-time
    # Use explicit wording that matches RouterAgent's instruction
    events = []
    async for event in remote_agent.async_stream_query(
        message=f"Create a study guide from this material:\n\n{pdf_text}",
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
    # The SequentialAgent returns multiple events (one per sub-agent)
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
        print(f"📊 Output length: {len(final_output)} characters")
    else:
        print("⚠️ No output received from agent")
        print(f"Total events received: {len(events)}")
        if events:
            import json
            print(f"\nLast event:")
            print(json.dumps(events[-1], indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
