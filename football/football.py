import json
import os
import re
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
        self.headers = {
            "X-Auth-Token": self.api_key
        }

    def competitions(self, season=""):
        """
        Returns a dictionary containing all the competitions available.
        """
        # Error checking for query parameter season
        if season:
            season = str(season)
            pattern = re.compile(r"\d\d\d\d")
            if not pattern.match(season):
                raise ValueError("season is invalid.")

        # Generate URL and return
        url = self._generate_url("competitions", {"season": season})
        competitions = requests.get(url, headers=self.headers).json()
        return competitions

    def teams(self, competition_id):
        """
        Returns a dictionary containing a list with all the teams in the given
        competition.
        """
        # Allow users to use both id or name
        if isinstance(competition_id, str):
            try:
                competition_id = LEAGUE_CODE[competition_id]
            except Exception as error:
                return error

        # Generate URL and return
        url = self._generate_url(f"competitions/{competition_id}/teams")
        teams = requests.get(url, headers=self.headers).json()
        return teams

    def table(self, competition_id, matchday=""):
        """
        Returns a dictionary containing a list with the competition's league
        table, sorted first to last.
        """
        # Allow users to use both id or name
        if isinstance(competition_id, str):
            try:
                competition_id = LEAGUE_CODE[competition_id]
            except Exception as error:
                return error
        # Error checking for query parameter matchday
        if matchday:
            matchday = str(matchday)
            pattern = re.compile(r"\d+")
            if not pattern.match(matchday):
                raise ValueError("matchday is invalid.")
        # Generate URL and return
        url = self._generate_url(
            f"competitions/{competition_id}/leagueTable",
            {"matchday": matchday})
        table = requests.get(url, headers=self.headers).json()
        return table

    def competition_fixtures(self, competition_id, matchday="", time_frame=""):
        """
        Returns a dictionary containing a list with all the fixtures in the
        given competition.
        """
        # Allow users to use both id or name
        if isinstance(competition_id, str):
            try:
                competition_id = LEAGUE_CODE[competition_id]
            except Exception as error:
                return error

        # Error checking for query parameter matchday
        if matchday:
            matchday = str(matchday)
            pattern = re.compile(r"\d+")
            if not pattern.match(matchday):
                raise ValueError("matchday is invalid.")

        # Error checking for query parameter time_frame
        if time_frame:
            time_frame = str(time_frame)
            pattern = re.compile(r"p|n[1-9]{1,2}")
            if not pattern.match(time_frame):
                raise ValueError("time_frame is invalid.")

        url = self._generate_url(
            f"competitions/{competition_id}/fixtures",
            {"matchday": matchday, "timeFrame": time_frame})
        fixtures = requests.get(url, headers=self.headers).json()
        return fixtures

    def fixtures(self, time_frame="", league_code=""):
        """
        Returns a dictionary containing a list with all the fixtures across
        all competitions.
        """
        # Error checking for query parameter time_frame
        if time_frame:
            time_frame = str(time_frame)
            pattern = re.compile(r"p|n[1-9]{1,2}")
            if not pattern.match(time_frame):
                raise ValueError("time_frame is invalid.")

        # Error checking for query parameter league_code
        if league_code:
            if league_code not in LEAGUE_CODE.keys():
                raise ValueError("league_code is invalid.")

        url = self._generate_url(
            "fixtures", {"timeFrame": time_frame, "league": league_code})
        fixtures = requests.get(url, headers=self.headers).json()
        return fixtures

    def fixture(self, fixture_id):
        """
        Returns a dictionary containing the fixture with the given id.
        """
        url = self._generate_url(f"fixtures/{fixture_id}")
        fixture = requests.get(url, headers=self.headers).json()
        return fixture

    def team_fixtures(self, team_id, season="", time_frame="", venue=""):
        """
        Returns a dictionary containing a list with all the fixtures of the
        team with the given id.
        """
        # Error checking for query parameter season
        if season:
            season = str(season)
            pattern = re.compile(r"\d\d\d\d")
            if not pattern.match(season):
                raise ValueError("season is invalid.")

        # Error checking for query parameter time_frame
        if time_frame:
            time_frame = str(time_frame)
            pattern = re.compile(r"p|n[1-9]{1,2}")
            if not pattern.match(time_frame):
                raise ValueError("time_frame is invalid.")

        # Error checking for query parameter venue
        if venue:
            if venue not in ("home", "away"):
                raise ValueError("venue is invalid.")

        url = self._generate_url(
            f"teams/{team_id}/fixtures",
            {"season": season, "timeFrame": time_frame, "venue": venue})
        fixtures = requests.get(url, headers=self.headers).json()
        return fixtures

    def team(self, team_id):
        """
        Returns a dictionary containing the team's name, code, short name,
        squad market value and crest.
        """
        url = self._generate_url(f"teams/{team_id}")
        team = requests.get(url, headers=self.headers).json()
        return team

    def players(self, team_id):
        """
        Returns a dictionary containing a list of dictionaries of the team's
        players. These dictionaries contain the player's name, position,
        contract expiration date and market value.
        """
        url = self._generate_url(f"teams/{team_id}/players")
        players = requests.get(url, headers=self.headers).json()
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
