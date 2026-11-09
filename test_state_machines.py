"""Exercise client transitions through real Authlib with an offline HTTP boundary."""

import json
from datetime import date, timedelta
from unittest.mock import Mock
from urllib.parse import parse_qs

import pytest
from authlib.integrations.base_client.errors import (
    InvalidTokenError,
    MissingTokenError,
    OAuthError,
)
from requests import HTTPError, Response, Session, Timeout

import pulse_throw as pt


@pytest.fixture
def transport(monkeypatch):
    calls = []
    pending = []

    def send(_session, request, **kwargs):
        calls.append((request, kwargs))
        assert pending, f"Unexpected HTTP request: {request.method} {request.url}"
        payload, status = pending.pop(0)
        if isinstance(payload, Exception):
            raise payload
        response = Response()
        response.status_code = status
        response.request = request
        response.url = request.url
        response.headers["Content-Type"] = "application/json"
        response._content = json.dumps(payload).encode()
        return response

    def enqueue(payload, status=200):
        pending.append((payload, status))

    monkeypatch.setattr(Session, "send", send)
    yield enqueue, calls
    assert not pending, "Expected HTTP responses were not consumed"


@pytest.fixture
def client():
    with pt.PulseClient(
        "client", "secret", "initial-refresh", authenticate=False
    ) as obj:
        yield obj


def token(**overrides):
    return {
        "access_token": "access",
        "token_type": "Bearer",
        "expires_in": 3600,
        "user_id": "athlete",
        **overrides,
    }


def test_constructor_authenticates_and_context_closes(transport, monkeypatch):
    enqueue, calls = transport
    enqueue(token())
    close = Mock()
    monkeypatch.setattr(Session, "close", close)

    with pt.PulseClient("client", "secret", "initial-refresh") as obj:
        assert obj.is_authenticated()
        assert obj.user_id == "athlete"
        assert obj.session.token["refresh_token"] == "initial-refresh"
        assert str(obj) == "PulseClient(athlete)"

    close.assert_called_once_with()
    assert calls[0][0].url == f"{pt.API_URL}/oauth/token"


@pytest.mark.parametrize("raises", [False, True])
def test_context_closes_on_normal_and_exceptional_exit(client, monkeypatch, raises):
    close = Mock()
    monkeypatch.setattr(client.session, "close", close)

    def enter():
        with client as entered:
            assert entered is client
            if raises:
                raise ValueError("body failed")

    if raises:
        with pytest.raises(ValueError, match="body failed"):
            enter()
    else:
        enter()

    close.assert_called_once_with()


def test_supplied_token_initializes_identity_without_authentication(transport):
    _, calls = transport
    with pt.PulseClient(
        "client", "secret", "initial-refresh", authenticate=False, token=token()
    ) as obj:
        assert obj.is_authenticated()
        assert obj.user_id == "athlete"
        assert obj._format_user_ids(None) == ["athlete"]
    assert calls == []


def test_custom_token_endpoint_remains_supported(transport):
    enqueue, calls = transport
    enqueue(token(refresh_token="rotated-refresh"))
    enqueue({"data": {"id": "athlete"}})
    with pt.PulseClient(
        "client",
        "secret",
        "initial-refresh",
        authenticate=False,
        token=token(refresh_token="initial-refresh", expires_at=1),
        token_endpoint="https://example.test/oauth/token",
    ) as obj:
        obj.get_profile()
    assert calls[0][0].url == "https://example.test/oauth/token"


@pytest.mark.parametrize(
    "endpoint", ["get_profile", "get_team", "get_snapshots", "get_events"]
)
def test_unauthenticated_requests_fail_without_http(client, transport, endpoint):
    _, calls = transport
    with pytest.raises(MissingTokenError, match="Try calling authenticate"):
        getattr(client, endpoint)()
    assert calls == []
    assert not client.is_authenticated()
    assert client.user_id == ""


def test_manual_authentication_retains_and_rotates_refresh_tokens(client, transport):
    enqueue, calls = transport
    for response in [token(), token(refresh_token="rotated-refresh"), token()]:
        enqueue(response)
        client.authenticate(timeout=7)

    assert [parse_qs(request.body)["refresh_token"] for request, _ in calls] == [
        ["initial-refresh"],
        ["initial-refresh"],
        ["rotated-refresh"],
    ]
    assert all(kwargs["timeout"] == 7 for _, kwargs in calls)
    assert client.session.token["refresh_token"] == "rotated-refresh"


def test_expiry_refreshes_before_request_and_keeps_latest_refresh_token(
    client, transport
):
    enqueue, calls = transport
    enqueue(token())
    client.authenticate()

    for access_token, refresh_response in [
        ("access-2", token(access_token="access-2", refresh_token="rotated-refresh")),
        ("access-3", token(access_token="access-3")),
    ]:
        refresh_response.pop("user_id")
        client.session.token["expires_at"] = 1
        assert client.is_authenticated()
        enqueue(refresh_response)
        enqueue({"data": {"id": "athlete"}})
        assert client.get_profile() == {"id": "athlete"}
        assert calls[-1][0].headers["Authorization"] == f"Bearer {access_token}"
        assert calls[-1][1]["timeout"] == 30
        assert client.user_id == "athlete"

    enqueue(token())
    client.authenticate()
    refresh_requests = [
        request for request, _ in calls if request.url.endswith("/oauth/token")
    ]
    assert [
        parse_qs(request.body)["refresh_token"] for request in refresh_requests
    ] == [
        ["initial-refresh"],
        ["initial-refresh"],
        ["rotated-refresh"],
        ["rotated-refresh"],
    ]
    assert client.session.token["refresh_token"] == "rotated-refresh"


