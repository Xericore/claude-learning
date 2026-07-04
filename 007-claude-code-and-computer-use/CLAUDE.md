# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A Python package implementing document-related tools (conversion/processing), exposed through an MCP (Model Context Protocol) server so they can be used by AI assistants.

## Setup & Commands

```bash
# Create a virtual env and activate it
uv venv
source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1

# Install the package in development mode
uv pip install -e .

# Start the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test file / test
uv run pytest tests/test_document.py
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx
```

This project uses `uv` for environment and dependency management (see `pyproject.toml` / `uv.lock`), not pip/venv directly.

## Architecture

- `main.py` — entry point. Creates a `FastMCP("docs")` server instance and registers tool functions onto it via `mcp.tool()(function)`. Running `main.py` starts the MCP server (`mcp.run()`).
- `tools/` — plain Python functions implementing the actual tool logic (e.g. `tools/math.py`, `tools/document.py`). These are framework-agnostic functions; they only become MCP tools once registered in `main.py`. **When adding a new tool, define the function in `tools/`, then explicitly register it in `main.py` — it is not picked up automatically.**
- `tests/` — pytest tests for the functions in `tools/`, plus `tests/fixtures/` containing sample binary documents (`.docx`, `.pdf`) used as test input.

## Defining MCP Tools

Tools are plain Python functions registered with the MCP server via:

```python
mcp.tool()(my_function)
```

Tool docstrings double as the tool description shown to the AI assistant calling it, so they should:

- Begin with a one-line summary
- Provide a detailed explanation of functionality
- Explain when to use (and not use) the tool
- Include usage examples with expected input/output

Parameters should use pydantic's `Field` for descriptions, since these descriptions are surfaced to the calling assistant:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does")
) -> ReturnType:
    """Comprehensive docstring here"""
    # Implementation
```

See `tools/math.py`'s `add` function for a worked example of this docstring/`Field` convention, and `main.py` for how it's wired up as a registered tool.
