import requests

from collections import Counter
from .fixture import Fixture
from .player import Player
from prettytable import PrettyTable
from ..utils import headers
from ..constants import LEAGUE_CODE


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
        self.name = team["name"]
        self.shortname = team["shortName"]
        self.squad_value = team["squadMarketValue"]

    def players(self):
        """
        Returns a list of Player objects.
        """
        response = requests.get(self.players_url, headers=headers()).json()
        return [Player(player, self.team_id, self.name)
                for player in response["players"]]

    def fixtures(self):
        """
        Returns a list of Fixture objects.
        """
        response = requests.get(self.fixtures_url, headers=headers()).json()
        return [Fixture(fixture) for fixture in response["fixtures"]]

    def depth(self, JSON=False):
        """
        Returns an overview of the team's positional depth.
        """
        players = self.players()
        positions = [player.position for player in players]

        if JSON:
            return dict(Counter(positions))
        else:
            # Create table
            table = PrettyTable(["Position", "#"])
            table.align["Position"] = "l"

            for position, amount in Counter(positions).items():
                table.add_row([position, amount])

            return table

    def results(self, league_code=None, number=5):
        """
        Return a list of the team's results.
        """
        fixtures = self.fixtures()

        if league_code:
            if league_code not in LEAGUE_CODE.keys():
                raise KeyError("Given league code does not exist!")

            competition_id = LEAGUE_CODE[league_code]

            # Check fixture's competition ID and if it has already been played
            results = [fixture for fixture in fixtures
                       if fixture.competition_id == competition_id and
                       fixture.winner]
        else:
            # Only check if fixture has already been played
            results = [fixture for fixture in fixtures if fixture.winner]

        if len(results) == 0:
            raise ValueError("No results found for the given league code.")

        return results[:number]

    def upcoming_fixtures(self, league_code=None, number=5):
        """
        Return a list of the team's upcoming fixtures.
        """
        fixtures = self.fixtures()

        if league_code:
            if league_code not in LEAGUE_CODE.keys():
                raise KeyError("Given league code does not exist!")

            competition_id = LEAGUE_CODE[league_code]

            # Check fixture's competition ID and if it has already been played
            results = [fixture for fixture in fixtures
                       if fixture.competition_id == competition_id and
                       not fixture.winner]
        else:
            # Only check if fixture has already been played
            results = [fixture for fixture in fixtures
                       if not fixture.winner]

        if len(results) == 0:
            raise ValueError("No fixtures found for the given league code.")

        return results[:number]

    def __str__(self):
        return self.name
