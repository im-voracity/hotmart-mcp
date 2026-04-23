from __future__ import annotations

import json
import logging
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any

from hotmart import (
    AuthenticationError,
    BadRequestError,
    HotmartError,
    InternalServerError,
    NotFoundError,
    RateLimitError,
)

_logger = logging.getLogger(__name__)


def handle_sdk_errors(fn: Callable[..., Coroutine[Any, Any, str]]) -> Callable[..., Coroutine[Any, Any, str]]:
    """Decorator that catches SDK exceptions and returns JSON error strings.

    See SPEC.md §6 for the error mapping contract.
    """

    @wraps(fn)
    async def wrapper(*args: Any, **kwargs: Any) -> str:
        try:
            return await fn(*args, **kwargs)
        except AuthenticationError as e:
            return json.dumps({"error": "Authentication failed. Check credentials.", "detail": str(e)})
        except NotFoundError as e:
            return json.dumps({"error": "Resource not found.", "detail": str(e)})
        except BadRequestError as e:
            return json.dumps({"error": "Bad request.", "detail": str(e)})
        except RateLimitError as e:
            error: dict[str, Any] = {"error": "Rate limit exceeded. Try again later."}
            if hasattr(e, "retry_after") and e.retry_after:
                error["retry_after_seconds"] = e.retry_after
            return json.dumps(error)
        except InternalServerError as e:
            return json.dumps({"error": "Hotmart API error.", "detail": str(e)})
        except HotmartError as e:
            return json.dumps({"error": "Unexpected error.", "detail": str(e)})
        except Exception as e:
            _logger.exception("Unhandled error in tool %s", fn.__name__)
            return json.dumps({"error": "Internal error.", "detail": str(e), "type": type(e).__name__})

    return wrapper
