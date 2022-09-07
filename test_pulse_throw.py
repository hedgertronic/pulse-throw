import os
from datetime import date, timedelta

import pytest
from authlib.integrations.base_client.errors import MissingTokenError
from dotenv import load_dotenv

import pulse_throw as pt


load_dotenv()

client_id = os.getenv("CLIENT_ID") or ""
client_secret = os.getenv("CLIENT_SECRET") or ""
refresh_token = os.getenv("REFRESH_TOKEN") or ""


########################################################################################
# FIXTURES


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["authorization"],
        "filter_post_data_parameters": ["client_id", "client_secret", "refresh_token"],
    }


@pytest.fixture
def client():
    return pt.PulseClient(client_id, client_secret, refresh_token, authenticate=False)


# @pytest.mark.vcr
@pytest.fixture
def auth_client():
    return pt.PulseClient(client_id, client_secret, refresh_token)


@pytest.fixture
def sample_team_data():
    return {
        "team": {"name": "TEAMNAME", "id": "JQtyNOYdDH"},
        "members": [
            {
                "userId": "r5FiwuBlYZ",
                "teamMemberId": "yvUsIxsjrg",
                "athleteProfileId": "dgTHp0nlN0",
                "firstName": "<player-first-name>",
                "lastName": "<player-last-name>",
                "email": "<player-email>",
            }
        ],
    }


@pytest.fixture
def sample_snapshot_data():
    return [
        {
            "date": "2022-06-01",
            "dailyWorkload": 18113.604788780212,
            "normDailyWorkload": 25.18513187021017,
        },
        {
            "date": "2022-06-02",
            "dailyWorkload": 7348.9012451171875,
            "normDailyWorkload": 10.217902589589357,
        },
        {
            "date": "2022-06-03",
            "dailyWorkload": 12723.611276626587,
            "normDailyWorkload": 17.690892127342522,
        },
    ]


@pytest.fixture
def sample_event_data():
    return [
        {
            "tag": "Pre-Game",
            "highEffort": False,
            "simulated": False,
            "workload": 8.588786125183105,
            "normalizedWorkload": 0.011941837146878242,
        },
        {
            "tag": "Plyo",
            "highEffort": True,
            "simulated": True,
            "workload": 117.60966491699219,
            "normalizedWorkload": 0.163524329662323,
        },
        {
            "tag": None,
            "highEffort": True,
            "simulated": False,
            "workload": 121.55718994140625,
            "normalizedWorkload": 0.16901294887065887,
        },
    ]


