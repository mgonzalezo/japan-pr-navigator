# Japan PR Navigator - MCP Server

## Project Overview

An MCP (Model Context Protocol) server that helps foreigners living in Japan navigate the Permanent Residence application process. It provides real-time access to official Immigration Services Agency (ISA) data and community insights from LinkedIn, delivered through natural language questions via a local LLM.

## Problem Statement

Foreign professionals in Japan face a fragmented, opaque PR application process. Official information is scattered across moj.go.jp (primarily in Japanese), practical tips live in LinkedIn posts and expat forums, and the 28-document checklist varies by applicant type (single vs. married, HSP vs. standard). No single tool combines official guidance with community-tested advice.

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    User's Machine                         │
│                                                          │
│  ┌─────────────┐    OpenAI-compat API    ┌────────────┐ │
│  │  LM Studio  │◄──────────────────────►│   Ollama    │ │
│  │  (Chat UI)  │                         │  (LLM Host) │ │
│  └──────┬──────┘                         └────────────┘ │
│         │ MCP Protocol (stdio)                           │
│         ▼                                                │
│  ┌──────────────────────────────────────┐                │
│  │     japan-pr-mcp-server (Python)     │                │
│  │                                      │                │
│  │  Tools:                              │                │
│  │  ├─ search_pr_requirements           │                │
│  │  ├─ check_hsp_points                 │                │
│  │  ├─ get_document_checklist           │                │
│  │  ├─ lookup_immigration_office        │                │
│  │  ├─ search_linkedin_insights         │                │
│  │  └─ get_phase_guidance               │                │
│  │                                      │                │
│  │  Resources:                          │                │
│  │  ├─ knowledge://documents/{id}       │                │
│  │  ├─ knowledge://phases/{phase}       │                │
│  │  ├─ knowledge://hsp/points-table     │                │
│  │  └─ knowledge://offices/{region}     │                │
│  │                                      │                │
│  │  Data Layer:                         │                │
│  │  ├─ knowledge/  (curated YAML/JSON)  │                │
│  │  ├─ scrapers/   (moj.go.jp fetcher)  │                │
│  │  └─ linkedin/   (feed integration)   │                │
│  └──────────────────────────────────────┘                │
└──────────────────────────────────────────────────────────┘
```

## Tech Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| MCP Framework | FastMCP (Python) | Lightweight, decorator-based, proven in production |
| LLM Runtime | Ollama | Resource-efficient, OpenAI-compatible API |
| Chat UI | LM Studio | Native MCP client support, polished UX |
| Web Scraping | httpx + BeautifulSoup | Async, lightweight, no browser overhead |
| LinkedIn | LinkedIn API / RSS feeds | Structured data access |
| Knowledge Base | YAML files | No database needed, git-versioned, community-editable |
| Language | Python 3.11+ | Matches FastMCP ecosystem |

## Key Design Decisions

1. **YAML knowledge base over vector DB**: The PR domain is bounded (~28 documents, ~4 phases, ~50 offices). Structured YAML is searchable, git-diffable, and requires zero infrastructure.

2. **FastMCP over TypeScript SDK**: The user has production FastMCP experience (carbon-kepler-mcp). Python ecosystem has better scraping libraries.

3. **Ollama over direct LM Studio inference**: Ollama runs headless, supports more model formats, and its API is the de facto standard for local LLM serving.

4. **Pre-curated data with periodic refresh over live scraping**: moj.go.jp changes infrequently. Ship curated data, refresh via a scraper script on demand. Avoids runtime failures from site changes.

## Project Structure

```
japan-pr-mcp-server/
├── CLAUDE.md
├── README.md
├── pyproject.toml
├── src/
│   └── japan_pr_mcp/
│       ├── __init__.py
│       ├── server.py              # FastMCP server entry point
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── requirements.py    # PR requirement lookups
│       │   ├── hsp_points.py      # HSP point calculator
│       │   ├── documents.py       # Document checklist tool
│       │   ├── offices.py         # Immigration office finder
│       │   ├── linkedin.py        # LinkedIn feed search
│       │   └── phases.py          # Phase-by-phase guidance
│       └── resources/
│           ├── __init__.py
│           └── knowledge.py       # MCP resource handlers
├── knowledge/
│   ├── documents.yaml             # 28-document master list
│   ├── phases.yaml                # 4 application phases
│   ├── hsp_points.yaml            # Point calculation tables
│   ├── offices.yaml               # Immigration offices by region
│   ├── tips.yaml                  # Community-sourced tips
│   └── faq.yaml                   # Common questions + answers
├── scrapers/
│   ├── moj_scraper.py             # moj.go.jp data refresh
│   └── linkedin_scraper.py        # LinkedIn feed collector
├── tests/
│   ├── test_tools.py
│   ├── test_resources.py
│   └── test_scrapers.py
├── scripts/
│   ├── setup.sh                   # One-command setup
│   └── refresh-data.sh            # Refresh knowledge base
├── .github/
│   └── workflows/
│       └── ci.yml                 # Lint + test on PR
└── docs/
    ├── CONTRIBUTING.md
    └── SETUP.md
```

## Development Commands

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Run server (stdio mode for LM Studio)
python -m japan_pr_mcp.server

# Run server (SSE mode for remote access)
python -m japan_pr_mcp.server --transport sse --port 8080

# Tests
pytest tests/ -v --cov=src/japan_pr_mcp --cov-report=term-missing

# Lint
ruff check src/ tests/
ruff format src/ tests/

# Refresh knowledge base from moj.go.jp
python -m scrapers.moj_scraper

# Type check
mypy src/
```

## MCP Tools Reference

| Tool | Description | Input |
|------|-------------|-------|
| `search_pr_requirements` | Search PR requirements by visa type, marital status | `visa_type`, `marital_status` |
| `check_hsp_points` | Calculate HSP points from user profile | `age`, `salary`, `education`, `experience`, `jlpt_level`, `university_ranking` |
| `get_document_checklist` | Get personalized document checklist | `applicant_type` (single/married/with_children) |
| `lookup_immigration_office` | Find nearest immigration office | `prefecture` or `city` |
| `search_linkedin_insights` | Search community tips and experiences | `query`, `hashtags` |
| `get_phase_guidance` | Detailed guidance for each application phase | `phase` (1-4) |

## MCP Resources Reference

| URI Pattern | Description |
|-------------|-------------|
| `knowledge://documents/{doc_id}` | Individual document details (bilingual) |
| `knowledge://phases/{phase_number}` | Phase walkthrough with tips |
| `knowledge://hsp/points-table` | Full HSP point calculation matrix |
| `knowledge://offices/{region}` | Immigration office details + hours |

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md). Key areas for community contribution:
- **knowledge/*.yaml**: Add tips, correct document requirements, update office info
- **scrapers/**: Improve data extraction from moj.go.jp
- **tools/**: Add new MCP tools (e.g., timeline estimator, cost calculator)
- **translations**: Add non-English, non-Japanese language support

## Supported LLM Models (Recommended)

| Model | Size | Best For |
|-------|------|----------|
| `llama3.1:8b` | ~4.7GB | Quick answers, low-resource machines |
| `mistral:7b` | ~4.1GB | Good multilingual (JP/EN) support |
| `qwen2.5:14b` | ~8.9GB | Best Japanese language understanding |
| `gemma2:9b` | ~5.4GB | Balanced performance and size |
