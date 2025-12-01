from google.adk.agents import Agent
from .schemas import StudyGuideOverview
from ...tools.firecrawl_function_tool import get_firecrawl_function_tools


def create_overview_agent():
    """Creates the overview agent for generating high-level study guide structure

    This agent analyzes provided study material to create learning objectives
    and study guide structure using a structured Pydantic schema.

    Uses Firecrawl FunctionTools which work in both local development and deployment.
    """

    # Use FunctionTools instead of MCP for deployment compatibility
    tools = get_firecrawl_function_tools()

    instruction_base = """You are an educational overview specialist.

**Your Task:**
Analyze the provided study material and create a comprehensive high-level overview.
"""

    instruction_tools = """
**Available Tools:**
You have access to Firecrawl tools for web research:
- firecrawl_search(query, limit): Search the web for relevant educational content
- firecrawl_scrape(url): Extract content from a specific URL
- Use these tools when helpful to validate or enhance the overview
"""

    instruction_output = """
**Output Structure:**
You must provide a structured response with:
- main_topic: Central theme or subject (string)
- key_sections: 3-5 main sections to cover (list of strings)
- learning_objectives: 3-5 specific, measurable objectives (list of strings)
- difficulty_level: One of "beginner", "intermediate", or "advanced" (string)

**Important:**
- Keep learning objectives specific and actionable
- Focus on the material provided by the user
- Create comprehensive objectives based on the content
- Output will be structured according to the StudyGuideOverview schema"""

    return Agent(
        name="OverviewAgent",
        model="gemini-2.5-pro",
        description="Creates a high-level overview and structure for study materials",
        instruction=instruction_base + instruction_tools + instruction_output,
        output_schema=StudyGuideOverview,
        tools=tools,
        output_key="overview",
    )
