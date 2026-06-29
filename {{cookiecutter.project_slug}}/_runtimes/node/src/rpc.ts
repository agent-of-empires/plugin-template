// JSON-RPC 2.0 response builders. A MethodNotFoundError becomes -32601; any
// other error becomes the internal-error code -32603.

export const ERR_METHOD_NOT_FOUND = -32601;
export const ERR_INTERNAL = -32603;

export class MethodNotFoundError extends Error {}

export interface RpcResponse {
  jsonrpc: "2.0";
  id: unknown;
  result?: unknown;
  error?: { code: number; message: string };
}

export function resultResponse(id: unknown, result: unknown): RpcResponse {
  return { jsonrpc: "2.0", id, result };
}

export function errorResponse(id: unknown, err: unknown): RpcResponse {
  if (err instanceof MethodNotFoundError) {
    return { jsonrpc: "2.0", id, error: { code: ERR_METHOD_NOT_FOUND, message: `unknown method '${err.message}'` } };
  }
  const message = err instanceof Error ? err.message : String(err);
  return { jsonrpc: "2.0", id, error: { code: ERR_INTERNAL, message } };
}
