# Pulse Throw for Python <!-- omit in toc -->

Tools for acquiring and analyzing Pulse API data.

[Pulse](https://www.drivelinebaseball.com/pulse/) is a wearable sensor for baseball players to monitor throwing workload.

## Contents <!-- omit in toc -->

- [Installation](#installation)
- [Getting Started](#getting-started)
- [API Requests](#api-requests)
  - [Get Profile](#get-profile)
  - [Get Team](#get-team)
  - [Get Snapshots](#get-snapshots)
  - [Get Events](#get-events)
- [Usage With DataFrame](#usage-with-dataframe)
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

The `pulse_throw` module can be installed via pip:

`pip install pulse-throw`

## Getting Started

In order to use the Pulse client, you must have a `client_id`, `client_secret`, and `refresh_token` provided by the Pulse team at Driveline.

It is best practice to store these values in a `.env` file:

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
import pulse_throw as pt

# Using a traditional constructor and destructor
client = pt.PulseClient(client_id, client_secret, refresh_token)

...

del client

# Using a context manager that destructs automatically
with pt.PulseClient(client_id, client_secret, refresh_token) as client:
    ...
```

The Pulse client will authenticate the client upon construction by default. This involves fetching an access token from the API. If you don't want this request to happen automatically, pass `authenticate=False` into the object constructor. In order to make other requests, you will need to manually call the `authenticate()` method so that the other requests have the proper authorization headers:

```python
client = pt.PulseClient(
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

```python
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

```python
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
    ]
}
```

### Get Snapshots

Gets daily snapshots generated for one or more users over a range of dates. The owner of the session must have permission to access their data (e.g. the requested users must be either the current user or a member of a team for which the current user is a coach).

**Method**: `get_snapshots(start_date: str = <end_date - 8 days>, end_date: str = <today's date>, user_ids: str | list[str] = <user_id>)`

**Payload**:

- `startDate`: The earliest date for which to get data, pulled from the `start_date` parameter. Expected in ISO 8601 format (YYYY-MM-DD). Defaults to eight days before the `end_date` parameter.
- `endDate`: The latest date for which to get data, pulled from the `end_date` parameter. Expected in ISO 8601 format (YYYY-MM-DD). Defaults to today's date.
- `pulseUserIds`: User IDs for whom to get data, pulled from the `user_ids` parameter. IDs must belong to the owner of the session or a member of their team. Defaults to the ID of the owner of the session.

**Example Response**:

```python
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
    ]
}
```

### Get Events

Gets all of the individual throw events for one or more users over a range of dates. The owner of the session must have permission to access their data (e.g. the requested users must be either the current user or a member of a team for which the current user is a coach).

**Method**: `get_events(start_date: str = <end_date - 8 days>, end_date: str = <today's date>, user_ids: str | list[str] = <user_id>)`

**Payload**:

- `startDate`: The earliest date for which to get data, pulled from the `start_date` parameter. Expected in ISO 8601 format (YYYY-MM-DD). Defaults to eight days before the `end_date` parameter.
- `endDate`: The latest date for which to get data, pulled from the `end_date` parameter. Expected in ISO 8601 format (YYYY-MM-DD). Defaults to today's date.
- `pulseUserIds`: User IDs for whom to get data, pulled from the `user_ids` parameter. IDs must belong to the owner of the session or a member of their team. Defaults to the ID of the owner of the session.

**Example Response**:

```python
{
    "<id>": [
        {
            "eventId": "POC6TE5b8V",
            "scaler": None,
            "datetime": "2021-03-01T15:49:55.000Z",
            "tag": None,
            "armSlot": 59.782794823856534,
            "armSpeed": 452.4706718068326,
            "shoulderRotation": 155.58127276383868,
            "torque": 34.744537353515625,
            "ballVelocity": None,
            "highEffort": False,
            "ballWeight (oz)": 5.11472,
            "preferredBallWeightUnit": "OZ",
            "simulated": None,
            "workload": 100.728515625,
            "normalizedWorkload": 0.10925094783306122
        },
        ...
    ]
}
```

## Usage With DataFrame

Using Pulse API data with a Pandas DataFrame is very straightforward:

```python
>>> snapshots = client.get_snapshots()
>>> pd.DataFrame(snapshots[client.user_id])

         date  throwCount  highEffortThrowCount  acuteWorkload  \
0  2022-08-25          31                    20   11952.933733
1  2022-08-26          72                    48   12251.629390
2  2022-08-27          56                    18   11249.457626
3  2022-08-28         176                   145   13241.571388
4  2022-08-29           0                     0   12132.189473
5  2022-08-30          62                    20   11572.645582
6  2022-08-31          65                    36   12075.297746
7  2022-09-01          49                    15    9738.659914
8  2022-09-02           0                     0    8390.232797

   chronicWorkload  normAcuteWorkload  normChronicWorkload  workloadRatio  \
0     11246.190459          16.619434            15.636774       1.062843
1     11384.152924          17.034743            15.828598       1.076200
2     11121.532242          15.641317            15.463449       1.011502
3     11650.914981          18.411164            16.199506       1.136526
4     11650.914981          16.868673            16.199506       1.041308
5     11687.992378          16.090679            16.251058       0.990131
6     11562.057889          16.789570            16.075958       1.044390
7     11523.666522          13.540694            16.022579       0.845101
8     10797.709718          11.665833            15.013204       0.777038

   dailyWorkload  normDailyWorkload  \
0    5144.875027           7.153427
1   12124.726038          16.858203
2    6321.565857           8.789497
3   32827.030812          45.642660
4       0.000000           0.000000
5    8166.044329          11.354057
6    9547.085176          13.274255
7    5729.350730           7.966082
8       0.000000           0.000000

                    baseballProjectedOneDayWorkloads
0  [24.089221616656328, 16.56913593881418, 37.272...
1  [29.527065038098115, 40.09697202261785, 0, 25....
2  [50.66824711842194, 0, 26.841686804976792, 37....
3  [0, 30, 70, 0, 25.73377540372583, 11.208688593...
4  [30, 38.04141022232487, 0, 29.14158049224935, ...
5  [38.04141022232487, 0, 30, 30, 15.565793655546...
6  [0, 30, 30, 30, 0, 30, 30, 0, 26.2226596467895...
7  [30, 30, 19.098921681830898, 0, 30, 30, 0, 27....
8  [30, 30, 0, 30, 30, 0, 30, 18.888786678880873,...

[9 rows x 11 columns]

>>> events = client.get_events()
>>> pd.DataFrame(events[client.user_id])

        eventId scaler                  datetime   tag    armSlot    armSpeed  \
0    xNNOY5GBCv   None  2022-08-25T18:42:27.000Z  None  39.011018  330.794549
1    53i2oQx53q   None  2022-08-25T18:42:31.000Z  None  29.182062  383.459351
2    TegHm4tdvP   None  2022-08-25T18:42:34.000Z  None  22.965265  351.637081
3    g6eP3tsucf   None  2022-08-25T18:42:37.000Z  None  23.100885  422.844626
4    57SCmdrwPQ   None  2022-08-25T18:42:40.000Z  None  27.501726  399.794249
..          ...    ...                       ...   ...        ...         ...
506  GeXBh31fBE   None  2022-09-01T18:50:04.000Z  None   0.100000  907.755746
507  nAtPE2rIFs   None  2022-09-01T18:50:12.000Z  None   9.234862  381.136577
508  mCZZxMKin4   None  2022-09-01T18:50:17.000Z  None  26.717210  244.712983
509  JqIj8m5NLE   None  2022-09-01T18:50:23.000Z  None  21.914508  255.154921
510  FiwpRgMXEI   None  2022-09-01T18:51:08.000Z  None   0.100000   98.299791

     shoulderRotation     torque ballVelocity  highEffort  ballWeight (oz)  \
0          148.981671  28.648439         None       False          5.11472
1          160.395491  28.523619         None       False          5.11472
2          159.953864  28.265261         None       False          5.11472
3          164.191710  36.169968         None       False          5.11472
4          156.744317  33.482159         None       False          5.11472
..                ...        ...          ...         ...              ...
506        180.999999  59.939060         None        True          5.11472
507        170.765138  26.342402         None       False          5.11472
508        160.575152  13.585204         None       False          5.11472
509        158.549454  15.364590         None       False          5.11472
510        178.999997   2.170652         None       False          5.11472

    preferredBallWeightUnit  simulated    workload  normalizedWorkload
0                        OZ      False   78.384682            0.108986
1                        OZ      False   77.940994            0.108369
2                        OZ      False   77.024490            0.107095
3                        OZ      False  106.133499            0.147568
4                        OZ      False   95.996948            0.133474
..                      ...        ...         ...                 ...
506                      OZ      False  204.655212            0.284552
507                      OZ      False   70.283264            0.097722
508                      OZ      False   29.715700            0.041317
509                      OZ      False   34.872028            0.048486
510                      OZ      False    2.738843            0.003808

[511 rows x 15 columns]
```


## Data Filtering Functions

The `pulse_throw` module contains functions that can filter event data based on certain characteristics.

### Filter By Tag

Filter throw events by tag or tags.

**Function**: `filter_by_tag(events: list[dict[str, Any]], tags: str | list[str], blacklist: bool = False)`

```python
# Get all throw events from a single date
events = client.get_events(
    start_date="2022-05-01", end_date="2022-05-01"
)

# Get all throw events marked with the desired tag
pre_game = pt.filter_by_tag(
    events[client.user_id], tags="Pre-Game"
)

# Get all throw events marked with one of multiple tags
non_game = pt.filter_by_tag(
    events[client.user_id], tags=["Pre-Game", "Plyo", "Warmup"]
)

# Get all throw events without the desired tag
non_plyos = pt.filter_by_tag(
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
non_simulated = pt.filter_simulated(events[client.user_id])

# Get all throw events that are simulated
simulated = pt.filter_simulated(
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
high_effort = pt.filter_high_effort(events[client.user_id])

# Get all throw events that are not high effort
low_effort = pt.filter_high_effort(
    events[client.user_id], get_high_effort=False
)
```

## Workload Functions

The `pulse_throw` module contains functions that are useful when manually performing workload calculations.

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
norm_workload = pt.sum_workload(events[client.user_id])

# Compute sum using unnormalized values
workload = pt.sum_workload(
    events[client.user_id], normalized=False
)
```

This function can be useful for summing the workload of throws with a certain tag:

```python
pre_game = pt.filter_by_tag(events, tag="Pre-Game")

pre_game_workload = pt.sum_workload(pre_game)
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
norm_acute_workload = pt.compute_acute_workload(
    snapshots[client.user_id]
)

# Compute acute workload using unnormalized values
acute_workload = pt.compute_acute_workload(
    snapshots[client.user_id], normalized=False
)
```

Acute workload is the weighted average of one-day workloads over a 9-day period. The weights for the nine days are defined by `pt.ACUTE_WEIGHTS`:

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
norm_chronic_workload = pt.compute_chronic_workload(
    snapshots[client.user_id]
)

# Compute acute workload using unnormalized values
chronic_workload = pt.compute_chronic_workload(
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
norm_acr = pt.compute_acr(snapshots[client.user_id])

# Compute ACR using unnormalized values
acr = pt.compute_acr(snapshots[client.user_id], normalized=False)
```

Acute/chronic workload ratio is the quotient of acute workload and chronic workload over a 28-day period.

## Additional Resources

You can learn more about Pulse and throwing workload at the following links:

- [Using Pulse to Define Throwing Workload](https://www.drivelinebaseball.com/2020/04/what-is-throwing-workload/)
- [Optimized Acute Workload Computation for Baseball Pitchers](https://www.researchgate.net/publication/336345883_OPTIMIZED_ACUTE_WORKLOAD_COMPUTATION_FOR_BASEBALL_PITCHERS_COUPLED_9-DAY_EXPONENTIALLY_WEIGHTED_AVERAGES_WITH_DYNAMIC_DIVISORS)
