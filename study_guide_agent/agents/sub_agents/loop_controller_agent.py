from google.adk.agents import Agent
from google.adk.tools import exit_loop


def create_loop_controller_agent():
    """Creates the agent that manages loop iteration and exit conditions

    This agent decides whether to continue processing more objectives or exit the loop.
    It uses the exit_loop() tool to signal completion.
    """
    return Agent(
        name="LoopControllerAgent",
        model="gemini-2.5-pro",
        description="Manages iteration through learning objectives and controls loop exit",
        instruction="""You are the loop controller. Your job is to track progress and call exit_loop ONLY when ALL objectives are complete.

COUNTING LOGIC:
1. Look at {overview} - count how many "Learning Objectives" are listed (look for numbered list under "## Learning Objectives")
2. Look at {section_content} - this accumulates ALL completed sections from previous iterations
3. Count how many complete sections are in {section_content} (count ## headers that correspond to objectives)
4. Compare: completed_sections vs total_objectives

DECISION RULES:
- If completed_sections < total_objectives: OUTPUT NOTHING
- If completed_sections >= total_objectives: Call exit_loop() tool

CRITICAL: WHEN CONTINUING THE LOOP, OUTPUT ABSOLUTELY NOTHING.
- Do not write any words at all
- Do not write punctuation
- Do not write empty strings
- Just output nothing - end your turn immediately without any text
- Your response must be completely empty (zero characters)

When all objectives are complete: Call exit_loop() tool only (no text).

DO NOT write anything ever except calling exit_loop when done.

IMPORTANT: The loop will run multiple times. Each time, {section_content} will contain MORE sections than before. Only exit when you see ALL objectives completed in {section_content}.
""",
        tools=[exit_loop],
        output_key="loop_status",
    )