@pytest.fixture
def sample_workload_data():
    return [
        {
            "date": "2022-04-01",
            "acuteWorkload": 9769.022346690714,
            "chronicWorkload": 10026.405936064493,
            "normAcuteWorkload": 13.58291028054794,
            "normChronicWorkload": 13.94077804643894,
            "workloadRatio": 0.9743294266145774,
            "dailyWorkload": 5688.352069854736,
            "normDailyWorkload": 7.9090772196650505,
        },
        {
            "date": "2022-04-02",
            "acuteWorkload": 10325.500974344754,
            "chronicWorkload": 10177.924288214426,
            "normAcuteWorkload": 14.35664167394861,
            "normChronicWorkload": 14.15145011883994,
            "workloadRatio": 1.014499684017223,
            "dailyWorkload": 12706.15563583374,
            "normDailyWorkload": 17.66662183776498,
        },
        {
            "date": "2022-04-03",
            "acuteWorkload": 7979.457436662022,
            "chronicWorkload": 9595.381489363837,
            "normAcuteWorkload": 11.094687943502024,
            "normChronicWorkload": 13.341478937430239,
            "workloadRatio": 0.8315935583704501,
            "dailyWorkload": 0,
            "normDailyWorkload": 0,
        },
        {
            "date": "2022-04-04",
            "acuteWorkload": 9236.96285098243,
            "chronicWorkload": 9860.420623440632,
            "normAcuteWorkload": 12.843131402207334,
            "normChronicWorkload": 13.709991020957075,
            "workloadRatio": 0.9367716858877106,
            "dailyWorkload": 15147.249799728394,
            "normDailyWorkload": 21.060715950094163,
        },
        {
            "date": "2022-04-05",
            "acuteWorkload": 9730.614461372823,
            "chronicWorkload": 9994.793104155708,
            "normAcuteWorkload": 13.529507714577234,
            "normChronicWorkload": 13.896823365582208,
            "workloadRatio": 0.9735683730488586,
            "dailyWorkload": 11512.759433746338,
            "normDailyWorkload": 16.007325431331992,
        },
        {
            "date": "2022-04-06",
            "acuteWorkload": 8931.51797996112,
            "chronicWorkload": 9583.81069941426,
            "normAcuteWorkload": 12.418438927208397,
            "normChronicWorkload": 13.325390838111538,
            "workloadRatio": 0.9319380630615954,
            "dailyWorkload": 5912.964567422867,
            "normDailyWorkload": 8.221378200221807,
        },
        {
            "date": "2022-04-07",
            "acuteWorkload": 8749.548213927625,
            "chronicWorkload": 9563.768104249153,
            "normAcuteWorkload": 12.165427016897581,
            "normChronicWorkload": 13.297523487392537,
            "workloadRatio": 0.9148641119853405,
            "dailyWorkload": 5039.746336936951,
            "normDailyWorkload": 7.0072567539755255,
        },
        {
            "date": "2022-04-08",
            "acuteWorkload": 7331.461109998418,
            "chronicWorkload": 9428.308313331167,
            "normAcuteWorkload": 10.193709764229256,
            "normChronicWorkload": 13.109179339804003,
            "workloadRatio": 0.7776009084929998,
            "dailyWorkload": 7164.87233543396,
            "normDailyWorkload": 9.96202889084816,
        },
        {
            "date": "2022-04-09",
            "acuteWorkload": 9852.207222752675,
            "chronicWorkload": 9917.245579437607,
            "normAcuteWorkload": 13.698571056841576,
            "normChronicWorkload": 13.789000798149823,
            "workloadRatio": 0.9934418930978393,
            "dailyWorkload": 21837.042689085007,
            "normDailyWorkload": 30.362195095978677,
        },
        {
            "date": "2022-04-10",
            "acuteWorkload": 9210.672000597384,
            "chronicWorkload": 9976.051151049427,
            "normAcuteWorkload": 12.80657643802503,
            "normChronicWorkload": 13.87076443578448,
            "workloadRatio": 0.9232783454231256,
            "dailyWorkload": 3197.7362327575684,
            "normDailyWorkload": 4.446128189563751,
        },
        {
            "date": "2022-04-11",
            "acuteWorkload": 7640.654314958832,
            "chronicWorkload": 9264.735211210285,
            "normAcuteWorkload": 10.623613946376517,
            "normChronicWorkload": 12.881746267018427,
            "workloadRatio": 0.8247029343821589,
            "dailyWorkload": 0,
            "normDailyWorkload": 0,
        },
        {
            "date": "2022-04-12",
            "acuteWorkload": 10013.581635744167,
            "chronicWorkload": 9721.747565212716,
            "normAcuteWorkload": 13.92294705839531,
            "normChronicWorkload": 13.517179126235897,
            "workloadRatio": 1.03001868425135,
            "dailyWorkload": 20455.685294628143,
            "normDailyWorkload": 28.44155780505389,
        },
        {
            "date": "2022-04-13",
            "acuteWorkload": 9107.730440447824,
            "chronicWorkload": 9726.029379553673,
            "normAcuteWorkload": 12.663445843577698,
            "normChronicWorkload": 13.523132587899426,
            "workloadRatio": 0.9364284318937329,
            "dailyWorkload": 6218.792235374451,
            "normDailyWorkload": 8.646600391715765,
        },
        {
            "date": "2022-04-14",
            "acuteWorkload": 8380.726858319593,
            "chronicWorkload": 9038.373215736996,
            "normAcuteWorkload": 11.652615478036582,
            "normChronicWorkload": 12.567011120928703,
            "workloadRatio": 0.9272384153962182,
            "dailyWorkload": 5194.520327806473,
            "normDailyWorkload": 7.2224541627801955,
        },
        {
            "date": "2022-04-15",
            "acuteWorkload": 8534.72552121745,
            "chronicWorkload": 9141.692885092649,
            "normAcuteWorkload": 11.866736190143921,
            "normChronicWorkload": 12.710667440800783,
            "workloadRatio": 0.9336044897258603,
            "dailyWorkload": 8237.077334880829,
            "normDailyWorkload": 11.452821342973039,
        },
        {
            "date": "2022-04-16",
            "acuteWorkload": 8420.235936158075,
            "chronicWorkload": 9035.608050274644,
            "normAcuteWorkload": 11.707549149032745,
            "normChronicWorkload": 12.563166417430944,
            "workloadRatio": 0.931894775570985,
            "dailyWorkload": 6092.569334983826,
            "normDailyWorkload": 8.471100229769945,
        },
        {
            "date": "2022-04-17",
            "acuteWorkload": 10005.906194969622,
            "chronicWorkload": 9712.225984205748,
            "normAcuteWorkload": 13.91227507713614,
            "normChronicWorkload": 13.503940259954623,
            "workloadRatio": 1.0302381978386277,
            "dailyWorkload": 18945.406072616577,
            "normDailyWorkload": 26.341667590662837,
        },
        {
            "date": "2022-04-18",
            "acuteWorkload": 7979.524477446772,
            "chronicWorkload": 9439.300918875415,
            "normAcuteWorkload": 11.094781157431942,
            "normChronicWorkload": 13.124463527879135,
            "workloadRatio": 0.8453512125554147,
            "dailyWorkload": 1672.3294219970703,
            "normDailyWorkload": 2.3252046294510365,
        },
        {
            "date": "2022-04-19",
            "acuteWorkload": 8196.435556636983,
            "chronicWorkload": 9057.335335852069,
            "normAcuteWorkload": 11.396375689918147,
            "normChronicWorkload": 12.593376172323968,
            "workloadRatio": 0.9049499938676947,
            "dailyWorkload": 7078.349512696266,
            "normDailyWorkload": 9.841727681923658,
        },
        {
            "date": "2022-04-20",
            "acuteWorkload": 10737.936006029575,
            "chronicWorkload": 9593.310916492095,
            "normAcuteWorkload": 14.930093943082541,
            "normChronicWorkload": 13.338599999851011,
            "workloadRatio": 1.119314916351739,
            "dailyWorkload": 21858.257093429565,
            "normDailyWorkload": 30.391691781580448,
        },
        {
            "date": "2022-04-21",
            "acuteWorkload": 9445.811285348613,
            "chronicWorkload": 9551.839701947065,
            "normAcuteWorkload": 13.133515582482007,
            "normChronicWorkload": 13.280938161603572,
            "workloadRatio": 0.988899686352898,
            "dailyWorkload": 6413.146989166737,
            "normDailyWorkload": 8.91683100303635,
        },
        {
            "date": "2022-04-22",
            "acuteWorkload": 9390.19576466845,
            "chronicWorkload": 9015.862651601365,
            "normAcuteWorkload": 13.05618741178123,
            "normChronicWorkload": 12.535712290588492,
            "workloadRatio": 1.0415193894952024,
            "dailyWorkload": 7318.835624694824,
            "normDailyWorkload": 10.176099322736263,
        },
        {
            "date": "2022-04-23",
            "acuteWorkload": 9298.124327892334,
            "chronicWorkload": 9087.903492801617,
            "normAcuteWorkload": 12.928170705426293,
            "normChronicWorkload": 12.635878330528987,
            "workloadRatio": 1.0231319396445209,
            "dailyWorkload": 6637.472747802734,
            "normDailyWorkload": 9.228733327239752,
        },
        {
            "date": "2022-04-24",
            "acuteWorkload": 9217.966913020973,
            "chronicWorkload": 9140.369929652124,
            "normAcuteWorkload": 12.816719330265176,
            "normChronicWorkload": 12.708827995212873,
            "workloadRatio": 1.0084894795250154,
            "dailyWorkload": 8265.969958603382,
            "normDailyWorkload": 11.49299363931641,
        },
        {
            "date": "2022-04-25",
            "acuteWorkload": 9290.994089943375,
            "chronicWorkload": 8965.300804817922,
            "normAcuteWorkload": 12.918256777614216,
            "normChronicWorkload": 12.465410779945417,
            "workloadRatio": 1.0363282049555356,
            "dailyWorkload": 8297.137899398804,
            "normDailyWorkload": 11.536329507827759,
        },
        {
            "date": "2022-04-26",
            "acuteWorkload": 9900.406866261912,
            "chronicWorkload": 9499.103695570375,
            "normAcuteWorkload": 13.76558814515463,
            "normChronicWorkload": 13.207613685750403,
            "workloadRatio": 1.042246424878873,
            "dailyWorkload": 18317.032143354416,
            "normDailyWorkload": 25.467977260239422,
        },
        {
            "date": "2022-04-27",
            "acuteWorkload": 9898.263251602619,
            "chronicWorkload": 8797.390969861308,
            "normAcuteWorkload": 13.762607649813344,
            "normChronicWorkload": 12.231947886474822,
            "workloadRatio": 1.1251362233999551,
            "dailyWorkload": 5742.540998458862,
            "normDailyWorkload": 7.984421189874411,
        },
        {
            "date": "2022-04-28",
            "acuteWorkload": 9572.86638794277,
            "chronicWorkload": 8974.611133160417,
            "normAcuteWorkload": 13.310173798419742,
            "normChronicWorkload": 12.478355919189712,
            "workloadRatio": 1.0666608553736496,
            "dailyWorkload": 6338.489402413368,
            "normDailyWorkload": 8.813027301686816,
        },
        {
            "date": "2022-04-29",
            "acuteWorkload": 8028.766383598599,
            "chronicWorkload": 8948.752562972028,
            "normAcuteWorkload": 11.163247414296427,
            "normChronicWorkload": 12.442402000119078,
            "workloadRatio": 0.8971939191636463,
            "dailyWorkload": 4964.308172225952,
            "normDailyWorkload": 6.902367485687137,
        },
        {
            "date": "2022-04-30",
            "acuteWorkload": 10074.395739401238,
            "chronicWorkload": 9259.825028807387,
            "normAcuteWorkload": 14.007503371652772,
            "normChronicWorkload": 12.874919118438683,
            "workloadRatio": 1.0879682616096649,
            "dailyWorkload": 21416.232349395752,
            "normDailyWorkload": 29.77710115071386,
        },
    ]


