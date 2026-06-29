from {{ cookiecutter.project_slug|replace('-', '_') }}.rpc import MethodNotFoundError, error_response, result_response


def test_result_response_shape():
    assert result_response(1, {"ok": True}) == {"jsonrpc": "2.0", "id": 1, "result": {"ok": True}}


def test_method_not_found_maps_to_32601():
    response = error_response(5, MethodNotFoundError("x.y"))
    assert response["error"]["code"] == -32601


def test_internal_error_maps_to_32603():
    response = error_response(5, ValueError("boom"))
    assert response["error"]["code"] == -32603
