# hotmart-mcp — Technical Specification
**Version 0.1 — April 2026**

> This document is the contract for the MCP server. It defines tools, parameters, return shapes,
> categories, and error contracts. All code and tests are derived from this spec — not the other way around.

---

## 1. Overview

`hotmart-mcp` is a Model Context Protocol (MCP) server that exposes the Hotmart API as tools for
LLM-powered agents. It uses the `hotmart-python` SDK (v1.1+) as its HTTP client — it does not
make HTTP calls directly.

**Primary dependency:** `hotmart-python` (AsyncHotmart)
**MCP framework:** FastMCP
**Python:** ≥ 3.11
**Transport:** stdio

---

## 2. Configuration

### 2.1 Environment variables (via pydantic-settings)

| Variable               | Required | Default | Description                |
|------------------------|----------|---------|----------------------------|
| `HOTMART_CLIENT_ID`    | yes      | —       | OAuth client ID            |
| `HOTMART_CLIENT_SECRET`| yes      | —       | OAuth client secret        |
| `HOTMART_BASIC`        | yes      | —       | Basic auth token           |
| `HOTMART_SANDBOX`      | no       | false   | Use sandbox environment    |

### 2.2 CLI arguments

| Argument      | Default     | Description                         |
|---------------|-------------|-------------------------------------|
| `--essential` | ✓ (default) | Read-only tools only                |
| `--write`     |             | Essential + mutation tools          |
| `--all`       |             | All tools (same as --write for now) |

### 2.3 Configuration guard clauses

The server must fail immediately (before any tool registration) if:
- `HOTMART_CLIENT_ID` is missing or empty → `ValidationError`
- `HOTMART_CLIENT_SECRET` is missing or empty → `ValidationError`
- `HOTMART_BASIC` is missing or empty → `ValidationError`

### 2.4 .env support

The server reads `.env` files in the working directory via pydantic-settings `env_file=".env"`.

---

## 3. Tool Categories

### 3.1 Modes

- **essential** — Read-only tools. Safe for any user/agent. Default mode.
- **write** — Essential + tools that mutate data (refunds, cancellations, coupon management).
- **all** — Every registered tool. Currently identical to `write`.

### 3.2 Filtering mechanism

All tools are registered first, then tools not belonging to the active mode are removed
via FastMCP's tool provider. This matches the pattern used in `metabase-mcp-python`.

---

## 4. Tool Definitions

### 4.1 Sales Tools

#### `get_sales_history` — essential

SDK: `await client.sales.history(**params)`

| Parameter            | Type         | Required | Description                     |
|----------------------|--------------|----------|---------------------------------|
| `product_id`         | int \| null  | no       | Filter by product ID            |
| `start_date`         | int \| null  | no       | Start date (epoch ms)           |
| `end_date`           | int \| null  | no       | End date (epoch ms)             |
| `sales_source`       | str \| null  | no       | Sales source identifier         |
| `transaction`        | str \| null  | no       | Filter by transaction code      |
| `buyer_name`         | str \| null  | no       | Filter by buyer name            |
| `buyer_email`        | str \| null  | no       | Filter by buyer email           |
| `transaction_status` | str \| null  | no       | Filter by status (e.g. APPROVED)|
| `payment_type`       | str \| null  | no       | Filter by payment method        |
| `offer_code`         | str \| null  | no       | Filter by offer code            |
| `commission_as`      | str \| null  | no       | Commission role filter          |
| `max_results`        | int \| null  | no       | Max items per page              |
| `page_token`         | str \| null  | no       | Pagination token                |

Returns: JSON `{"items": [...], "page_info": {"next_page_token": "..."}}`
Annotations: `readOnlyHint=True`

#### `get_sales_summary` — essential

SDK: `await client.sales.summary(**params)`

| Parameter            | Type         | Required | Description                     |
|----------------------|--------------|----------|---------------------------------|
| `product_id`         | int \| null  | no       | Filter by product ID            |
| `start_date`         | int \| null  | no       | Start date (epoch ms)           |
| `end_date`           | int \| null  | no       | End date (epoch ms)             |
| `sales_source`       | str \| null  | no       | Sales source identifier         |
| `affiliate_name`     | str \| null  | no       | Filter by affiliate name        |
| `payment_type`       | str \| null  | no       | Filter by payment method        |
| `offer_code`         | str \| null  | no       | Filter by offer code            |
| `transaction`        | str \| null  | no       | Filter by transaction code      |
| `transaction_status` | str \| null  | no       | Filter by status                |
| `max_results`        | int \| null  | no       | Max items per page              |
| `page_token`         | str \| null  | no       | Pagination token                |

