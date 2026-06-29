use std::io::Write;
use std::process::{Command, Stdio};

fn run_worker(input: &str) -> String {
    let mut child = Command::new(env!("CARGO_BIN_EXE_{{ cookiecutter.project_slug }}-worker"))
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .expect("spawn worker");
    child
        .stdin
        .take()
        .expect("stdin")
        .write_all(input.as_bytes())
        .expect("write stdin");
    let output = child.wait_with_output().expect("wait");
    String::from_utf8(output.stdout).expect("utf8")
}

#[test]
fn status_returns_ok() {
    let out = run_worker("{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"x.status\"}\n");
    assert!(out.contains("\"ok\":true"), "got: {out}");
    assert!(out.contains("\"runtime\":\"rust\""), "got: {out}");
}

#[test]
fn unknown_method_errors() {
    let out = run_worker("{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"x.nope\"}\n");
    assert!(out.contains("-32601"), "got: {out}");
}

#[test]
fn notification_has_no_response() {
    let out = run_worker("{\"jsonrpc\":\"2.0\",\"method\":\"x.status\"}\n");
    assert!(out.trim().is_empty(), "got: {out}");
}
