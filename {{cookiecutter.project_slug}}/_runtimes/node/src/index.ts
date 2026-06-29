// Agent of Empires worker: JSON-RPC 2.0 over newline-delimited JSON on stdio.
//
// The host spawns this process, sends one JSON-RPC request per line on stdin,
// and reads one response per line on stdout. The worker exits cleanly on EOF.

import * as readline from "node:readline";
import { fileURLToPath } from "node:url";
import { MethodNotFoundError, RpcResponse, errorResponse, resultResponse } from "./rpc.js";

const RUNTIME = "node";

export function handle(method: string, _params: Record<string, unknown>): Record<string, unknown> {
  // The host maps a command id to a method; dispatch on the trailing segment so
  // the worker is robust to the host's exact method prefix. A real handler reads
  // `_params` for the request arguments.
  const command = method.split(".").pop();
  if (command === "status") {
    return { ok: true, runtime: RUNTIME, message: "{{ cookiecutter.plugin_name }} worker is running" };
  }
  throw new MethodNotFoundError(method);
}

export function processLine(line: string): RpcResponse | null {
  let request: unknown;
  try {
    request = JSON.parse(line);
  } catch {
    return null;
  }
  if (request === null || typeof request !== "object" || Array.isArray(request)) {
    return null; // not a JSON-RPC object: ignore
  }
  const message = request as Record<string, unknown>;
  const id = message.id;
  if (id === undefined || id === null) {
    return null; // a notification: no response
  }
  try {
    const params = message.params;
    const result = handle(
      String(message.method ?? ""),
      params !== null && typeof params === "object" && !Array.isArray(params) ? (params as Record<string, unknown>) : {},
    );
    return resultResponse(id, result);
  } catch (err) {
    return errorResponse(id, err);
  }
}

export function main(): void {
  const rl = readline.createInterface({ input: process.stdin, terminal: false });
  rl.on("line", (line) => {
    const trimmed = line.trim();
    if (trimmed === "") {
      return;
    }
    const response = processLine(trimmed);
    if (response !== null) {
      process.stdout.write(JSON.stringify(response) + "\n");
    }
  });
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}