Returns: JSON `{"items": [...], "page_info": {"next_page_token": "..."}}`
Annotations: `readOnlyHint=True`

#### `get_sales_participants` — essential

SDK: `await client.sales.participants(**params)`

| Parameter            | Type         | Required | Description                     |
|----------------------|--------------|----------|---------------------------------|
| `product_id`         | int \| null  | no       | Filter by product ID            |
| `start_date`         | int \| null  | no       | Start date (epoch ms)           |
| `end_date`           | int \| null  | no       | End date (epoch ms)             |
| `buyer_email`        | str \| null  | no       | Filter by buyer email           |
| `buyer_name`         | str \| null  | no       | Filter by buyer name            |
| `sales_source`       | str \| null  | no       | Sales source identifier         |
| `transaction`        | str \| null  | no       | Filter by transaction code      |
| `affiliate_name`     | str \| null  | no       | Filter by affiliate name        |
| `commission_as`      | str \| null  | no       | Commission role filter          |
| `transaction_status` | str \| null  | no       | Filter by status                |
| `max_results`        | int \| null  | no       | Max items per page              |
| `page_token`         | str \| null  | no       | Pagination token                |

Returns: JSON `{"items": [...], "page_info": {"next_page_token": "..."}}`
Annotations: `readOnlyHint=True`

#### `get_sales_commissions` — essential

SDK: `await client.sales.commissions(**params)`

| Parameter            | Type         | Required | Description                     |
|----------------------|--------------|----------|---------------------------------|
| `product_id`         | int \| null  | no       | Filter by product ID            |
| `start_date`         | int \| null  | no       | Start date (epoch ms)           |
| `end_date`           | int \| null  | no       | End date (epoch ms)             |
| `transaction`        | str \| null  | no       | Filter by transaction code      |
| `commission_as`      | str \| null  | no       | Commission role filter          |
| `transaction_status` | str \| null  | no       | Filter by status                |
| `max_results`        | int \| null  | no       | Max items per page              |
| `page_token`         | str \| null  | no       | Pagination token                |

Returns: JSON `{"items": [...], "page_info": {"next_page_token": "..."}}`
Annotations: `readOnlyHint=True`

#### `get_sales_price_details` — essential

SDK: `await client.sales.price_details(**params)`

| Parameter            | Type         | Required | Description                     |
|----------------------|--------------|----------|---------------------------------|
| `product_id`         | int \| null  | no       | Filter by product ID            |
| `start_date`         | int \| null  | no       | Start date (epoch ms)           |
| `end_date`           | int \| null  | no       | End date (epoch ms)             |
| `transaction`        | str \| null  | no       | Filter by transaction code      |
| `transaction_status` | str \| null  | no       | Filter by status                |
| `payment_type`       | str \| null  | no       | Filter by payment method        |
| `max_results`        | int \| null  | no       | Max items per page              |
| `page_token`         | str \| null  | no       | Pagination token                |

Returns: JSON `{"items": [...], "page_info": {"next_page_token": "..."}}`
Annotations: `readOnlyHint=True`

#### `refund_sale` — write

SDK: `await client.sales.refund(transaction_code)`

| Parameter          | Type | Required | Description            |
|--------------------|------|----------|------------------------|
| `transaction_code` | str  | yes      | Transaction to refund  |

Returns: JSON `{"status": "ok"}`
Annotations: `readOnlyHint=False, destructiveHint=True`

---

### 4.2 Subscription Tools

#### `list_subscriptions` — essential

SDK: `await client.subscriptions.list(**params)`

