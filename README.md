# Agent of Empires plugin template

The official [cookiecutter](https://cookiecutter.readthedocs.io/) starter for
[Agent of Empires](https://github.com/agent-of-empires/agent-of-empires)
plugins. It scaffolds a complete, installable plugin with a valid
`aoe-plugin.toml` manifest, a working JSON-RPC worker, tests, and CI in your
choice of **Python**, **Node** (TypeScript), or **Rust**.

## Generate a plugin

```bash
# install cookiecutter once (any of these works)
pipx install cookiecutter        # or: uv tool install cookiecutter / pip install cookiecutter

cookiecutter gh:agent-of-empires/plugin-template
```

You will be prompted for the plugin name, id, description, and a `runtime`
(`python`, `node`, or `rust`). Everything else is derived. The generated
project contains only the runtime you picked.

Non-interactive (handy for scripts and CI):

```bash
cookiecutter gh:agent-of-empires/plugin-template --no-input \
  plugin_name="My Plugin" runtime=python
```

## What you get

Every generated plugin shares the same Agent of Empires scaffolding:

- `aoe-plugin.toml` -- the plugin manifest (api_version 6), pre-filled with one
  command, one setting, one UI slot, and the `[runtime]` block for your
  language. See the [plugin API reference](https://agent-of-empires.com/docs/api/plugin-api/).
- a worker that speaks JSON-RPC 2.0 over newline-delimited JSON on stdio, with a
  `status` command and clean shutdown on EOF,
- language-native build, lint, type-check, and test tooling,
- GitHub Actions for checks, PR-title linting, and tagged releases,
- `.pre-commit-config.yaml`, `.editorconfig`, `cliff.toml`, and a CodeRabbit config.

The runtime command is always **plugin-relative** (it lives under `.aoe-build/`),
so the Agent of Empires daemon never depends on your shell `PATH` to launch the
worker. See the generated `README.md` for the per-language layout and dev loop.

## Runtimes

| Runtime | Build | Worker entrypoint |
| ------- | ----- | ----------------- |
| python  | `python3 -m venv` + `pip install .` | `.aoe-build/venv/bin/<slug>-worker` |
| node    | `npm ci` + `npm run build` + wrapper | `.aoe-build/node/bin/<slug>-worker` |
| rust    | `cargo build --release` | `.aoe-build/cargo-target/release/<slug>-worker` |

Python is modeled on the production
[GitHub plugin](https://github.com/agent-of-empires/plugin-github). Node and
Rust are minimal but fully working starters: they build, pass their tests, and
satisfy the same JSON-RPC worker contract. They are not full reference plugins.

## Contributing

`hooks/post_gen_project.py` promotes the selected `_runtimes/<runtime>/` payload
to the project root after generation. `.github/workflows/test-template.yml`
generates and builds all three runtimes on every push, which is what keeps the
unproven Node and Rust payloads honest. Run it locally before opening a PR:

```bash
cookiecutter . --no-input -o /tmp/aoe-out runtime=python
```

## License

MIT
