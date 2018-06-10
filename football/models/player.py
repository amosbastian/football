import requests

from dateutil.parser import parse
from ..utils import headers


class Player():
    """
    The Player class.
    """

    API_URL = "http://api.football-data.org/v1/"

    def __init__(self, player, team_id, team=None):
        self.contract_until = player["contractUntil"]
        self.date_of_birth = parse(player["dateOfBirth"])
        self.market_value = player["marketValue"] 
        self.name = player["name"]
        self.nationality = player["nationality"]
        self.number = player["jerseyNumber"]
        self.position = player["position"]
        self.team_id = team_id
        self.team_url = f"http://api.football-data.org/vi/teams/{team_id}"

    def team(self):
        """
        Returns the player's team.
        """
        response = requests.get(
            f"{self.API_URL}teams/{self.team_id}", headers=headers()).json()
        return response["name"]

    def __str__(self):
        return (f"{self.number:2} - {self.name} - {self.position} - "
                f"{self.team}")