| Parameter               | Type              | Required | Description                       |
|-------------------------|-------------------|----------|-----------------------------------|
| `product_id`            | int \| null       | no       | Filter by product ID              |
| `plan_id`               | int \| null       | no       | Filter by plan ID                 |
| `accession_date`        | int \| null       | no       | Accession start date (epoch ms)   |
| `end_accession_date`    | int \| null       | no       | Accession end date (epoch ms)     |
| `status`                | str \| null       | no       | Filter by status                  |
| `subscriber_code`       | str \| null       | no       | Filter by subscriber code         |
| `subscriber_email`      | str \| null       | no       | Filter by subscriber email        |
| `transaction`           | str \| null       | no       | Filter by transaction code        |
| `trial`                 | bool \| null      | no       | Filter by trial status            |
| `cancelation_date`      | int \| null       | no       | Cancellation start date           |
| `end_cancelation_date`  | int \| null       | no       | Cancellation end date             |
| `date_next_charge`      | int \| null       | no       | Next charge start date            |
| `end_date_next_charge`  | int \| null       | no       | Next charge end date              |
| `max_results`           | int \| null       | no       | Max items per page                |
| `page_token`            | str \| null       | no       | Pagination token                  |

Returns: JSON `{"items": [...], "page_info": {"next_page_token": "..."}}`
Annotations: `readOnlyHint=True`

#### `get_subscription_summary` — essential

SDK: `await client.subscriptions.summary(**params)`

| Parameter            | Type         | Required | Description                     |
|----------------------|--------------|----------|---------------------------------|
| `product_id`         | int \| null  | no       | Filter by product ID            |
| `subscriber_code`    | str \| null  | no       | Filter by subscriber            |
| `accession_date`     | int \| null  | no       | Accession start date            |
| `end_accession_date` | int \| null  | no       | Accession end date              |
| `date_next_charge`   | int \| null  | no       | Next charge date filter         |
| `max_results`        | int \| null  | no       | Max items per page              |
| `page_token`         | str \| null  | no       | Pagination token                |

Returns: JSON `{"items": [...], "page_info": {"next_page_token": "..."}}`
Annotations: `readOnlyHint=True`

#### `get_subscription_purchases` — essential

SDK: `await client.subscriptions.purchases(subscriber_code)`

| Parameter         | Type | Required | Description            |
|-------------------|------|----------|------------------------|
| `subscriber_code` | str  | yes      | Subscriber identifier  |

Returns: JSON array of purchase objects
Annotations: `readOnlyHint=True`

#### `get_subscription_transactions` — essential

SDK: `await client.subscriptions.transactions(subscriber_code)`

| Parameter         | Type | Required | Description            |
|-------------------|------|----------|------------------------|
| `subscriber_code` | str  | yes      | Subscriber identifier  |

Returns: JSON array of transaction objects
Annotations: `readOnlyHint=True`

#### `cancel_subscriptions` — write

SDK: `await client.subscriptions.cancel(subscriber_code, send_mail=send_mail)`

| Parameter         | Type       | Required | Description                             |
|-------------------|------------|----------|-----------------------------------------|
| `subscriber_code` | list[str]  | yes      | List of subscriber codes                |
| `send_mail`       | bool       | no       | Send cancellation email (default: true) |

Returns: JSON with cancellation results
Annotations: `readOnlyHint=False, destructiveHint=True`

#### `reactivate_subscriptions` — write

SDK: `await client.subscriptions.reactivate(subscriber_code, charge=charge)`

| Parameter         | Type       | Required | Description                         |
|-------------------|------------|----------|-------------------------------------|
| `subscriber_code` | list[str]  | yes      | List of subscriber codes            |
| `charge`          | bool       | no       | Charge immediately (default: false) |

Returns: JSON with reactivation results
Annotations: `readOnlyHint=False`

#### `reactivate_subscription` — write

SDK: `await client.subscriptions.reactivate_single(subscriber_code, charge=charge)`

| Parameter         | Type | Required | Description                         |
|-------------------|------|----------|-------------------------------------|
| `subscriber_code` | str  | yes      | Subscriber code                     |
| `charge`          | bool | no       | Charge immediately (default: false) |

Returns: JSON with reactivation result
Annotations: `readOnlyHint=False`

#### `change_subscription_due_day` — write

SDK: `await client.subscriptions.change_due_day(subscriber_code, due_day)`

| Parameter         | Type | Required | Description            |
|-------------------|------|----------|------------------------|
| `subscriber_code` | str  | yes      | Subscriber code        |
| `due_day`         | int  | yes      | New billing day (1-28) |

