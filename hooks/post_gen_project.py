"""Post-generation hook: promote the chosen runtime payload to the project root.

Cookiecutter renders every file in the template (including the runtimes the
author did not choose) and only then runs this hook from inside the generated
project directory. This hook:

  1. appends the selected runtime's gitignore fragment to the root .gitignore,
  2. moves the selected `_runtimes/<runtime>/` contents up to the project root,
  3. deletes the entire `_runtimes/` staging directory.

It is deterministic and offline: it never installs dependencies or touches the
network. Building the worker happens later, when Agent of Empires installs the
plugin (via the manifest's [[runtime.build]] steps) or when the author runs the
language-specific dev commands.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

RUNTIME = "{{ cookiecutter.runtime }}"
VALID_RUNTIMES = {"python", "node", "rust"}


def append_gitignore_fragment(project_root: Path, selected_dir: Path) -> None:
    fragment = selected_dir / "gitignore.fragment"
    if not fragment.exists():
        return
    gitignore = project_root / ".gitignore"
    with gitignore.open("a", encoding="utf-8") as out:
        out.write("\n")
        out.write(fragment.read_text(encoding="utf-8").rstrip())
        out.write("\n")
    fragment.unlink()


def promote_runtime_payload(project_root: Path, selected_dir: Path) -> None:
    for child in selected_dir.iterdir():
        target = project_root / child.name
        if target.exists():
            sys.exit(f"Refusing to overwrite existing path while promoting runtime payload: {target}")
        shutil.move(str(child), str(target))


def main() -> None:
    project_root = Path.cwd()

    if RUNTIME not in VALID_RUNTIMES:
        sys.exit(f"Invalid runtime {RUNTIME!r}; expected one of {sorted(VALID_RUNTIMES)}")

    runtimes_dir = project_root / "_runtimes"
    selected_dir = runtimes_dir / RUNTIME
    if not selected_dir.exists():
        sys.exit(f"Missing runtime payload: {selected_dir}")

    append_gitignore_fragment(project_root, selected_dir)
    promote_runtime_payload(project_root, selected_dir)
    shutil.rmtree(runtimes_dir)

    print(f"Generated an Agent of Empires plugin using the {RUNTIME} runtime.")
    print("Next steps are in the generated README.md.")


if __name__ == "__main__":
    main()
