//! JSON-RPC 2.0 response builders. A `MethodNotFound` becomes -32601.

use serde_json::{json, Value};

pub const ERR_METHOD_NOT_FOUND: i64 = -32601;

pub enum RpcError {
    MethodNotFound(String),
}

pub fn result_response(id: &Value, result: Value) -> Value {
    json!({"jsonrpc": "2.0", "id": id, "result": result})
}

pub fn error_response(id: &Value, err: &RpcError) -> Value {
    let (code, message) = match err {
        RpcError::MethodNotFound(method) => {
            (ERR_METHOD_NOT_FOUND, format!("unknown method '{method}'"))
        }
    };
    json!({"jsonrpc": "2.0", "id": id, "error": {"code": code, "message": message}})
}