########################################################################################
# PULSE CLIENT TESTS


class TestPulseClient:
    def test_context_manager(self):
        with pt.PulseClient(
            client_id, client_secret, refresh_token, authenticate=False
        ) as client:
            assert not client.is_authenticated()
            assert not client.session.token

            assert not client.user_id
            assert str(client) == "PulseClient(<Unauthenticated>)"

    def test_unauthenticated_client(self, client: pt.PulseClient):
        assert not client.is_authenticated()
        assert not client.session.token

        assert not client.user_id
        assert str(client) == "PulseClient(<Unauthenticated>)"

    @pytest.mark.vcr
    def test_authenticate(self, client: pt.PulseClient):
        client.authenticate()

        assert client.is_authenticated()
        assert client.session.token

        assert client.user_id
        assert str(client) == f"PulseClient({client.user_id})"

    @pytest.mark.vcr
    def test_authenticated_client(self, auth_client: pt.PulseClient):
        assert auth_client.is_authenticated()
        assert auth_client.session.token

        assert auth_client.user_id
        assert str(auth_client) == f"PulseClient({auth_client.user_id})"

    @pytest.mark.vcr
    def test_refresh_token(self, auth_client: pt.PulseClient):
        auth_client.session.refresh_token(f"{auth_client.API_URL}/oauth/token")

        assert auth_client.is_authenticated()
        assert auth_client.session.token

    ####################################################################################
    # API ENDPOINT TESTS

    def test_unauthenticated_request(self, client: pt.PulseClient):
        with pytest.raises(MissingTokenError):
            client.get_profile()

    @pytest.mark.vcr
    def test_get_profile(self, auth_client: pt.PulseClient):
        profile = auth_client.get_profile()

        assert isinstance(profile, dict)

        assert isinstance(profile.get("id"), str)
        assert isinstance(profile.get("firstName"), str)
        assert isinstance(profile.get("lastName"), str)
        assert isinstance(profile.get("email"), str)

        assert profile["id"] == auth_client.user_id

    @pytest.mark.vcr
    def test_get_team(self, auth_client: pt.PulseClient):
        team = auth_client.get_team()

        assert isinstance(team, dict)

    def test_get_team_from_sample(self, sample_team_data):
        assert isinstance(sample_team_data, dict)

        assert (team_data := sample_team_data.get("team")) is not None
        assert (member_data := sample_team_data.get("members")) is not None

        assert isinstance(team_data, dict)
        assert isinstance(team_data.get("name"), str)
        assert isinstance(team_data.get("id"), str)

        assert isinstance(member_data, list)
        assert isinstance(member := member_data[0], dict)

        assert isinstance(member.get("userId"), str)
        assert isinstance(member.get("teamMemberId"), str)
        assert isinstance(member.get("athleteProfileId"), str)
        assert isinstance(member.get("firstName"), str)
        assert isinstance(member.get("lastName"), str)
        assert isinstance(member.get("email"), str)

    @pytest.mark.vcr
    def test_get_snapshots(self, auth_client: pt.PulseClient):
        snapshots = auth_client.get_snapshots(end_date="2022-08-22")

        assert isinstance(snapshots, dict)

        assert (user_snapshots := snapshots.get(auth_client.user_id)) is not None

        assert isinstance(user_snapshots, list)
        assert isinstance(data := user_snapshots[0], dict)

        assert isinstance(data.get("throwCount"), int)
        assert isinstance(data.get("date"), str)
        assert isinstance(data.get("highEffortThrowCount"), int)
        assert isinstance(data.get("acuteWorkload"), float)
        assert isinstance(data.get("chronicWorkload"), float)
        assert isinstance(data.get("normAcuteWorkload"), float)
        assert isinstance(data.get("normChronicWorkload"), float)
        assert isinstance(data.get("workloadRatio"), float)
        assert isinstance(data.get("dailyWorkload"), float)
        assert isinstance(data.get("normDailyWorkload"), float)

        proj_workloads = data.get("baseballProjectedOneDayWorkloads")

        assert isinstance(proj_workloads, list)

        for item in proj_workloads:
            assert isinstance(item, int | float)

    @pytest.mark.vcr
    def test_get_events(self, auth_client: pt.PulseClient):
        events = auth_client.get_events()

        assert isinstance(events, dict)

        assert (user_events := events.get(auth_client.user_id)) is not None

        assert isinstance(user_events, list)
        assert isinstance(data := user_events[0], dict)

        assert isinstance(data.get("eventId"), str)
        assert isinstance(data.get("scaler"), int | float | None)
        assert isinstance(data.get("datetime"), str)
        assert isinstance(data.get("tag"), str | None)
        assert isinstance(data.get("armSlot"), float)
        assert isinstance(data.get("armSpeed"), float)
        assert isinstance(data.get("shoulderRotation"), float)
        assert isinstance(data.get("torque"), float)
        assert isinstance(data.get("ballVelocity"), int | float | None)
        assert isinstance(data.get("ballWeight (oz)"), float)
        assert isinstance(data.get("preferredBallWeightUnit"), str)
        assert isinstance(data.get("simulated"), bool)
        assert isinstance(data.get("workload"), float)
        assert isinstance(data.get("normalizedWorkload"), float)

    ####################################################################################
    # API HELPER METHOD TESTS

    def test_format_user_ids(self, auth_client: pt.PulseClient):
        test_id = "abc123"
        test_list = ["abc123", "def456", "ghi789"]

        assert auth_client._format_user_ids(None) == [auth_client.user_id]
        assert auth_client._format_user_ids(test_id) == [test_id]
        assert auth_client._format_user_ids(test_list) == test_list

    def test_format_user_ids_unauthenticated(self, client: pt.PulseClient):
        assert client._format_user_ids(None) == [client.user_id]

    def test_format_dates(self, client: pt.PulseClient):
        test_start_date = "2022-05-01"
        test_end_date = "2022-05-10"

        assert client._format_dates(test_start_date, test_end_date) == (
            test_start_date,
            test_end_date,
        )

        assert client._format_dates(start_date=test_start_date, end_date=None) == (
            test_start_date,
            str(date.today()),
        )

        assert client._format_dates(start_date=None, end_date=test_end_date) == (
            str(date.fromisoformat(test_end_date) - timedelta(days=8)),
            test_end_date,
        )

        assert client._format_dates(start_date=None, end_date=None) == (
            str(date.today() - timedelta(days=8)),
            str(date.today()),
        )

    def test_format_dates_bad_dates(self, client: pt.PulseClient):
        test_start_date = "2022-05-01"
        test_end_date = "2022-05-10"

        with pytest.raises(ValueError):
            client._format_dates(test_end_date, test_start_date)


