//! Agent of Empires worker: JSON-RPC 2.0 over newline-delimited JSON on stdio.
//!
//! The host spawns this process, sends one JSON-RPC request per line on stdin,
//! and reads one response per line on stdout. The worker exits cleanly on EOF.

mod rpc;

use std::io::{self, BufRead, Write};

use serde_json::{json, Value};

use rpc::{error_response, result_response, RpcError};

const RUNTIME: &str = "rust";

fn handle(method: &str, _params: &Value) -> Result<Value, RpcError> {
    // The host maps a command id to a method; dispatch on the trailing segment so
    // the worker is robust to the host's exact method prefix. A real handler reads
    // `_params` for the request arguments.
    let command = method.rsplit('.').next().unwrap_or(method);
    if command == "status" {
        Ok(json!({"ok": true, "runtime": RUNTIME, "message": "{{ cookiecutter.plugin_name }} worker is running"}))
    } else {
        Err(RpcError::MethodNotFound(method.to_string()))
    }
}

fn process_line(line: &str) -> Option<Value> {
    let request: Value = serde_json::from_str(line).ok()?;
    let id = request.get("id")?;
    if id.is_null() {
        return None; // a notification: no response
    }
    let method = request.get("method").and_then(Value::as_str).unwrap_or("");
    let params = request.get("params").cloned().unwrap_or_else(|| json!({}));
    Some(match handle(method, &params) {
        Ok(result) => result_response(id, result),
        Err(err) => error_response(id, &err),
    })
}

fn main() {
    let stdin = io::stdin();
    let stdout = io::stdout();
    let mut out = stdout.lock();
    for line in stdin.lock().lines() {
        let Ok(line) = line else { break };
        let trimmed = line.trim();
        if trimmed.is_empty() {
            continue;
        }
        if let Some(response) = process_line(trimmed) {
            let _ = writeln!(
                out,
                "{}",
                serde_json::to_string(&response).unwrap_or_default()
            );
            let _ = out.flush();
        }
    }
}
