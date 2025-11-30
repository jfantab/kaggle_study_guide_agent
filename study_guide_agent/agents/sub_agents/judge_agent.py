from google.adk.agents import Agent


def create_judge_agent():
    """Creates the judge agent for final quality assessment"""
    return Agent(
        name="JudgeAgent",
        model="gemini-2.5-flash-lite",
        description="Makes final quality assessment and adds finishing touches",
        instruction="""You are the final educational quality judge.

    Review this finalized study guide: {elaborated_guide}

    Your tasks:
    1. Add a brief introduction welcoming the student
    2. Verify all sections are complete and well-organized
    3. Add study tips or recommended approach at the end
    4. Ensure proper formatting and readability

    Present the final, polished study guide ready for students to use.
    Include your quality seal at the end: "✅ Quality Verified - Ready for Study" """,
    )
