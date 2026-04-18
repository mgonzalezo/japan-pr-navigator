#!/usr/bin/env bash
set -euo pipefail

echo "=== Japan PR Navigator - Setup ==="

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
REQUIRED="3.11"
if [ "$(printf '%s\n' "$REQUIRED" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED" ]; then
    echo "ERROR: Python >= 3.11 required (found $PYTHON_VERSION)"
    exit 1
fi
echo "[OK] Python $PYTHON_VERSION"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi
echo "[OK] Virtual environment"

# Activate and install
source .venv/bin/activate
echo "Installing dependencies..."
pip install -q -e ".[dev]"
echo "[OK] Dependencies installed"

# Validate knowledge base
echo "Validating knowledge base..."
python3 -c "
from japan_pr_mcp.knowledge_base import KnowledgeBase
from pathlib import Path
kb = KnowledgeBase.load(Path('knowledge'))
docs = kb.get_documents()
phases = kb.get_phases()
offices = kb.get_offices()
print(f'  Documents: {len(docs)}')
print(f'  Phases: {len(phases)}')
print(f'  Offices: {len(offices)}')
print(f'  Tips: {len(kb.get_tips())}')
print(f'  FAQ: {len(kb.get_faq())}')
"
echo "[OK] Knowledge base valid"

# Run tests
echo "Running tests..."
python3 -m pytest tests/ -q --tb=short
echo ""
echo "=== Setup complete ==="
echo ""
echo "Next steps:"
echo "  1. Install Ollama: https://ollama.ai"
echo "  2. Pull a model: ollama pull qwen2.5:14b"
echo "  3. Configure your MCP client (see README.md)"
echo "  4. Start asking questions!"
