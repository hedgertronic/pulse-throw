# Pulse Throw for Python <!-- omit in toc -->

Tools for acquiring and analyzing Pulse API data.

[Pulse](https://www.drivelinebaseball.com/pulse/) is a wearable sensor for baseball players to monitor throwing workload.

- [Installation](#installation)
- [Getting Started](#getting-started)
- [API Requests](#api-requests)
  - [Get Profile](#get-profile)
  - [Get Team](#get-team)
  - [Get Snapshots](#get-snapshots)
  - [Get Events](#get-events)
- [Data Filtering Functions](#data-filtering-functions)
  - [Filter By Tag](#filter-by-tag)
  - [Filter Simulated](#filter-simulated)
  - [Filter High Effort](#filter-high-effort)
- [Workload Functions](#workload-functions)
  - [Sum Workload](#sum-workload)
  - [Compute Acute Workload](#compute-acute-workload)
  - [Compute Chronic Workload](#compute-chronic-workload)
  - [Compute Acute/Chronic Workload Ratio](#compute-acutechronic-workload-ratio)
- [Additional Resources](#additional-resources)

## Installation

The `pulse` module can be installed via pip:

`pip install pulse-throw`

## Getting Started

In order to use the Pulse client, you must have a `client_id`, `client_secret`, and `refresh_token` provided by the Pulse team at Driveline.

It is best practice to use these values stored in a `.env` file:

```bash
# Pulse credentials
CLIENT_ID="<CLIENT_ID>"
CLIENT_SECRET="<CLIENT_SECRET>"
REFRESH_TOKEN="<REFRESH_TOKEN>"
```

You can use [`python-dotenv`](https://github.com/theskumar/python-dotenv) to load the enviroment variables for use in code:

```python
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID") or ""
client_secret = os.getenv("CLIENT_SECRET") or ""
refresh_token = os.getenv("REFRESH_TOKEN") or ""
```

Once the environment variables are loaded, a `PulseClient` object can created:

```python
import pulse

# Using a traditional constructor and destructor
client = pulse.PulseClient(client_id, client_secret, refresh_token)
...
del client

# Using a context manager that destructs automatically
with pulse.PulseClient(client_id, client_secret, refresh_token) as client:
    ...
```

The Pulse client will authenticate the client upon construction by default. This involves fetching an access token from the API. If you don't want this request to happen automatically, pass `authenticate=False` into the object constructor. In order to make other requests, you will need to manually call the `authenticate()` method so that the other requests have the proper authorization headers:

```python
import pulse

client = pulse.PulseClient(
    client_id, client_secret, refresh_token, authenticate=False
)

client.authenticate()

...

del client
```

## API Requests

There are four different API requests that `PulseClient` can make.

### Get Profile

Returns info about the owner of the session.

**Method**: `get_profile()`

**Payload**: None

**Example Response**:

```json
{
  "id": "<id>",
  "firstName": "<first-name>",
  "lastName": "<last-name>",
  "email": "<email>"
}
```

### Get Team

Returns info about the owner of the session's team.

**Method**: `get_team()`

**Payload**: None

**Example Response**:

```json
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
```

### Get Snapshots

Gets daily snapshots generated for one or more users over a range of dates. The owner of the session must have permission to access their data (e.g. the requested users must be either the current user or a member of a team for which the current user is a coach).

**Method**: `get_snapshots(start_date: str = <end_date - 8 days>, end_date: str = <today's date>, user_ids: str | list[str] = <user_id>)`

**Payload**:

- `startDate`: The earliest date for which to get data, pulled from the `start_date` parameter. Expected in ISO 8601 format (YYYY-MM-DD). Defaults to eight days before the `end_date` parameter.
- `endDate`: The latest date for which to get data, pulled from the `end_date` parameter. Expected in ISO 8601 format (YYYY-MM-DD). Defaults to today's date.
- `pulseUserIds`: User IDs for whom to get data, pulled from the `user_ids` parameter. IDs must belong to the owner of the session or a member of their team. Defaults to the ID of the owner of the session.

**Example Response**:

```json
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
```

### Get Events

Gets all of the individual throw events for one or more users over a range of dates. The owner of the session must have permission to access their data (e.g. the requested users must be either the current user or a member of a team for which the current user is a coach).

**Method**: `get_events(start_date: str = <end_date - 8 days>, end_date: str = <today's date>, user_ids: str | list[str] = <user_id>)`

**Payload**:

- `startDate`: The earliest date for which to get data, pulled from the `start_date` parameter. Expected in ISO 8601 format (YYYY-MM-DD). Defaults to eight days before the `end_date` parameter.
- `endDate`: The latest date for which to get data, pulled from the `end_date` parameter. Expected in ISO 8601 format (YYYY-MM-DD). Defaults to today's date.
- `pulseUserIds`: User IDs for whom to get data, pulled from the `user_ids` parameter. IDs must belong to the owner of the session or a member of their team. Defaults to the ID of the owner of the session.

**Example Response**:

```json
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
```

## Data Filtering Functions

The `pulse` module contains functions that can filter event data based on certain characteristics.

### Filter By Tag

Filter throw events by tag or tags.

**Function**: `filter_by_tag(events: list[dict[str, Any]], tags: str | list[str], blacklist: bool = False)`

```python
# Get all throw events from a single date
events = client.get_events(
    start_date="2022-05-01", end_date="2022-05-01"
)

# Get all throw events marked with the desired tag
pre_game = pulse.filter_by_tag(
    events[client.user_id], tags="Pre-Game"
)

# Get all throw events marked with one of multiple tags
non_game = pulse.filter_by_tag(
    events[client.user_id], tags=["Pre-Game", "Plyo", "Warmup"]
)

# Get all throw events without the desired tag
non_plyos = pulse.filter_by_tag(
    events[client.user_id], tags="Plyo", blacklist=True
)
```

### Filter Simulated

Filter throw events based on simulated status.

**Function**: `filter_simulated(events: list[dict[str, Any]], get_simulated: bool = False)`

```python
# Get all throw events from a single date
events = client.get_events(
    start_date="2022-05-01", end_date="2022-05-01"
)

# Get all throw events that are not simulated
non_simulated = pulse.filter_simulated(events[client.user_id])

# Get all throw events that are simulated
simulated = pulse.filter_simulated(
    events[client.user_id], get_simulated=True
)
```

### Filter High Effort

Filter throw events based on high effort status.

**Function**: `filter_high_effort(events: list[dict[str, Any]], get_high_effort: bool = True)`

```python
# Get all throw events from a single date
events = client.get_events(
    start_date="2022-05-01", end_date="2022-05-01"
)

# Get all throw events that are high effort
high_effort = pulse.filter_high_effort(events[client.user_id])

# Get all throw events that are not high effort
low_effort = pulse.filter_high_effort(
    events[client.user_id], get_high_effort=False
)
```

## Workload Functions

The `pulse` module contains functions that are useful when manually performing workload calculations.

Since throw events and daily snapshots are stored in a dict indexed by user ID, the desired user ID must be accessed by key when passing data into the following functions. For indiviudal users (i.e. not coaches), the desired user ID will be the same as the owner of the session and can be accessed using `client.user_id`. For coaches, the `get_team()` endpoint can match players with their respective user IDs.

### Sum Workload

Compute sum of `workload` or `normalizedWorkload` values from individual throw events returned by the `get_events()` endpoint.

**Function**: `sum_workload(events: list[dict[str, Any]], normalized: bool = True)`

```python
# Get all throw events from a single date
events = client.get_events(
    start_date="2022-05-01", end_date="2022-05-01"
)

# Make sure to access the desired user from events
norm_workload = pulse.sum_workload(events[client.user_id])

# Compute sum using unnormalized values
workload = pulse.sum_workload(
    events[client.user_id], normalized=False
)
```

This function can be useful for summing the workload of throws with a certain tag:

```python
pre_game = pulse.filter_by_tag(events, tag="Pre-Game")

pre_game_workload = pulse.sum_workload(pre_game)
```

### Compute Acute Workload

Compute acute workload using `dailyWorkload` or `normDailyWorkload` values from daily snapshots returned by the `get_snapshots()` endpoint.

**Function**: `compute_acute_workload(snapshots: list[dict[str, Any]], end_date: str = <most recent date in snapshots>, normalized: bool = True)`

```python
# Get daily snapshots for a two week time period.
snapshots = client.get_snapshots(
    start_date="2022-05-01", end_date="2022-05-14"
)

# Make sure to access the desired user from snapshots
norm_acute_workload = pulse.compute_acute_workload(
    snapshots[client.user_id]
)

# Compute acute workload using unnormalized values
acute_workload = pulse.compute_acute_workload(
    snapshots[client.user_id], normalized=False
)
```

Acute workload is the weighted average of one-day workloads over a 9-day period. The weights for the nine days are defined by `pulse.ACUTE_WEIGHTS`:

```python
ACUTE_WEIGHTS = [1.3, 1.225, 1.15, 1.075, 1.0, 0.925, 0.85, 0.775, 0.7]
```

where the current day is multiplied by 1.3 and the last day is multipled by 0.7.

The divisor for acute workload is usually 9, but it can be less if there have been less than 7 days of throwing (3 after 1 day of throwing, 4 after 2 days, ..., 9 after 7+ days). This function assumes that the dates in `snapshots` are the only days of throwing and will adjust the acute divisor accordingly.

### Compute Chronic Workload

Compute chronic workload using `dailyWorkload` or `normDailyWorkload` values from daily snapshots returned by the `get_snapshots()` endpoint.

**Function**: `compute_chronic_workload(snapshots: list[dict[str, Any]], end_date: str = <most recent date in snapshots>, normalized: bool = True)`

```python
# Get daily snapshots for a one month time period.
snapshots = client.get_snapshots(
    start_date="2022-05-01", end_date="2022-06-01"
)

# Make sure to access the desired user from snapshots
norm_chronic_workload = pulse.compute_chronic_workload(
    snapshots[client.user_id]
)

# Compute acute workload using unnormalized values
chronic_workload = pulse.compute_chronic_workload(
    snapshots[client.user_id], normalized=False
)
```

Chronic workload is the average of one-day workloads over a 28-day period.

The divisor for chronic workload is usually 28, but it can be less if there have been less than 24 days of throwing (5 after 1 day of throwing, 6 after 2 days, ..., 28 after 24+ days). This function assumes that the dates in `snapshots` are the only days of throwing and will adjust the chronic divisor accordingly.

### Compute Acute/Chronic Workload Ratio

Compute acute/chronic workload ratio using `dailyWorkload` or `normDailyWorkload` values from daily snapshots returned by the `get_snapshots()` endpoint.

**Function**: `compute_acr(snapshots: list[dict[str, Any]], end_date: str = <most recent date in snapshots>, normalized: bool = True)`

```python
# Get daily snapshots for a one month time period.
snapshots = client.get_snapshots(
    start_date="2022-05-01", end_date="2022-06-01"
)

# Make sure to access the desired user from snapshots
norm_acr = pulse.compute_acr(snapshots[client.user_id])

# Compute ACR using unnormalized values
acr = pulse.compute_acr(snapshots[client.user_id], normalized=False)
```

Acute/chronic workload ratio is the quotient of acute workload and chronic workload over a 28-day period.

## Additional Resources

You can learn more about Pulse and throwing workload at the following links:

- [Using Pulse to Define Throwing Workload](https://www.drivelinebaseball.com/2020/04/what-is-throwing-workload/)
- [Optimized Acute Workload Computation for Baseball Pitchers](https://www.researchgate.net/publication/336345883_OPTIMIZED_ACUTE_WORKLOAD_COMPUTATION_FOR_BASEBALL_PITCHERS_COUPLED_9-DAY_EXPONENTIALLY_WEIGHTED_AVERAGES_WITH_DYNAMIC_DIVISORS)
