from google.adk.agents import Agent
from .schemas import StudyGuideOverview
from ...tools.firecrawl_mcp import get_firecrawl_toolset


def create_overview_agent():
    """Creates the overview agent for generating high-level study guide structure

    This agent analyzes provided study material to create learning objectives
    and study guide structure using a structured Pydantic schema.
    Can use Firecrawl for web research to enrich the overview.
    """

    return Agent(
        name="OverviewAgent",
        model="gemini-2.5-pro",
        description="Creates a high-level overview and structure for study materials",
        instruction="""You are an educational overview specialist with web research capabilities.

**Your Task:**
Analyze the provided study material and create a comprehensive high-level overview.

**Available Tools:**
You have access to Firecrawl MCP tools for web research:
- firecrawl_search: Search the web for relevant educational content to enrich your understanding
- Use these tools when helpful to validate or enhance the overview

**Output Structure:**
You must provide a structured response with:
- main_topic: Central theme or subject (string)
- key_sections: 3-5 main sections to cover (list of strings)
- learning_objectives: 3-5 specific, measurable objectives (list of strings)
- difficulty_level: One of "beginner", "intermediate", or "advanced" (string)

**Important:**
- Keep learning objectives specific and actionable
- Focus on the material provided by the user
- Optionally use firecrawl_search to enrich your understanding when beneficial
- Create comprehensive objectives based on the content
- Output will be structured according to the StudyGuideOverview schema""",
        output_schema=StudyGuideOverview,
        tools=[get_firecrawl_toolset()],
        output_key="overview",
    )
