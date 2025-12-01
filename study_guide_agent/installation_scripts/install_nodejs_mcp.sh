#!/bin/bash
set -e

echo "Installing Node.js and npm for Firecrawl MCP server support..."

# Install Node.js 20.x LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Verify installation
echo "Verifying Node.js installation..."
node --version
npm --version
npx --version

echo "Node.js and npx installed successfully for Firecrawl MCP server"
