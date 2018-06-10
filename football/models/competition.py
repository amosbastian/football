import requests

from .fixture import Fixture
from .table import Table
from .team import Team
from ..utils import headers


class Competition():
    """
    The Competition class.
    """
    def __init__(self, competition):
        self._competition_url = competition["_links"]["self"]["href"]
        self._fixtures_url = competition["_links"]["fixtures"]["href"]
        self._league_table_url = competition["_links"]["leagueTable"]["href"]
        self._teams_url = competition["_links"]["teams"]["href"]

        self.current_matchday = competition["currentMatchday"]
        self.id = competition["id"]
        self.last_updated = competition["lastUpdated"]
        self.name = competition["caption"]
        self.number_games = competition["numberOfGames"]
        self.number_matchdays = competition["numberOfMatchdays"]
        self.number_teams = competition["numberOfTeams"]
        self.shortname = competition["league"]
        self.year = competition["year"]

    def fixtures(self):
        """
        Returns all current fixtures of the competition.
        """
        response = requests.get(self._fixtures_url, headers=headers()).json()
        return [Fixture(fixture) for fixture in response["fixtures"]]

    def teams(self):
        """
        Returns all teams currently participating in the competition.
        """
        response = requests.get(self._teams_url, headers=headers()).json()
        return [Team(team) for team in response["teams"]]

    def table(self):
        """
        Returns the current league table of the competition.
        """
        response = requests.get(
            self._league_table_url, headers=headers()).json()
        return Table(response)

    def __str__(self):
        return self.name
