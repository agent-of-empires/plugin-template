# {{ cookiecutter.plugin_name }}

{{ cookiecutter.description }}

An [Agent of Empires](https://github.com/agent-of-empires/agent-of-empires)
plugin. It contributes a `status` command, one setting, and a `pane` UI slot,
backed by a worker that speaks JSON-RPC 2.0 over newline-delimited JSON on stdio.

## Install into Agent of Empires

```bash
# from a local checkout
aoe plugin install ./{{ cookiecutter.project_slug }}

# or from GitHub once published
aoe plugin install gh:your-org/{{ cookiecutter.project_slug }}
```

The host runs the manifest's `[[runtime.build]]` steps at install time and then
launches the plugin-relative worker entrypoint under `.aoe-build/`. Manage the
plugin from the TUI, the web dashboard, or `aoe plugin {enable,disable,update}`.

## Layout

```
aoe-plugin.toml        the manifest (commands, settings, ui slots, runtime)
{% if cookiecutter.runtime == "python" -%}
pyproject.toml         build + dev tooling (hatchling, ruff, mypy, pytest)
src/{{ cookiecutter.project_slug|replace('-', '_') }}/
  worker.py            the JSON-RPC worker loop
  rpc.py               response builders
tests/                 worker-contract and framing tests
{% elif cookiecutter.runtime == "node" -%}
package.json           build + dev tooling (tsc, eslint, vitest)
tsconfig.json
src/
  index.ts             the JSON-RPC worker loop
  rpc.ts               response builders
scripts/
  write-aoe-wrapper.mjs generates the plugin-relative launcher
test/                  worker-contract and framing tests
{% elif cookiecutter.runtime == "rust" -%}
Cargo.toml             crate + dev tooling
src/
  main.rs              the JSON-RPC worker loop
  rpc.rs               response builders
tests/                 worker-contract test
{% endif -%}
```

## Develop

{% if cookiecutter.runtime == "python" -%}
This plugin uses [uv](https://docs.astral.sh/uv/).

```bash
uv sync                       # install deps into a local venv
uv run ruff check .           # lint
uv run ruff format --check .  # format check
uv run mypy src               # type-check
uv run pytest                 # test
```

Drive the worker by hand (it reads one JSON-RPC request per line on stdin):

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"{{ cookiecutter.project_slug }}.status","params":{}}' \
  | uv run {{ cookiecutter.project_slug }}-worker
```
{% elif cookiecutter.runtime == "node" -%}
```bash
npm ci          # install deps
npm run lint    # eslint
npm run build   # compile TypeScript to dist/
npm test        # vitest
```

Drive the worker by hand (it reads one JSON-RPC request per line on stdin):

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"{{ cookiecutter.project_slug }}.status","params":{}}' \
  | node dist/index.js
```
{% elif cookiecutter.runtime == "rust" -%}
```bash
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
cargo build --release
```

Drive the worker by hand (it reads one JSON-RPC request per line on stdin):

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"{{ cookiecutter.project_slug }}.status","params":{}}' \
  | cargo run
```
{% endif -%}

## Worker protocol

The host spawns the worker and exchanges newline-delimited JSON-RPC 2.0 messages
over stdio. The worker answers a request whose method ends in `.status` and exits
cleanly when stdin reaches EOF. A request:

```json
{"jsonrpc": "2.0", "id": 1, "method": "{{ cookiecutter.project_slug }}.status", "params": {}}
```

A response:

```json
{"jsonrpc": "2.0", "id": 1, "result": {"ok": true, "runtime": "{{ cookiecutter.runtime }}", "message": "..."}}
```

Unknown methods return a JSON-RPC error with code `-32601`. See the
[plugin authoring guide](https://agent-of-empires.com/docs/development/writing-plugins/)
and the [plugin API reference](https://agent-of-empires.com/docs/api/plugin-api/).

## Release

Push a `v{{ cookiecutter.version }}`-style tag to run the release workflow: it
runs checks, generates the changelog from conventional commits, and publishes a
GitHub Release with a source archive and `sha256`. To get listed in the Agent of
Empires featured index, see the authoring guide's publishing section.

## License

MIT
