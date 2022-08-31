"""Tools for acquiring and analyzing Pulse API data.

Pulse is a wearable sensor for baseball players to monitor throwing workload. Learn more
about Pulse at https://www.drivelinebaseball.com/pulse/.

More information about acute workload, chronic workload, and acute/chronic workload
ratio can be found at the following links:
    https://www.drivelinebaseball.com/2020/04/what-is-throwing-workload/

    https://www.researchgate.net/publication/336345883_OPTIMIZED_ACUTE_WORKLOAD_COMPUTATION_FOR_BASEBALL_PITCHERS_COUPLED_9-DAY_EXPONENTIALLY_WEIGHTED_AVERAGES_WITH_DYNAMIC_DIVISORS

Examples:
    Loading environment variables:
        import os
        from dotenv import load_dotenv

        load_dotenv()

        client_id = os.getenv("CLIENT_ID") or ""
        client_secret = os.getenv("CLIENT_SECRET") or ""
        refresh_token = os.getenv("REFRESH_TOKEN") or ""

    Creating a client:
        import pulse

        client = pulse.PulseClient(client_id, client_secret, refresh_token)
        del client

        with pulse.PulseClient(client_id, client_secret, refresh_token) as client:
            ...

    Making requests for a single user (the owner of the session):
        client = pulse.PulseClient(client_id, client_secret, refresh_token)

        events = client.get_events()
        snapshots = client.get_snapshots()

        print(events[client.user_id])
        print(snapshots[client.user_id])

Attributes:
    ACUTE_LENGTH (int): Length in days for the acute workload window.
    ACUTE_WEIGHTS (List[float]): Weights used for acute workload calculations.

    CHRONIC_LENGTH (int): Length in days for the chronic workload window.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from authlib.integrations.base_client.errors import MissingTokenError
from authlib.integrations.requests_client import OAuth2Session


ACUTE_LENGTH = 9  # days
ACUTE_WEIGHTS = [1.3, 1.225, 1.15, 1.075, 1.0, 0.925, 0.85, 0.775, 0.7]

CHRONIC_LENGTH = 28  # days


########################################################################################
# PULSE CLIENT


class PulseClient:
    """Make requests to the Pulse API.

    Attributes:
        API_URL (str): Base URL for API requests.
        session (authlib.OAuth2Session): OAuth2Session for accessing the Pulse API.
        user_id (str): User ID of the owner of the session. Will default to an empty
            string before the session is authenticated and then replaced by the correct
            user ID once a token is fetched.

    Raises:
        ValueError: If `start_date` is after `end_date`.
    """

    API_URL = "https://pulse-server.drivelinebaseball.com/third_party_api"

    ####################################################################################
    # DUNDER METHODS

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        refresh_token: str,
        authenticate: bool = True,
        **kwargs,
    ):
        """Initialize an OAuth2 session for making API requests.

        Optionally makes a request to the Pulse API to acquire an access token.

        Args:
            client_id (str): API client ID provided by Pulse.
            client_secret (str): API client secret provided by Pulse.
            refresh_token (str): API refresh token provided by Pulse.
            authenticate (bool): Whether to fetch a token from the API upon
                session creation. If false, `authenticate()` must be called manually.
                Defaults to true.
            kwargs (Dict[str, Any], optional): Additional arguments for OAuth2Session.
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._refresh_token = refresh_token

        self.session = OAuth2Session(
            client_id,
            client_secret,
            token_endpont=f"{self.API_URL}/oauth/token",
            **kwargs,
        )

        self.user_id = ""

        if authenticate:
            self.authenticate()

    def __del__(self) -> None:
        """Close the OAuth2Session."""
        self.session.close()

    def __enter__(self) -> PulseClient:
        """Enter a context manager.

        Returns:
            PulseClient: A Pulse client with an active OAuth2Session.
        """
        return self

    def __exit__(self, *_) -> None:
        """Exit a context manager by closing the OAuth2 session.

        Args:
            _ (Any): Exception arguments passed when closing context manager.
        """
        del self

    def __str__(self) -> str:
        """Generate string representation of client.

        Returns:
            str: String representation of client featuring user ID of the owner of the
                session.
        """
        return f"PulseClient({self.user_id if self.user_id else '<Unauthenticated>'})"

    ####################################################################################
    # API ENDPOINTS

    def get_profile(self) -> dict[str, str]:
        """Make request to Get Profile endpoint.

        Returns info about the owner of the session.

        Returns:
            Dict[str, str]: Response JSON data loaded into an object. Example:
                {
                    "id": "<id>",
                    "firstName": "<first-name>",
                    "lastName": "<last-name>",
                    "email": "<email>"
                }
        """
        return self._make_request(method="POST", url_slug="user/get_profile")

    def get_team(self) -> dict[str, str]:
        """Make request to Get Team endpoint.

        Returns info about the owner of the session's team.

        Returns:
            Dict[str, str]: Response JSON data loaded into an object. Example:
                {
                    "team": {
                        "name": "TEAMNAME",
                        "id": "JQtyNOYdDH"
                    },
                    "members": [
                        {
                            "userId": "r5FiwuBlYZ",
                            "teamMemberId": "yvUsIxsjrg",
                            "athleteProfileId": "dgTHp0nlN0",
                            "firstName": "<player-first-name>",
                            "lastName": "<player-last-name>",
                            "email": "<player-email>"
                        },
                        ...
        """
        return self._make_request(method="POST", url_slug="user/get_team")

    def get_snapshots(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        user_ids: str | list[str] | None = None,
    ) -> dict[str, Any]:
        """Make request to Get Snapshots endpoint.

        Gets daily snapshots generated for one or more users over a range of dates. The
        owner of the session must have permission to access their data (e.g. the
        requested users must be either the current user or a member of a team for which
        the current user is a coach).

        Args:
            start_date (str, optional): The earliest date for which to get data.
                Expected in ISO 8601 format (YYYY-MM-DD). Defaults to eight days before
                `end_date`.
            end_date (str, optional): The latest date for which to get data. Expected
                in ISO 8601 format (YYYY-MM-DD). Defaults to today's date.
            user_ids (str | List[str], optional): User IDs for whom to get data. IDs
                must belong to the owner of the session or a member their team.
                Defaults to the ID of the owner of the session.

        Returns:
            Dict[str, Any]: Response JSON data loaded into an object. Example:
                {
                    "<id>": [
                        {
                            "date": "2021-08-01",
                            "throwCount": 0,
                            "highEffortThrowCount": 0,
                            "acuteWorkload": 2041.948878326791,
                            "chronicWorkload": 3229.3557437324716,
                            "normAcuteWorkload": 3.1660202416772414,
                            "normChronicWorkload": 5.007082087486716,
                            "workloadRatio": 0.6323084356035417,
                            "dailyWorkload": 0,
                            "normDailyWorkload": 0,
                            "baseballProjectedOneDayWorkloads": [
                                0,
                                30,
                                26.82887058971028,
                                ...
                            ]
                        },
                        ...
        """
        return self._make_request(
            method="POST",
            url_slug="user/get_snapshots",
            json=self._format_payload(start_date, end_date, user_ids),
        )

    def get_events(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        user_ids: str | list[str] | None = None,
    ) -> dict[str, Any]:
        """Make request to Get Events endpoint.

        Gets all of the individual throw events for one or more users over a range of
        dates. The owner of the session must have permission to access their data (e.g.
        the requested users must be either the current user or a member of a team for
        which the current user is a coach).

        Args:
            start_date (str, optional): The earliest date for which to get data.
                Expected in ISO 8601 format (YYYY-MM-DD). Defaults to eight days before
                `end_date`.
            end_date (str, optional): The latest date for which to get data. Expected
                in ISO 8601 format (YYYY-MM-DD). Defaults to today's date.
            user_ids (str | List[str], optional): User IDs for whom to get data. IDs
                must belong to the owner of the session or their team. Defaults to the
                ID of the owner of the session.

        Returns:
            Dict[str, Any]: Response JSON data loaded into an object. Example:
                {
                    "<id>": [
                        {
                            "eventId": "POC6TE5b8V",
                            "scaler": null,
                            "datetime": "2021-03-01T15:49:55.000Z",
                            "tag": null,
                            "armSlot": 59.782794823856534,
                            "armSpeed": 452.4706718068326,
                            "shoulderRotation": 155.58127276383868,
                            "torque": 34.744537353515625,
                            "ballVelocity": null,
                            "highEffort": false,
                            "ballWeight (oz)": 5.11472,
                            "preferredBallWeightUnit": "OZ",
                            "simulated": null,
                            "workload": 100.728515625,
                            "normalizedWorkload": 0.10925094783306122
                        },
                        ...
        """
        return self._make_request(
            method="POST",
            url_slug="user/get_events",
            json=self._format_payload(start_date, end_date, user_ids),
        )

    ####################################################################################
    # API HELPER METHODS

    def authenticate(self, **kwargs) -> None:
        """Authenticate OAuth2Session by fetching token.

        If `user_id` is `None`, it will be set according to the `user_id` returned with
        the token.

        Args:
            kwargs (Dict[str, Any], optional): Additional arguments for `fetch_token()`.
        """
        self.session.fetch_token(
            url=f"{self.API_URL}/oauth/token",
            grant_type="refresh_token",
            refresh_token=self._refresh_token,
            **kwargs,
        )

        if not self.user_id:
            self.user_id = str(self.session.token.get("user_id"))

    def is_authenticated(self) -> bool:
        """Check if the OAuth2Session is authenticated.

        Returns:
            bool: Whether the OAuth2Session has a token and is therefore authenticated.
        """
        return self.session.token is not None

    def _make_request(
        self, method: str, url_slug: str, **kwargs: Any
    ) -> dict[str, Any]:
        try:
            response = self.session.request(
                method=method, url=f"{self.API_URL}/{url_slug}", **kwargs
            )
        except MissingTokenError as exc:
            raise MissingTokenError(
                "Client is not authenticated. Try calling authenticate()."
            ) from exc

        response.raise_for_status()

        return response.json()["data"]

    def _format_payload(
        self,
        start_date: str | None,
        end_date: str | None,
        user_ids: str | list[str] | None,
    ) -> dict[str, dict[str, str | list[str]]]:
        start, end = self._format_dates(start_date, end_date)
        users = self._format_user_ids(user_ids)

        return {
            "payload": {
                "pulseUserIds": users,
                "startDate": start,
                "endDate": end,
            },
        }

    def _format_user_ids(self, user_ids: str | list[str] | None) -> list[str]:
        if not user_ids:
            return [self.user_id]

        if isinstance(user_ids, str):
            return [user_ids]

        return user_ids

    def _format_dates(
        self, start_date: str | None, end_date: str | None
    ) -> tuple[str, str]:
        end = date.fromisoformat(end_date) if end_date else date.today()
        start = (
            date.fromisoformat(start_date) if start_date else end - timedelta(days=8)
        )

        if start > end:
            raise ValueError(f"Start date greater than end date: {start} > {end}")

        return str(start), str(end)


