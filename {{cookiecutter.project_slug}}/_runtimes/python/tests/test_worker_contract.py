import json
import os
import subprocess
import sys
from pathlib import Path

SRC = str(Path(__file__).resolve().parent.parent / "src")


def run_worker(requests):
    payload = "".join(json.dumps(r) + "\n" for r in requests)
    env = {**os.environ, "PYTHONPATH": SRC}
    proc = subprocess.run(
        [sys.executable, "-m", "{{ cookiecutter.project_slug|replace('-', '_') }}.worker"],
        input=payload,
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
        env=env,
    )
    return [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]


def test_status_returns_ok():
    responses = run_worker([{"jsonrpc": "2.0", "id": 1, "method": "{{ cookiecutter.project_slug }}.status", "params": {}}])
    assert len(responses) == 1
    assert responses[0]["id"] == 1
    assert responses[0]["result"]["ok"] is True
    assert responses[0]["result"]["runtime"] == "python"


def test_unknown_method_errors():
    responses = run_worker([{"jsonrpc": "2.0", "id": 2, "method": "{{ cookiecutter.project_slug }}.nope"}])
    assert responses[0]["error"]["code"] == -32601


def test_notification_has_no_response():
    responses = run_worker([{"jsonrpc": "2.0", "method": "{{ cookiecutter.project_slug }}.status"}])
    assert responses == []