Returns: JSON `{"status": "ok"}`
Annotations: `readOnlyHint=False`

---

### 4.3 Product Tools

#### `list_products` — essential

SDK: `await client.products.list(**params)`

| Parameter    | Type         | Required | Description                          |
|--------------|--------------|----------|--------------------------------------|
| `id`         | int \| null  | no       | Filter by product ID                 |
| `status`     | str \| null  | no       | Filter by status (ACTIVE, DRAFT...)  |
| `format`     | str \| null  | no       | Filter by format (ONLINE_COURSE...)  |
| `max_results`| int \| null  | no       | Max items per page                   |
| `page_token` | str \| null  | no       | Pagination token                     |

Returns: JSON `{"items": [...], "page_info": {"next_page_token": "..."}}`
Annotations: `readOnlyHint=True`

#### `get_product_offers` — essential

SDK: `await client.products.offers(ucode, **params)`

| Parameter    | Type         | Required | Description        |
|--------------|--------------|----------|--------------------|
| `ucode`      | str          | yes      | Product ucode      |
| `max_results`| int \| null  | no       | Max items per page |
| `page_token` | str \| null  | no       | Pagination token   |

Returns: JSON `{"items": [...], "page_info": {"next_page_token": "..."}}`
Annotations: `readOnlyHint=True`

#### `get_product_plans` — essential

SDK: `await client.products.plans(ucode, **params)`

| Parameter    | Type         | Required | Description        |
|--------------|--------------|----------|--------------------|
| `ucode`      | str          | yes      | Product ucode      |
| `max_results`| int \| null  | no       | Max items per page |
| `page_token` | str \| null  | no       | Pagination token   |

Returns: JSON `{"items": [...], "page_info": {"next_page_token": "..."}}`
Annotations: `readOnlyHint=True`

---

### 4.4 Coupon Tools

#### `list_coupons` — essential

SDK: `await client.coupons.list(product_id, **params)`

| Parameter    | Type         | Required | Description            |
|--------------|--------------|----------|------------------------|
| `product_id` | str          | yes      | Product ID             |
| `code`       | str \| null  | no       | Filter by coupon code  |
| `page_token` | str \| null  | no       | Pagination token       |

Returns: JSON `{"items": [...], "page_info": {"next_page_token": "..."}}`
Annotations: `readOnlyHint=True`

#### `create_coupon` — write

SDK: `await client.coupons.create(product_id, coupon_code, discount)`

| Parameter    | Type  | Required | Description         |
|--------------|-------|----------|---------------------|
| `product_id` | str   | yes      | Product ID          |
| `coupon_code`| str   | yes      | Coupon code         |
| `discount`   | float | yes      | Discount percentage |

Returns: JSON `{"status": "ok"}`
Annotations: `readOnlyHint=False`

#### `delete_coupon` — write

SDK: `await client.coupons.delete(coupon_id)`

| Parameter  | Type | Required | Description |
|------------|------|----------|-------------|
| `coupon_id`| str  | yes      | Coupon ID   |

Returns: JSON `{"status": "ok"}`
Annotations: `readOnlyHint=False, destructiveHint=True`

---

### 4.5 Club Tools

#### `get_club_modules` — essential

SDK: `await client.club.modules(subdomain, is_extra=is_extra)`

| Parameter  | Type          | Required | Description            |
|------------|---------------|----------|------------------------|
| `subdomain`| str           | yes      | Members area subdomain |
| `is_extra` | bool \| null  | no       | Filter extra modules   |

Returns: JSON array of module objects
Annotations: `readOnlyHint=True`

#### `get_club_pages` — essential

SDK: `await client.club.pages(subdomain, module_id)`

| Parameter  | Type | Required | Description            |
|------------|------|----------|------------------------|
| `subdomain`| str  | yes      | Members area subdomain |
| `module_id`| str  | yes      | Module identifier      |

Returns: JSON array of page objects
Annotations: `readOnlyHint=True`

#### `get_club_students` — essential

SDK: `await client.club.students(subdomain)`

| Parameter  | Type | Required | Description            |
|------------|------|----------|------------------------|
| `subdomain`| str  | yes      | Members area subdomain |

Returns: JSON array of student objects
Annotations: `readOnlyHint=True`

#### `get_club_student_progress` — essential

