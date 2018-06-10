"""
Contains the Football class used to interact with the API.
"""
import os
import re
import requests
import urllib.parse

from .models.competition import Competition
from .models.fixture import Fixture
from .models.player import Player
from .models.table import Table
from .models.team import Team
from .utils import headers
from .constants import LEAGUE_CODE, TEAM_ID


class Football(object):
    """
    The Football class.
    """

    API_URL = "http://api.football-data.org/v1/"

    def __init__(self, api_key=None):
        """
        Initialise a new instance of the Football class.
        """
        if not api_key:
            if "FOOTBALL_API_KEY" in os.environ:
                api_key = os.environ["FOOTBALL_API_KEY"]
            else:
                raise ValueError(
                    "FOOTBALL_API_KEY environment variable not set or no "
                    "API key given.")

        self.api_key = api_key
        self.headers = headers()

    def competitions(self, season=None):
        """
        Returns a list of Competition objects of all the available
        competitions.
        """
        # Error checking for query parameter season
        if season:
            season = str(season)
            pattern = re.compile(r"\d\d\d\d")
            if not pattern.match(season):
                raise ValueError("season is invalid.")
            season = {"season": season}

        url = self._generate_url("competitions", season)
        competitions = requests.get(url, headers=self.headers).json()
        competitions = [Competition(competition)
                        for competition in competitions]

        return competitions

    def competition(self, competition_id, season=None):
        """
        Returns a Competition object of competition with the given id.
        """
        # Error checking for query parameter season
        if season:
            # Do it this way, because API does not support other method
            competitions = self.competitions(season)
            for competition in competitions:
                if competition.id == competition_id:
                    return competition

            raise ValueError("could not find competition.")

        url = self._generate_url(f"competitions/{competition_id}")
        competition = requests.get(url, headers=self.headers).json()
        competition = Competition(competition)

        return competition

    def teams(self, competition):
        """
        Returns a list of Team objects of teams that are playing in the given
        competition.
        """
        # Allow users to use both id or name
        if isinstance(competition, str):
            try:
                competition = LEAGUE_CODE[competition]
            except KeyError as error:
                return error

        url = self._generate_url(f"competitions/{competition}/teams")
        teams = requests.get(url, headers=self.headers).json()

        return [Team(team) for team in teams["teams"]]

    def table(self, competition, matchday=None):
        """
        Returns a Table object made from the table of the given competition.
        """
        # Allow users to use both id or name
        if isinstance(competition, str):
            try:
                competition = LEAGUE_CODE[competition]
            except KeyError as error:
                return error

        # Error checking for query parameter matchday
        if matchday:
            matchday = str(matchday)
            pattern = re.compile(r"\d+")
            if not pattern.match(matchday):
                raise ValueError("matchday is invalid.")
            matchday = {"matchday": matchday}

        url = self._generate_url(
            f"competitions/{competition}/leagueTable", matchday)
        table = requests.get(url, headers=self.headers).json()

        return Table(table)

    def competition_fixtures(self, competition, matchday=None,
                             time_frame=None):
        """
        Returns a list of Fixture objects made from the fixtures of the given
        competition.
        """
        # Allow users to use both id or name
        if isinstance(competition, str):
            try:
                competition = LEAGUE_CODE[competition]
            except KeyError as error:
                return error

        query_params = {}
        # Error checking for query parameter matchday
        if matchday:
            matchday = str(matchday)
            pattern = re.compile(r"\d+")
            if not pattern.match(matchday):
                raise ValueError("matchday is invalid.")
            query_params["matchday"] = matchday

        # Error checking for query parameter time_frame
        if time_frame:
            time_frame = str(time_frame)
            pattern = re.compile(r"p|n[1-9]{1,2}")
            if not pattern.match(time_frame):
                raise ValueError("time_frame is invalid.")
            query_params["timeFrame"] = time_frame

        url = self._generate_url(
            f"competitions/{competition}/fixtures", query_params)
        fixtures = requests.get(url, headers=self.headers).json()

        return [Fixture(fixture) for fixture in fixtures["fixtures"]]

    def fixtures(self, time_frame=None, league_code=None):
        """
        Returns a list of Fixture objects made from the fixtures across either
        all competitions or a specific league.
        """
        query_params = {}
        # Error checking for query parameter time_frame
        if time_frame:
            time_frame = str(time_frame)
            pattern = re.compile(r"p|n[1-9]{1,2}")
            if not pattern.match(time_frame):
                raise ValueError("time_frame is invalid.")
            query_params["timeFrame"] = time_frame

        # Error checking for query parameter league_code
        if league_code:
            if league_code not in LEAGUE_CODE.keys():
                raise ValueError("league_code is invalid.")
            query_params["league"] = league_code

        url = self._generate_url("fixtures", query_params)
        fixtures = requests.get(url, headers=self.headers).json()

        return [Fixture(fixture) for fixture in fixtures["fixtures"]]

    def fixture(self, fixture_id):
        """
        Returns a Fixture object of the fixture with the given ID.
        """
        url = self._generate_url(f"fixtures/{fixture_id}")
        fixture = requests.get(url, headers=self.headers).json()
        return Fixture(fixture["fixture"])

    def team_fixtures(self, team, season=None, time_frame=None, venue=None):
        """
        Returns a list of Fixture objects made from the fixtures of the team
        with the given ID, in a certain season, time frame or venue.
        """
        # If string try to convert to ID
        if isinstance(team, str):
            if team.lower() in TEAM_ID.keys():
                team = TEAM_ID[team.lower()]
            else:
                raise ValueError(f"{team} is not a valid team or ID!")

        query_params = {}
        # Error checking for query parameter season
        if season:
            season = str(season)
            pattern = re.compile(r"\d\d\d\d")
            if not pattern.match(season):
                raise ValueError("season is invalid.")
            query_params["season"] = season

        # Error checking for query parameter time_frame
        if time_frame:
            time_frame = str(time_frame)
            pattern = re.compile(r"p|n[1-9]{1,2}")
            if not pattern.match(time_frame):
                raise ValueError("time_frame is invalid.")
            query_params["timeFrame"] = time_frame

        # Error checking for query parameter venue
        if venue:
            if venue not in ("home", "away"):
                raise ValueError("venue is invalid.")
            query_params["venue"] = venue

        url = self._generate_url(f"teams/{team}/fixtures", query_params)
        fixtures = requests.get(url, headers=self.headers).json()

        return [Fixture(fixture) for fixture in fixtures["fixtures"]]

    def team(self, team):
        """
        Returns a Team object made from the given team.
        """
        # If string try to convert to ID
        if isinstance(team, str):
            if team.lower() in TEAM_ID.keys():
                team = TEAM_ID[team.lower()]
            else:
                raise ValueError(f"{team} is not a valid team or ID!")

        url = self._generate_url(f"teams/{team}")
        team = requests.get(url, headers=self.headers).json()
        return Team(team)

    def players(self, team):
        """
        Returns a list of Player objects made from players playing for the team
        with the given ID.
        """
        # If string try to convert to ID
        if isinstance(team, str):
            if team.lower() in TEAM_ID.keys():
                team = TEAM_ID[team.lower()]
            else:
                raise ValueError(f"{team} is not a valid team or ID!")

        url = self._generate_url(f"teams/{team}/players")
        players = requests.get(url, headers=self.headers).json()

        return [Player(player, team) for player in players["players"]]

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