########################################################################################
# FILTER FUNCTION TESTS


def test_filter_by_tag(sample_event_data):
    test_tag = "Pre-Game"
    test_list = ["Pre-Game", "Plyo"]

    tagged = pt.filter_by_tag(sample_event_data, test_tag)
    untagged = pt.filter_by_tag(sample_event_data, test_tag, blacklist=True)

    tagged_list = pt.filter_by_tag(sample_event_data, test_list)
    untagged_list = pt.filter_by_tag(sample_event_data, test_list, blacklist=True)

    assert isinstance(tagged, list)

    for item in tagged:
        assert isinstance(item, dict)
        assert item.get("tag") == test_tag

    assert isinstance(untagged, list)

    for item in untagged:
        assert isinstance(item, dict)
        assert item.get("tag") != test_tag

    assert isinstance(tagged_list, list)

    for item in tagged_list:
        assert isinstance(item, dict)
        assert item.get("tag") in test_list

    assert isinstance(untagged_list, list)

    for item in untagged_list:
        assert isinstance(item, dict)
        assert item.get("tag") not in test_list


def test_filter_simulated(sample_event_data):
    non_simulated = pt.filter_simulated(sample_event_data)
    simulated = pt.filter_simulated(sample_event_data, get_simulated=True)

    assert isinstance(non_simulated, list)

    for item in non_simulated:
        assert isinstance(item, dict)
        assert item.get("simulated") == False

    assert isinstance(simulated, list)

    for item in simulated:
        assert isinstance(item, dict)
        assert item.get("simulated") == True


