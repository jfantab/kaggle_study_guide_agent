#!/bin/bash
# Run adk web with increased timeouts for network stability

# Set timeout environment variables (5 minutes)
export GOOGLE_AUTH_TOKEN_URI_TIMEOUT=300
export GOOGLE_API_TIMEOUT=300
export GOOGLE_GENAI_TIMEOUT=300

# Increase Python's socket timeout
export PYTHONHTTPTIMEOUT=300

echo "🔧 Timeouts set:"
echo "  - Auth token timeout: 300s (5 min)"
echo "  - API timeout: 300s (5 min)"
echo "  - GenAI timeout: 300s (5 min)"
echo ""
echo "🚀 Starting adk web server..."
echo "   URL: http://localhost:8000"
echo ""

# Run adk web from the deployed_agent directory
cd "$(dirname "$0")" || exit 1
adk web --reload_agents 