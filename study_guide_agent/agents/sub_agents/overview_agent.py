from google.adk.agents import Agent
from ...tools.firecrawl_mcp import get_firecrawl_toolset


def create_overview_agent():
    """Creates the overview agent for generating high-level study guide structure

    This agent uses web search to gather additional context and information
    before creating learning objectives and study guide structure.
    """
    # Configure tools for web search
    try:
        firecrawl_tools = get_firecrawl_toolset()
        tools = [firecrawl_tools]
    except ValueError as e:
        # If Firecrawl API key is not set, agent will work without search
        print(f"⚠️ Warning: {e}")
        print("⚠️ Overview agent will work without web search capability")
        tools = None

    return Agent(
        name="OverviewAgent",
        model="gemini-2.5-pro",
        description="Creates a high-level overview and structure for study materials with optional web research",
        instruction="""You are an educational overview specialist with access to MCP tools for web research.

**Your Task:**
Analyze the provided study material and create a comprehensive high-level overview.

The firecrawl_search tool is

**Step 1: Assess the Input**
- If the user provides ONLY a topic name (e.g., "quantum computing" or "photosynthesis"), use firecrawl_search to gather context
- If the user provides detailed text or material, skip to Step 2

**Step 2: Use MCP Tools (if needed)**
When you need to search, use the firecrawl_search tool EXACTLY like this:
- Tool name: firecrawl_search
- Parameter: query (string)
- Example usage: Call firecrawl_search with query="quantum computing basics for students"
- Limit: 1-2 searches maximum

**Step 3: Create Overview**
Generate an overview with:

1. **Main Topic**: Central theme or subject
2. **Key Sections**: 3-5 main sections to cover
3. **Learning Objectives**: 3-5 specific, measurable objectives
4. **Difficulty Level**: beginner, intermediate, or advanced

**Output Format:**
# Main Topic
[Topic name]

## Key Sections
1. [Section 1]
2. [Section 2]
3. [Section 3]

## Learning Objectives
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

## Difficulty Level
[Beginner/Intermediate/Advanced]

**Important:**
- Use MCP tools (specifically firecrawl_search) ONLY when you have insufficient context
- When calling tools, use the EXACT tool names provided to you
- Keep learning objectives specific and actionable
- Do not mention in your output that you used search tools""",
        tools=tools,
        output_key="overview",
    )
