import json
import requests
import urllib.parse

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
        """
        Returns a dictionary containing all the competitions available.
        """
        competitions = requests.get(f"{self.API_URL}competitions/").json()
        return competitions

    def teams(self, competition_id):
        """
        Returns a dictionary containing a list with all the teams in the given
        competition.
        """
        if isinstance(competition_id, str):
            try:
                competition_id = LEAGUE_CODE[competition_id]
            except Exception as error:
                return error
        teams = requests.get(
            f"{self.API_URL}competitions/{competition_id}/teams").json()
        return teams

    def table(self, competition_id):
        """
        Returns a dictionary containing a list with the competition's league
        table, sorted first to last.
        """
        if isinstance(competition_id, str):
            try:
                competition_id = LEAGUE_CODE[competition_id]
            except Exception as error:
                return error
        table = requests.get(
            f"{self.API_URL}competitions/{competition_id}/leagueTable").json()
        return table

    def competition_fixtures(self, competition_id):
        """
        Returns a dictionary containing a list with all the fixtures in the
        given competition.
        """
        if isinstance(competition_id, str):
            try:
                competition_id = LEAGUE_CODE[competition_id]
            except Exception as error:
                return error
        fixtures = requests.get(
            f"{self.API_URL}competitions/{competition_id}/fixtures").json()
        return fixtures

    def fixtures(self):
        """
        Returns a dictionary containing a list with all the fixtures across
        all competitions.
        """
        fixtures = requests.get(f"{self.API_URL}fixtures/").json()
        return fixtures

    def fixture(self, fixture_id):
        """
        Returns a dictionary containing the fixture with the given id.
        """
        fixture = requests.get(f"{self.API_URL}fixtures/{fixture_id}").json()
        return fixture

    def team_fixtures(self, team_id):
        """
        Returns a dictionary containing a list with all the fixtures of the
        team with the given id.
        """
        fixtures = requests.get(
            f"{self.API_URL}teams/{team_id}/fixtures").json()
        return fixtures

    def team(self, team_id):
        """
        Returns a dictionary containing the team's name, code, short name,
        squad market value and crest.
        """
        team = requests.get(f"{self.API_URL}teams/{team_id}").json()
        return team

    def players(self, team_id):
        """
        Returns a dictionary containing a list of dictionaries of the team's
        players. These dictionaries contain the player's name, position,
        contract expiration date and market value.
        """
        players = requests.get(f"{self.API_URL}teams/{team_id}/players").json()
        return players

    def _generate_url(self, action, query_params=None):
        """
        Generates a URL for the given action, with optional query parameters
        that can be used to filter the response.
        """
        if action == "competitions" or action == "fixtures":
            action += "/"

        if query_params:
            query_params = urllib.parse.urlencode(query_params)
            action = f"{action}?{query_params}"

        url = urllib.parse.urljoin(self.API_URL, action)
        return url
