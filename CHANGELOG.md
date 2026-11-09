# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `test_state_machines.py`: offline tests of authentication, token refresh, identity
  and workload transitions through real Authlib with a stubbed HTTP boundary.
- GitHub Actions CI across Python 3.12-3.14 (ruff, mypy, pytest with coverage,
  package build).
- README notes on token refresh, `is_authenticated()` and `user_id` semantics.

### Changed
- Tooling: Poetry replaced by PEP 621 metadata, Hatchling and uv; black, isort,
  flake8, pylint and pyupgrade replaced by ruff; strict mypy and pre-commit hooks
  updated to match the `whoop` repo.
- Minimum supported Python is now 3.12.
- Tests that need recorded API cassettes carry a `live` marker and are deselected by
  default (`pytest -m live` to run them).

### Fixed
- `OAuth2Session` was constructed with the misspelled `token_endpont=` keyword, so
  Authlib had no token endpoint and could not refresh expired access tokens
  automatically. It now receives `token_endpoint`, which callers can still override.
- `authenticate()` reuses the latest (possibly rotated) refresh token, and retains the
  token used when a response omits a replacement.
- `user_id` is initialized from a supplied token, updated when a new non-null ID is
  returned, and retained when a response omits it.
- `test_refresh_token` referenced a nonexistent `PulseClient.API_URL`.
