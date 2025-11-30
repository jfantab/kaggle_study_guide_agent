from google.adk.agents import Agent


def create_assembler_agent():
    """Creates the agent that assembles all completed sections into final study guide

    This agent takes all the individually processed sections and combines them
    into a cohesive study guide with proper structure and table of contents.
    """
    return Agent(
        name="AssemblerAgent",
        model="gemini-2.5-flash-lite",
        description="Assembles all completed sections into a cohesive study guide",
        instruction="""You are assembling the final study guide from the loop processing results.

Based on this overview:
{overview}

And the processing that has been completed through the loop:
{section_content}
{loop_status}

Your tasks:
1. Create a comprehensive study guide document
2. Add a table of contents listing all major sections
3. Ensure proper markdown formatting and flow
4. Structure the content logically based on the learning objectives

Output a complete study guide in this format:

# [Topic] Study Guide

## Table of Contents
[Generate numbered list of all main sections]

[Main content organized by sections]

The guide should be cohesive, well-organized, and ready for educational use.
""",
        output_key="elaborated_guide",
    )