@pytest.mark.parametrize("identity", [{}, {"user_id": None}])
def test_missing_identity_stays_unknown_then_recovers(client, transport, identity):
    enqueue, _ = transport
    response = token()
    response.pop("user_id")
    enqueue({**response, **identity})
    client.authenticate()
    assert client.user_id == ""

    enqueue(token())
    client.authenticate()
    assert client.user_id == "athlete"

    enqueue({**response, **identity})
    client.authenticate()
    assert client.user_id == "athlete"


def test_new_identity_updates_default_request_target(client, transport):
    enqueue, calls = transport
    enqueue(token())
    client.authenticate()
    enqueue(token(user_id="other-athlete"))
    client.authenticate()
    enqueue({"data": {"other-athlete": []}})
    assert client.get_events() == {"other-athlete": []}
    assert json.loads(calls[-1][0].body)["payload"]["pulseUserIds"] == ["other-athlete"]


@pytest.mark.parametrize("authenticated", [False, True])
@pytest.mark.parametrize("failure", ["oauth", "http", "timeout"])
def test_failed_authentication_preserves_state(
    client, transport, authenticated, failure
):
    enqueue, _ = transport
    if authenticated:
        enqueue(token(refresh_token="rotated-refresh"))
        client.authenticate()
    previous_token = dict(client.session.token) if authenticated else None
    previous_id = client.user_id

    if failure == "oauth":
        enqueue({"error": "invalid_grant"})
        expected = OAuthError
    elif failure == "http":
        enqueue({}, status=503)
        expected = HTTPError
    else:
        enqueue(Timeout("token request timed out"))
        expected = Timeout

    with pytest.raises(expected):
        client.authenticate()
    assert client.session.token == previous_token
    assert client.user_id == previous_id
    assert client.is_authenticated() is authenticated

    enqueue(token())
    client.authenticate()
    assert client.is_authenticated()
    assert client.user_id == "athlete"


def test_failed_automatic_refresh_does_not_send_resource_request(client, transport):
    enqueue, calls = transport
    enqueue(token())
    client.authenticate()
    client.session.token["expires_at"] = 1
    previous_token = dict(client.session.token)
    enqueue({"error": "invalid_grant"})
    with pytest.raises(OAuthError):
        client.get_profile()
    assert client.session.token == previous_token
    assert client.user_id == "athlete"
    assert all(request.url.endswith("/oauth/token") for request, _ in calls)

    enqueue(token())
    client.authenticate()
    enqueue({"data": {"id": "athlete"}})
    assert client.get_profile() == {"id": "athlete"}


def test_expired_supplied_token_without_refresh_token_fails_locally(client, transport):
    _, calls = transport
    client.session.token = token(expires_at=1)
    with pytest.raises(InvalidTokenError):
        client.get_profile()
    assert calls == []


@pytest.mark.parametrize("status", [401, 403, 429, 500])
def test_http_errors_propagate_without_retry_or_token_changes(
    client, transport, status
):
    enqueue, calls = transport
    enqueue(token())
    client.authenticate()
    previous_token = dict(client.session.token)
    enqueue({"error": "request failed"}, status=status)
    with pytest.raises(HTTPError):
        client.get_profile()
    assert len(calls) == 2
    assert client.session.token == previous_token


def test_missing_response_data_propagates_without_changing_identity(client, transport):
    enqueue, _ = transport
    enqueue(token())
    client.authenticate()
    enqueue({})
    with pytest.raises(KeyError, match="data"):
        client.get_profile()
    assert client.user_id == "athlete"


@pytest.mark.parametrize(
    "timespan, acute, chronic",
    [
        (0, 13.0, 6.0),
        (5, 3.46875, 3.0),
        (6, 2.8333333333, 2.7272727273),
        (8, 2.3333333333, 2.3076923077),
        (9, 0.0, 2.1428571429),
        (22, 0.0, 1.1111111111),
        (23, 0.0, 1.0714285714),
        (27, 0.0, 1.0714285714),
        (28, 0.0, 0.0),
    ],
)
def test_workload_ramps_and_window_expiry(timespan, acute, chronic):
    snapshots = [{"date": "2022-01-01", "normDailyWorkload": 30.0}]
    end = str(date(2022, 1, 1) + timedelta(days=timespan))
    assert pt.compute_acute_workload(snapshots, end_date=end) == pytest.approx(acute)
    assert pt.compute_chronic_workload(snapshots, end_date=end) == pytest.approx(
        chronic
    )
    if timespan >= 9:
        assert pt.compute_acr(snapshots, end_date=end) == 0.0
