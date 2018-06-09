import requests

from .fixture import Fixture
from .player import Player
from ..utils import headers


class Team():
    """
    The Team class.
    """
    def __init__(self, team):
        self.team_url = team["_links"]["self"]["href"]
        self.fixtures_url = team["_links"]["fixtures"]["href"]
        self.players_url = team["_links"]["players"]["href"]
        self.badge_url = team["crestUrl"]
        self.team_id = int(self.team_url.split("/")[-1])

        self.code = team["code"]
        self.fixtures = self._fixtures()
        self.name = team["name"]
        self.players = self._players()
        self.shortname = team["shortName"]
        self.squad_value = team["squadMarketValue"]

    def _players(self):
        """
        Returns a list of Player objects.
        """
        response = requests.get(self.players_url, headers=headers()).json()
        return [Player(player, self.team_id, self.name)
                for player in response["players"]]

    def _fixtures(self):
        """
        Returns a list of Fixture objects.
        """
        response = requests.get(self.fixtures_url, headers=headers()).json()
        return [Fixture(fixture) for fixture in response["fixtures"]]

    def __str__(self):
        return self.name
