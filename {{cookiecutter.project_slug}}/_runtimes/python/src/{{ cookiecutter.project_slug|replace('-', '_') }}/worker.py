"""Agent of Empires worker: JSON-RPC 2.0 over newline-delimited JSON on stdio.

The host spawns this process, sends one JSON-RPC request per line on stdin, and
reads one response per line on stdout. The worker exits cleanly on EOF.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from {{ cookiecutter.project_slug|replace('-', '_') }}.rpc import MethodNotFoundError, error_response, result_response

RUNTIME = "python"


def handle(method: str, _params: dict[str, Any]) -> dict[str, Any]:
    # The host maps a command id to a method; dispatch on the trailing segment so
    # the worker is robust to the host's exact method prefix. A real handler reads
    # `_params` for the request arguments.
    command = method.rsplit(".", 1)[-1]
    if command == "status":
        return {"ok": True, "runtime": RUNTIME, "message": "{{ cookiecutter.plugin_name }} worker is running"}
    raise MethodNotFoundError(method)


def process_line(line: str) -> dict[str, Any] | None:
    try:
        request = json.loads(line)
    except json.JSONDecodeError:
        return None
    msg_id = request.get("id")
    if msg_id is None:
        return None  # a notification: no response
    try:
        result = handle(request.get("method", ""), request.get("params") or {})
    except Exception as exc:  # noqa: BLE001 - any handler failure becomes an error response
        return error_response(msg_id, exc)
    return result_response(msg_id, result)


def main() -> None:
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        response = process_line(line)
        if response is None:
            continue
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