def test_filter_high_effort(sample_event_data):
    high_effort = pt.filter_high_effort(sample_event_data)
    low_effort = pt.filter_high_effort(sample_event_data, get_high_effort=False)

    assert isinstance(high_effort, list)

    for item in high_effort:
        assert isinstance(item, dict)
        assert item.get("highEffort") == True

    assert isinstance(low_effort, list)

    for item in low_effort:
        assert isinstance(item, dict)
        assert item.get("highEffort") == False


########################################################################################
# WORKLOAD FUNCTION TESTS


def test_sum_workload(sample_event_data):
    assert pt.sum_workload(sample_event_data) == sum(
        event["normalizedWorkload"] for event in sample_event_data
    )

    assert pt.sum_workload(sample_event_data, normalized=False) == sum(
        event["workload"] for event in sample_event_data
    )


def test_compute_acute_workload(sample_workload_data):
    assert pt.compute_acute_workload(sample_workload_data) == pytest.approx(
        sample_workload_data[-1]["normAcuteWorkload"]
    )

    assert pt.compute_acute_workload(
        sample_workload_data, normalized=False
    ) == pytest.approx(sample_workload_data[-1]["acuteWorkload"], 1)

    assert pt.compute_acute_workload(
        sample_workload_data, end_date="2022-04-29"
    ) == pytest.approx(sample_workload_data[-2]["normAcuteWorkload"])

    assert pt.compute_acute_workload(
        sample_workload_data, end_date="2022-04-29"
    ) == pytest.approx(sample_workload_data[-2]["acuteWorkload"], 1)

    assert pt.compute_acute_workload(sample_workload_data, end_date="2023-04-30") == 0.0


