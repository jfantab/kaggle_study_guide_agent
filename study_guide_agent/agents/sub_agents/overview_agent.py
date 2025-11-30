from google.adk.agents import Agent


def create_overview_agent():
    """Creates the overview agent for generating high-level study guide structure"""
    return Agent(
        name="OverviewAgent",
        model="gemini-2.5-flash-lite",
        description="Creates a high-level overview and structure for study materials",
        instruction="""You are an educational overview specialist.

    Analyze the provided study material and create a high-level overview that includes:
    1. **Main Topic**: Identify the central theme or subject
    2. **Key Sections**: List 3-5 main sections that should be covered
    3. **Learning Objectives**: Define what a student should understand after studying this material (list 3-5 specific objectives)
    4. **Difficulty Level**: Assess the complexity (beginner, intermediate, or advanced)

    Output your response in a clear, structured markdown format.""",
        output_key="overview",
    )
