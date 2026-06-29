// Generate a plugin-relative launcher under .aoe-build/node/bin that pins the
// build-time node binary, so Agent of Empires can launch the worker without the
// daemon's PATH deciding which node (or whether any) is found. Run as the last
// [[runtime.build]] step in aoe-plugin.toml.

import { chmodSync, mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

function shQuote(value) {
  return `'${value.replaceAll("'", `'\\''`)}'`;
}

const root = process.cwd();
const node = process.execPath;
const entrypoint = resolve(root, "dist/index.js");
const out = resolve(root, ".aoe-build/node/bin/{{ cookiecutter.project_slug }}-worker");

mkdirSync(dirname(out), { recursive: true });
writeFileSync(out, `#!/bin/sh\nexec ${shQuote(node)} ${shQuote(entrypoint)} "$@"\n`);
chmodSync(out, 0o755);

console.log(`wrote ${out}`);