def test_compute_acute_workload_bad_dates(sample_workload_data):
    with pytest.raises(ValueError):
        pt.compute_acute_workload(sample_workload_data, end_date="2021-04-01")


def test_compute_chronic_workload(sample_workload_data):
    assert pt.compute_chronic_workload(sample_workload_data) == pytest.approx(
        sample_workload_data[-1]["normChronicWorkload"]
    )

    assert pt.compute_chronic_workload(
        sample_workload_data, normalized=False
    ) == pytest.approx(sample_workload_data[-1]["chronicWorkload"], 1)

    assert pt.compute_chronic_workload(
        sample_workload_data, end_date="2022-04-29"
    ) == pytest.approx(sample_workload_data[-2]["normChronicWorkload"])

    assert pt.compute_chronic_workload(
        sample_workload_data, end_date="2022-04-29"
    ) == pytest.approx(sample_workload_data[-2]["chronicWorkload"], 1)

    assert (
        pt.compute_chronic_workload(sample_workload_data, end_date="2023-04-30") == 0.0
    )


def test_compute_chronic_workload_bad_dates(sample_workload_data):
    with pytest.raises(ValueError):
        pt.compute_chronic_workload(sample_workload_data, end_date="2021-04-01")


def test_compute_acr(sample_workload_data):
    assert pt.compute_acr(sample_workload_data) == pytest.approx(
        sample_workload_data[-1]["workloadRatio"]
    )

    assert pt.compute_acr(sample_workload_data, normalized=False) == pytest.approx(
        sample_workload_data[-1]["workloadRatio"], 1
    )

    assert pt.compute_acr(sample_workload_data, end_date="2022-04-29") == pytest.approx(
        sample_workload_data[-2]["workloadRatio"]
    )

    assert pt.compute_acr(sample_workload_data, end_date="2022-04-29") == pytest.approx(
        sample_workload_data[-2]["workloadRatio"], 1
    )

    assert pt.compute_acr(sample_workload_data, end_date="2023-04-30") == 0.0


