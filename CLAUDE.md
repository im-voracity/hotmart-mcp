# hotmart-mcp — Agent Instructions

## Language

- **All code, comments, docstrings, variable names, function names, class names, and commit messages must be in English**

---

## Project context

`hotmart-mcp` is an MCP (Model Context Protocol) server for the Hotmart API, built with FastMCP.

**Read `SPEC.md` before starting any task.** It is the contract of this project — every implementation
decision must be derived from it, not invented.

---

## Fixed architectural decisions

These decisions are final. Do not question or suggest alternatives without explicit context:

1. **HTTP client:** use `hotmart-python` (AsyncHotmart) as the full HTTP client. The server does not
   make HTTP calls directly. Retry, backoff, rate limiting, and token renewal are SDK responsibilities.

2. **Async native:** use `AsyncHotmart` directly — no `asyncio.to_thread()`, no sync bridges.

3. **Pagination:** tools return one page at a time with `page_token`. The LLM decides whether to
   fetch more pages.

4. **Tool filtering:** register all tools first, then remove those not in the active mode.
   Same pattern as `metabase-mcp-python`.

5. **No new Pydantic models:** the SDK already has comprehensive models. The MCP server passes
   through serialized dicts via `.model_dump()`.

---

## Code conventions

### Required in every file

```python
from __future__ import annotations  # always at the top
```

### Early returns — no else after return or raise

```python
# CORRECT
if value is None:
    return None
return process(value)
```

### Type hints required on all public functions

### Naming

- Tools: `snake_case` (`get_sales_history`)
- Classes: `PascalCase` (`HotmartMCPClient`)
- Constants: `UPPER_SNAKE_CASE` (`ESSENTIAL_TOOLS`)

### Quality tools

```bash
uv run ruff check src tests
uv run ruff format src tests
uv run mypy src
uv run pytest tests/ -v
uv run pytest tests/ --cov=hotmart_mcp --cov-report=term-missing
```

All must pass before any commit.

---

## Development workflow (TDD)

1. Read the relevant section of `SPEC.md`
2. Write the failing test (RED)
3. Write minimum code to pass (GREEN)
4. Refactor while keeping tests passing (REFACTOR)
5. Repeat

---

## Error handling

The SDK raises typed exceptions. The server handles them via a centralized decorator:

```python
# AuthenticationError → re-raise as JSON error (invalid credentials need human intervention)
# NotFoundError       → JSON error with detail
# Everything else     → JSON error with detail
```

**Never retry, backoff, or refresh tokens.** The SDK already does this.

---

## Tool implementation pattern

```python
def register_sales_tools(mcp: FastMCP, client: HotmartMCPClient) -> None:

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def get_sales_history(
        product_id: Annotated[int | None, Field(description="Filter by product ID")] = None,
        ...
    ) -> str:
        """Get sales history with buyer, product, and payment details."""
        result = await client.get_sales_history(product_id=product_id, ...)
        return json.dumps(result, indent=2)
```