SDK: `await client.club.student_progress(subdomain, student_email=student_email)`

| Parameter       | Type         | Required | Description            |
|-----------------|--------------|----------|------------------------|
| `subdomain`     | str          | yes      | Members area subdomain |
| `student_email` | str \| null  | no       | Filter by email        |

Returns: JSON array of progress objects
Annotations: `readOnlyHint=True`

---

### 4.6 Event Tools

#### `get_event` — essential

SDK: `await client.events.get(event_id)`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `event_id`| str  | yes      | Event ID    |

Returns: JSON event object or null
Annotations: `readOnlyHint=True`

#### `get_event_tickets` — essential

SDK: `await client.events.tickets(product_id=product_id, **params)`

| Parameter    | Type         | Required | Description        |
|--------------|--------------|----------|--------------------|
| `product_id` | int          | yes      | Product ID         |
| `max_results`| int \| null  | no       | Max items per page |
| `page_token` | str \| null  | no       | Pagination token   |

Returns: JSON `{"items": [...], "page_info": {"next_page_token": "..."}}`
Annotations: `readOnlyHint=True`

---

### 4.7 Negotiation Tools

#### `create_negotiation` — write

SDK: `await client.negotiation.create(subscriber_code)`

| Parameter         | Type | Required | Description     |
|-------------------|------|----------|-----------------|
| `subscriber_code` | str  | yes      | Subscriber code |

Returns: JSON negotiation response or null
Annotations: `readOnlyHint=False`

---

## 5. Client Wrapper

### 5.1 Architecture

The `HotmartMCPClient` class wraps `AsyncHotmart` from the SDK:
- Initializes SDK with config from pydantic-settings
- Exposes async methods matching each tool
- Converts Pydantic models to dicts via `.model_dump()` (paginated) or model_validate + model_dump (lists)
- Returns plain Python dicts/lists — tools `json.dumps()` them

### 5.2 Paginated response shape

For SDK methods returning `PaginatedResponse[T]`:
```python
{
    "items": [item.model_dump() for item in page.items],
    "page_info": {"next_page_token": page.page_info.next_page_token} if page.page_info else None
}
```

For SDK methods returning `list[T]`:
```python
[item.model_dump() for item in items]
```

For SDK methods returning `None` (void actions):
```python
{"status": "ok"}
```

### 5.3 Context manager

```python
async with HotmartMCPClient(config) as client:
    ...  # SDK connection is cleaned up on exit
```

---

## 6. Error Handling

### 6.1 SDK exceptions mapped to JSON error responses

The SDK raises typed exceptions. The MCP server catches them and returns JSON errors:

| SDK Exception        | JSON error                                               |
|----------------------|----------------------------------------------------------|
| `AuthenticationError`| `{"error": "Authentication failed. Check credentials."}` |
| `NotFoundError`      | `{"error": "Resource not found.", "detail": str(e)}`     |
| `BadRequestError`    | `{"error": "Bad request.", "detail": str(e)}`            |
| `RateLimitError`     | `{"error": "Rate limit exceeded. Try again later."}`     |
| `InternalServerError`| `{"error": "Hotmart API error.", "detail": str(e)}`      |
| `HotmartError`       | `{"error": "Unexpected error.", "detail": str(e)}`       |

### 6.2 Centralized handler

A decorator or helper function in `exceptions.py` wraps all tool calls to avoid try/except boilerplate.

### 6.3 What the server must NOT do

- Never retry — the SDK handles retries internally
- Never manage rate limiting — the SDK handles it
- Never refresh tokens — the SDK handles it

---

## 7. Repository Structure

