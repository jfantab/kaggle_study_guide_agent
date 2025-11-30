from .setup import setup_environment
from .agents import create_main_study_guide_agent

# Initialize environment and Vertex AI
setup_environment()

# Study Guide Agent: Sequential flow through all stages
# Note: Memory is configured via the Runner, not the Agent
# When using `adk web`, memory will be handled automatically
# For custom runners, configure memory_service on the Runner instance
root_agent = create_main_study_guide_agent()
