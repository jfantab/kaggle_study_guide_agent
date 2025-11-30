from .setup import setup_environment
from .agents import create_main_study_guide_agent

# Initialize environment and Vertex AI
setup_environment()

# Study Guide Agent: Sequential flow through all stages
root_agent = create_main_study_guide_agent()