```
hotmart-mcp/
├── CLAUDE.md
├── SPEC.md                          # This document
├── README.md
├── LICENSE
├── pyproject.toml
├── src/
│   └── hotmart_mcp/
│       ├── __init__.py              # __version__
│       ├── __main__.py              # CLI: argparse --essential/--write/--all → main()
│       ├── server.py                # create_server(config, mode) → FastMCP
│       ├── config.py                # HotmartMCPConfig (pydantic-settings)
│       ├── client.py                # HotmartMCPClient wrapping AsyncHotmart
│       ├── exceptions.py            # handle_sdk_errors decorator
│       ├── validators.py            # parse_if_string, JsonParsed
│       └── tools/
│           ├── __init__.py          # ESSENTIAL_TOOLS, WRITE_TOOLS, register_all_tools()
│           ├── sales.py
│           ├── subscriptions.py
│           ├── products.py
│           ├── coupons.py
│           ├── club.py
│           ├── events.py
│           └── negotiation.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_config.py
    ├── test_client.py
    ├── test_server.py
    ├── test_main.py
    ├── test_validators.py
    └── tools/
        ├── __init__.py
        ├── conftest.py
        ├── test_sales.py
        ├── test_subscriptions.py
        ├── test_products.py
        ├── test_coupons.py
        ├── test_club.py
        ├── test_events.py
        ├── test_negotiation.py
        └── test_tools_init.py
```

---

## 8. Test Plan

### 8.1 Test pyramid

| Layer       | File                     | What it tests                         |
|-------------|--------------------------|---------------------------------------|
| Unit        | `test_config.py`         | Env var loading, validation, defaults |
| Unit        | `test_validators.py`     | JSON string parsing                   |
| Unit        | `test_client.py`         | Async wrapper, model_dump, kwargs     |
| Unit        | `test_server.py`         | Server creation, tool registration    |
| Unit        | `test_main.py`           | CLI argparse modes                    |
| Tool        | `tests/tools/test_*.py`  | Each tool via `mcp.call_tool()`       |
| Tool        | `test_tools_init.py`     | Category filtering                    |
| Integration | (marked)                 | Real API calls against sandbox        |

### 8.2 Required test cases — `test_config.py`

- `test_config_loads_from_env` — all 3 required vars set → config created
- `test_config_missing_client_id` → ValidationError
- `test_config_missing_client_secret` → ValidationError
- `test_config_missing_basic` → ValidationError
- `test_config_empty_client_id` → ValidationError
- `test_config_sandbox_default_false` — sandbox defaults to False
- `test_config_sandbox_from_env` — HOTMART_SANDBOX=true → sandbox=True

### 8.3 Required test cases — `test_validators.py`

- `test_parse_if_string_with_valid_json` — `'{"a": 1}'` → `{"a": 1}`
- `test_parse_if_string_with_invalid_json` — `'not json'` → `'not json'`
- `test_parse_if_string_with_dict` — `{"a": 1}` → `{"a": 1}` (passthrough)
- `test_parse_if_string_with_list` — `[1, 2]` → `[1, 2]` (passthrough)

### 8.4 Required test cases — `test_client.py`

- `test_client_initializes_async_hotmart` — SDK initialized with config
- `test_client_paginated_response_shape` — returns items + page_info
- `test_client_list_response_shape` — returns list of dicts
- `test_client_void_response_shape` — returns {"status": "ok"}
- `test_client_context_manager` — aclose called on exit
- `test_client_forwards_kwargs` — all params forwarded to SDK

### 8.5 Required test cases — `test_server.py`

- `test_create_server_returns_fastmcp` — FastMCP instance
- `test_server_has_tools_registered` — tools are present

### 8.6 Required test cases — `test_main.py`

- `test_main_default_essential_mode`
- `test_main_write_mode`
- `test_main_all_mode`

### 8.7 Required test cases — per tool module

For each tool in each module:
- `test_{tool_name}_calls_correct_sdk_method` — verify mock called with right args
- `test_{tool_name}_returns_valid_json` — output is parseable JSON
- `test_{tool_name}_handles_sdk_error` — SDK exception → JSON error response

### 8.8 Required test cases — `test_tools_init.py`

- `test_essential_mode_only_has_read_tools` — 19 tools
- `test_write_mode_has_all_tools` — 27 tools
- `test_all_mode_same_as_write` — 27 tools
- `test_essential_tools_are_subset_of_write`

---

## 9. Acceptance Criteria

The server is ready when:

- [ ] `hotmart-mcp --essential` starts and registers 19 tools
- [ ] `hotmart-mcp --write` starts and registers 27 tools
- [ ] All tools return valid JSON responses when called
- [ ] Error responses follow the format in section 6.1
- [ ] `pytest tests/` passes with ≥80% coverage
- [ ] `ruff check src tests` passes with no errors
- [ ] `mypy src` passes with no errors
- [ ] Can connect via Claude Code MCP config and call tools successfully
