import httpx
import pytest

from app.gmail import get_access_token

def make_client(handler) -> httpx.Client:
    return httpx.Client(transport=httpx.MockTransport(handler))

def test_get_access_token_success():
    def handler(request: httpx.Request) -> httpx.Response:
        body = request.content.decode()

        assert str(request.url) == "https://oauth2.googleapis.com/token"
        assert "grant_type=refresh_token" in body
        assert "refresh_token=test-refreshToken" in body
        return httpx.Response(200, json={"access_token": "new-access-token"})

    assert get_access_token(make_client(handler), "test-refreshToken") == "new-access-token"

def test_get_access_token_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(400, json={"error": "invalid_grant"})

    with pytest.raises(httpx.HTTPStatusError):
        get_access_token(make_client(handler), "revoked")