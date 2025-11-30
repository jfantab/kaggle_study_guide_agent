#!/bin/bash
# Deploy the study guide agent to Google Cloud

# Change to the script's directory (deployed_agent/)
cd "$(dirname "$0")" || exit 1

python3 cleanup.py study_guide_agent
adk deploy agent_engine --project=$PROJECT_ID --region=us-west1 study_guide_agent --agent_engine_config_file=study_guide_agent/.agent_engine_config.json