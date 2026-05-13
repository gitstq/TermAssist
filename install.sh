#!/bin/bash
# Installation script for TermAssist

set -e

echo "🚀 Installing TermAssist..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Python 3.8+ is required (found $python_version)"
    exit 1
fi

echo "✅ Python version check passed"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --user

# Install package
echo "📦 Installing TermAssist..."
pip3 install -e . --user

# Create config directory
mkdir -p ~/.config/termassist

echo ""
echo "✅ Installation complete!"
echo ""
echo "Usage:"
echo "  termassist              # Start interactive mode"
echo "  termassist 'your query' # One-shot mode"
echo "  tai                     # Short alias"
echo ""
echo "Configuration file: ~/.config/termassist/config.yaml"
echo ""
echo "To configure LLM provider:"
echo "  1. Edit ~/.config/termassist/config.yaml"
echo "  2. Set provider to 'ollama', 'openai', or 'anthropic'"
echo "  3. Add your API key if using OpenAI or Anthropic"