########################################################################################
# FILTER FUNCTIONS


def filter_by_tag(
    events: list[dict[str, Any]], tags: str | list[str], blacklist: bool = False
) -> list[dict[str, Any]]:
    """Filter throw events by tag or tags.

    Args:
        events (List[Dict[str, Any]]): Individual throw data from `get_events` endpoint.
        tags (str | List[str]): Single or multiple tags to match.
        blacklist (bool): If false, will return throw events with a matching
            tag. If true, will return throw events without a matching tag. Defaults to
            false.

    Returns:
        List[Dict[str, Any]]: Throw events filtered by tags, either whitelisted or
            blacklisted.
    """
    if isinstance(tags, str):
        tags = [tags]

    return (
        [event for event in events if event.get("tag") in tags]
        if not blacklist
        else [event for event in events if event.get("tag") not in tags]
    )


def filter_simulated(
    events: list[dict[str, Any]], get_simulated: bool = False
) -> list[dict[str, Any]]:
    """Filter throw events based on simulated status.

    Args:
        events (List[Dict[str, Any]]): Individual throw data from `get_events` endpoint.
        get_simulated (bool): If true, will return simulated throw events. If
            false, will return unsimulated throw events. Defaults to false.

    Returns:
        List[Dict[str, Any]]: Throw events filtered by simulated status based on
            `get_simulated` parameter.
    """
    return [event for event in events if event.get("simulated") is get_simulated]


