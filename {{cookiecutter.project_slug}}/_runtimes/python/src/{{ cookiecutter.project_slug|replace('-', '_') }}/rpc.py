"""JSON-RPC 2.0 response builders.

A typed ``MethodNotFoundError`` becomes ``-32601``; anything else is the
internal-error code ``-32603``.
"""

from __future__ import annotations

from typing import Any

ERR_METHOD_NOT_FOUND = -32601
ERR_INTERNAL = -32603


class MethodNotFoundError(LookupError):
    """Raised when the worker has no handler for a requested method."""


def result_response(msg_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": msg_id, "result": result}


def error_response(msg_id: Any, exc: BaseException) -> dict[str, Any]:
    if isinstance(exc, LookupError):
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {"code": ERR_METHOD_NOT_FOUND, "message": f"unknown method {exc!s}"},
        }
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": ERR_INTERNAL, "message": str(exc)},
    }
