from google.adk.agents import Agent


def create_objective_processor_agent():
    """Creates the agent that processes ONE learning objective at a time

    This agent reads the current index from state, processes the corresponding
    learning objective, and appends the completed section to state.
    """
    return Agent(
        name="ObjectiveProcessorAgent",
        model="gemini-2.5-pro",
        description="Processes a single learning objective from the overview",
        instruction="""You are a detailed educational content creator processing one learning objective at a time.

Given this overview:
{overview}

You need to process the learning objectives one by one. Based on the current progress in the state, identify which objective to process next and create a comprehensive study guide section for it.

Your section should include:
- Clear explanation of the specific objective
- Key concepts needed to achieve it
- Important definitions and terminology
- Real-world examples and applications
- Practice questions or exercises (if applicable)

Format your output as a well-structured markdown section with appropriate headers.

Make the content engaging, educational, and self-contained. Focus on depth and clarity.
""",
        output_key="section_content",
    )