def filter_high_effort(
    events: list[dict[str, Any]], get_high_effort: bool = True
) -> list[dict[str, Any]]:
    """Filter throw events based on high effort status.

    Args:
        events (List[Dict[str, Any]]): Individual throw data from `get_events` endpoint.
        get_high_effort (bool): If true, will return high effort throw
            events. If false, will return throw events not marked as high effort.
            Defaults to true.

    Returns:
        List[Dict[str, Any]]: Throw events filtered by high effort events basedon
            `get_high_effort` parameter.
    """
    return [event for event in events if event.get("highEffort") is get_high_effort]


########################################################################################
# WORKLOAD FUNCTIONS


def sum_workload(events: list[dict[str, Any]], normalized: bool = True) -> float:
    """Compute sum of workloads from individual throw events.

    Args:
        events (List[Dict[str, Any]]): Individual throw data from `get_events` endpoint.
        normalized (bool): If true, will return normalized data. If false,
            will return unnormalized data. Defaults to true.

    Returns:
        float: Total workload for given throws.
    """
    return sum(
        event["normalizedWorkload" if normalized else "workload"] for event in events
    )


def compute_acute_workload(
    snapshots: list[dict[str, Any]],
    end_date: str | None = None,
    normalized: bool = True,
) -> float:
    """Compute acute workload from daily snapshots.

    Acute workload is a weighted average. Each weight is indexed by how many days
    before `end_date` it is to be used for. For example, the weight in the positon 2 of
    the list is the weight to be used for date `end_date - 2 days`.

    This function assumes that the dates in `snapshots` are the only days of throwing
    and will adjust the acute divisor accordingly.

    Args:
        snapshots (List[Dict[str, Any]]): Daily snapshot data from `get_snapshots`
            endpoint.
        end_date (str, optional): Date for which to get acute workload. Expected in ISO
            8601 format (YYYY-MM-DD). Defaults to the most recent date in `snapshots`.
        normalized (bool): If true, will return normalized data. If false,
            will return unnormalized data. Defaults to true.

    Raises:
        ValueError: If `start_date` is after `end_date`.

    Returns:
        float: Acute workload value for given date range.
    """
    workloads = _get_workloads_by_date(snapshots, normalized)

    start = min(workloads.keys())
    end = date.fromisoformat(end_date) if end_date else max(workloads.keys())

    if start > end:
        raise ValueError(f"Start date greater than end date: {start} > {end}")

    return sum(
        workloads.get(end - timedelta(days=offset), 0.0) * ACUTE_WEIGHTS[offset]
        for offset in range(ACUTE_LENGTH)
    ) / _get_acute_divisor((end - start).days)


