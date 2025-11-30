from google.adk.agents import SequentialAgent, LoopAgent
from .sub_agents.overview_agent import create_overview_agent
from .sub_agents.objective_processor_agent import create_objective_processor_agent
from .sub_agents.loop_controller_agent import create_loop_controller_agent
from .sub_agents.assembler_agent import create_assembler_agent
from .sub_agents.judge_agent import create_judge_agent


def create_main_study_guide_agent():
    # Stage 1: Overview Agent - Creates high-level structure with Pydantic schema
    overview_agent = create_overview_agent()

    # Stage 2: Elaboration Loop - Processes learning objectives iteratively
    # The loop contains two sub-agents that work together:
    #   - ObjectiveProcessorAgent: Processes one objective at a time
    #   - LoopControllerAgent: Manages iteration and exit condition
    elaboration_loop = LoopAgent(
        name="ElaborationLoop",
        description="Iteratively processes each learning objective from the overview",
        sub_agents=[
            create_objective_processor_agent(),
            create_loop_controller_agent(),
        ],
        max_iterations=5,  # Safety limit to prevent infinite loops
    )

    # Stage 3: Assembler Agent - Combines all completed sections
    assembler_agent = create_assembler_agent()

    # Stage 4: Final Judge - Adds final polish and quality seal
    judge_agent = create_judge_agent()

    return SequentialAgent(
        name="study_guide_agent",
        description="Creates comprehensive study guides with detailed content using iterative processing",
        sub_agents=[
            overview_agent,
            elaboration_loop,
            assembler_agent,
            judge_agent,
        ],
    )
