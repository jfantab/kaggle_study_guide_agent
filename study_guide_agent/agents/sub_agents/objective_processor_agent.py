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

Given this overview: {overview}

Based on current progress, identify the next unprocessed objective and create a study guide section for it.

Include:
- Clear explanation of the objective
- Key concepts and terminology
- Real-world examples and applications
- Practice questions or exercises (if applicable)

OUTPUT FORMAT (MANDATORY):
- Start IMMEDIATELY with markdown content (no preamble)
- Format as well-structured markdown with headers
- NO conversational text: no greetings, no 'Here is...', no 'I hope this helps', no 'Let me...', no 'I will...'
- NO closing remarks: no 'Happy learning', 'Thank you', 'Good luck', 'Take care', 'Goodbye', 'See you', etc.
- NO praise or encouragement: no 'Excellent', 'Wonderful', 'Great job', etc.
- NO meta-commentary about the guide or process
- Output ONLY: [## Title\n\nContent...]

Focus on depth and clarity in the educational content itself.
""",
        output_key="section_content",
    )