def compute_chronic_workload(
    snapshots: list[dict[str, Any]],
    end_date: str | None = None,
    normalized: bool = True,
) -> float:
    """Compute chronic workload from daily snapshots.

    This function assumes that the dates in `snapshots` are the only days of throwing
    and will adjust the chronic divisor accordingly.

    Args:
        snapshots (List[Dict[str, Any]]): Daily snapshot data from `get_snapshots`
            endpoint.
        end_date (str, optional): Date for which to get chronic workload. Expected in
            ISO 8601 format (YYYY-MM-DD). Defaults to the most recent date in
            `snapshots`.
        normalized (bool): If true, will return normalized data. If false,
            will return unnormalized data. Defaults to true.

    Raises:
        ValueError: If `start_date` is after `end_date`.

    Returns:
        float: Chronic workload value for given date range.
    """
    workloads = _get_workloads_by_date(snapshots, normalized)

    start = min(workloads.keys())
    end = date.fromisoformat(end_date) if end_date else max(workloads.keys())

    if start > end:
        raise ValueError(f"Start date greater than end date: {start} > {end}")

    return sum(
        workloads.get(end - timedelta(days=offset), 0.0)
        for offset in range(CHRONIC_LENGTH)
    ) / _get_chronic_divisor((end - start).days)


def compute_acr(
    snapshots: list[dict[str, Any]],
    end_date: str | None = None,
    normalized: bool = True,
) -> float:
    """Compute acute/chronic workload ratio from daily snapshots.

    Args:
        snapshots (List[Dict[str, Any]]): Daily snapshot data from `get_snapshots`
            endpoint.
        end_date (str, optional): Date for which to get acute/chronic workload ratio.
            Expected in ISO 8601 format (YYYY-MM-DD). Defaults to the most recent date
            in `snapshots`.
        normalized (bool): If true, will return normalized data. If false,
            will return unnormalized data. Defaults to true.

    Returns:
        float: Acute/chronic workload ratio for given date range.
    """
    chronic_workload = compute_chronic_workload(snapshots, end_date, normalized)

    if chronic_workload == 0.0:
        return 0.0

    acute_workload = compute_acute_workload(snapshots, end_date, normalized)

    return acute_workload / chronic_workload


########################################################################################
# WORKLOAD HELPER FUNCTIONS


def _get_workloads_by_date(
    snapshots: list[dict[str, Any]], normalized: bool
) -> dict[date, float]:
    return {
        date.fromisoformat(snapshot["date"]): snapshot[
            "normDailyWorkload" if normalized else "dailyWorkload"
        ]
        for snapshot in snapshots
    }


def _get_acute_divisor(timespan: int) -> int:
    """Get acute divisor according to Pulse specifications.

    Args:
        timespan (int): Length of time that is covered between the min and max dates in
            a weighted workload calculation.

    Returns:
        int: Acute divisor for given timespan. Determined according to the pattern:
            After 1 day of throwing: 3
            After 2 days of throwing: 4
            After 3 days of throwing: 5
            ...
            After 7 days of throwing: 9

            As described here:
            https://www.drivelinebaseball.com/2020/04/what-is-throwing-workload/
    """
    return ACUTE_LENGTH if timespan >= 6 else timespan + 3


def _get_chronic_divisor(timespan: int) -> int:
    """Get chronic divisor according to Pulse specifications.

    Args:
        timespan (int): Length of time that is covered between the min and max dates in
            a weighted workload calculation.

    Returns:
        int: Chronic divisor for given timespan. Determined according to the pattern:
            After 1 day of throwing: 5
            After 2 days of throwing: 6
            After 3 days of throwing: 7
            ...
            After 24 days of throwing: 28

            As described here:
            https://www.drivelinebaseball.com/2020/04/what-is-throwing-workload/

            Due to how `timedelta` works in Python, "1 day of throwing" is actually a
            timespan of 0 days (`start_date - end_date == 0`).
    """
    return CHRONIC_LENGTH if timespan >= 23 else timespan + 5
