from google.adk.agents import Agent
from google.adk.tools import FunctionTool


def exit_loop():
    """Signal loop completion - all objectives have been processed

    This function MUST be called when all learning objectives have been
    successfully processed and we're ready to move to the assembly stage.
    """
    return {"status": "done", "message": "All learning objectives have been processed"}


def create_loop_controller_agent():
    """Creates the agent that manages loop iteration and exit conditions

    This agent decides whether to continue processing more objectives or exit the loop.
    It uses the exit_loop() tool to signal completion.
    """
    return Agent(
        name="LoopControllerAgent",
        model="gemini-2.5-flash-lite",
        description="Manages iteration through learning objectives and controls loop exit",
        instruction="""You are the loop controller. Your ONLY job is to count completed sections and call the exit_loop tool when done.

Count the learning objectives in the overview: {overview}

Count how many sections have been completed by looking at the section_content output.

IMPORTANT RULES:
- If the number of completed sections equals the total number of learning objectives: YOU MUST call the exit_loop() tool immediately. Do NOT write any text - just call the tool.
- If more sections remain: Simply acknowledge that processing should continue.

DO NOT write summaries, reviews, or additional content. Your sole purpose is to call exit_loop() when all objectives are processed.
""",
        tools=[FunctionTool(exit_loop)],
        output_key="loop_status",
    )
