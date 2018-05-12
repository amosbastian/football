import json
import requests

LEAGUE_CODE = {
    "BSA": 444,
    "PL": 445,
    "ELC": 446,
    "EL1": 447,
    "EL2": 448,
    "DED": 449,
    "FL1": 450,
    "FL2": 451,
    "BL1": 452,
    "BL2": 453,
    "PD": 455,
    "SA": 456,
    "PPL": 457,
    "DFB": 458,
    "SB": 459,
    "CL": 464,
    "AAL": 466
}


class Football(object):
    """
    The Football class.
    """

    API_URL = "http://api.football-data.org/v1/"

    def __init__(self, api_key):
        """
        Initialise a new instance of the Football class.
        """
        self.api_key = api_key

    def competitions(self):
        competitions = requests.get(f"{self.API_URL}competitions/").json()
        return competitions

    def teams(self, competition_id):
        if isinstance(competition_id, str):
            try:
                competition_id = LEAGUE_CODE[competition_id]
            except Exception as error:
                return error
        teams = requests.get(
            f"{self.API_URL}competitions/{competition_id}/teams").json()
        return teams

    def table(self, competition_id):
        if isinstance(competition_id, str):
            try:
                competition_id = LEAGUE_CODE[competition_id]
            except Exception as error:
                return error
        table = requests.get(
            f"{self.API_URL}competitions/{competition_id}/leagueTable").json()
        return table

    def competition_fixtures(self, competition_id):
        if isinstance(competition_id, str):
            try:
                competition_id = LEAGUE_CODE[competition_id]
            except Exception as error:
                return error
        fixtures = requests.get(
            f"{self.API_URL}competitions/{competition_id}/fixtures").json()
        return fixtures

    def fixtures(self):
        fixtures = requests.get(f"{self.API_URL}fixtures/").json()
        return fixtures

    def fixture(self, fixture_id):
        fixture = requests.get(f"{self.API_URL}fixtures/{fixture_id}").json()
        return fixture

    def team_fixtures(self, team_id):
        fixtures = requests.get(
            f"{self.API_URL}teams/{team_id}/fixtures").json()
        return fixtures

    def team(self, team_id):
        team = requests.get(f"{self.API_URL}teams/{team_id}").json()
        return team

    def players(self, team_id):
        players = requests.get(f"{self.API_URL}teams/{team_id}/players").json()
        return players