########################################################################################
# WORKLOAD HELPER FUNCTION TESTS


def test_get_workloads_by_date(sample_snapshot_data):
    norm_workloads = pt._get_workloads_by_date(sample_snapshot_data, normalized=True)
    workloads = pt._get_workloads_by_date(sample_snapshot_data, normalized=False)

    assert isinstance(norm_workloads, dict)

    assert list(norm_workloads.keys()) == [
        date.fromisoformat(snapshot["date"]) for snapshot in sample_snapshot_data
    ]

    assert isinstance(workloads, dict)

    assert list(workloads.keys()) == [
        date.fromisoformat(snapshot["date"]) for snapshot in sample_snapshot_data
    ]

    for snapshot in sample_snapshot_data:
        assert (
            snapshot["normDailyWorkload"]
            == norm_workloads[date.fromisoformat(snapshot["date"])]
        )

        assert (
            snapshot["dailyWorkload"] == workloads[date.fromisoformat(snapshot["date"])]
        )


def test_get_acute_divisor():
    assert pt._get_acute_divisor(0) == 3
    assert pt._get_acute_divisor(1) == 4
    assert pt._get_acute_divisor(2) == 5
    assert pt._get_acute_divisor(6) == 9
    assert pt._get_acute_divisor(7) == 9
    assert pt._get_acute_divisor(100) == 9


def test_get_chronic_divisor():
    assert pt._get_chronic_divisor(0) == 5
    assert pt._get_chronic_divisor(1) == 6
    assert pt._get_chronic_divisor(2) == 7
    assert pt._get_chronic_divisor(23) == 28
    assert pt._get_chronic_divisor(24) == 28
    assert pt._get_chronic_divisor(100) == 28
