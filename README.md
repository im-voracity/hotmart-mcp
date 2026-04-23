# hotmart-mcp

MCP (Model Context Protocol) server for the Hotmart API. Exposes 27 Hotmart API tools for LLM-powered agents via [FastMCP](https://github.com/jlowin/fastmcp).

Built on top of [hotmart-python](https://github.com/im-voracity/hotmart-python) SDK.

## Features

- **27 tools** covering Sales, Subscriptions, Products, Coupons, Club (Members Area), Events, and Negotiation
- **Three operating modes**: `--essential` (19 read-only tools, default), `--write` (all 27 tools), `--all`
- **Async native** — uses `AsyncHotmart` directly, no sync bridges
- **Centralized error handling** — SDK exceptions mapped to structured JSON error responses
- **Pagination support** — tools return one page at a time with `page_token` for cursor-based navigation

## Installation

```bash
pip install hotmart-mcp
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv pip install hotmart-mcp
```

## Configuration

Set the required environment variables (or use a `.env` file):

| Variable | Required | Default | Description |
|---|---|---|---|
| `HOTMART_CLIENT_ID` | yes | — | OAuth client ID |
| `HOTMART_CLIENT_SECRET` | yes | — | OAuth client secret |
| `HOTMART_BASIC` | yes | — | Basic auth token |
| `HOTMART_SANDBOX` | no | `false` | Use sandbox environment |

## Usage

### Standalone

```bash
hotmart-mcp                # essential mode (read-only, default)
hotmart-mcp --write        # essential + mutation tools
hotmart-mcp --all          # all tools
```

### Claude Code

Add to your Claude Code MCP config (`~/.claude/claude_code_config.json`):

```json
{
  "mcpServers": {
    "hotmart": {
      "command": "hotmart-mcp",
      "args": ["--write"],
      "env": {
        "HOTMART_CLIENT_ID": "your-client-id",
        "HOTMART_CLIENT_SECRET": "your-client-secret",
        "HOTMART_BASIC": "your-basic-token"
      }
    }
  }
}
```

### Claude Desktop

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "hotmart": {
      "command": "uvx",
      "args": ["hotmart-mcp", "--write"],
      "env": {
        "HOTMART_CLIENT_ID": "your-client-id",
        "HOTMART_CLIENT_SECRET": "your-client-secret",
        "HOTMART_BASIC": "your-basic-token"
      }
    }
  }
}
```

## Available Tools

### Essential (read-only)

| Tool | Description |
|---|---|
| `get_sales_history` | Get sales history with buyer, product, and payment details |
| `get_sales_summary` | Get aggregated sales commission values |
| `get_sales_participants` | Get sales participant and user data |
| `get_sales_commissions` | Get commission breakdown by role per transaction |
| `get_sales_price_details` | Get price, fee, and VAT details per transaction |
| `list_subscriptions` | List subscriptions with filtering options |
| `get_subscription_summary` | Get subscription statistics summary |
| `get_subscription_purchases` | Get purchase history for a subscriber |
| `get_subscription_transactions` | Get transaction history for a subscriber |
| `list_products` | List products with filtering options |
| `get_product_offers` | Get offers and payment options for a product |
| `get_product_plans` | Get subscription plans for a product |
| `list_coupons` | List coupons for a product |
| `get_club_modules` | Get course modules for a members area |
| `get_club_pages` | Get pages within a course module |
| `get_club_students` | Get enrolled students for a members area |
| `get_club_student_progress` | Get student completion progress data |
| `get_event` | Get event details |
| `get_event_tickets` | Get event tickets for a product |

### Write (mutations)

| Tool | Description |
|---|---|
| `refund_sale` | Request a refund for a transaction |
| `cancel_subscriptions` | Cancel one or more subscriptions |
| `reactivate_subscriptions` | Reactivate subscriptions in bulk |
| `reactivate_subscription` | Reactivate a single subscription |
| `change_subscription_due_day` | Change the billing due day |
| `create_coupon` | Create a discount coupon |
| `delete_coupon` | Delete a coupon |
| `create_negotiation` | Create an installment negotiation |

## Development

```bash
git clone https://github.com/im-voracity/hotmart-mcp.git
cd hotmart-mcp
uv sync

# Quality checks
uv run ruff check src tests
uv run ruff format src tests
uv run mypy src
uv run pytest tests/ -v
uv run pytest tests/ --cov=hotmart_mcp --cov-report=term-missing
```

## License

Apache-2.0
