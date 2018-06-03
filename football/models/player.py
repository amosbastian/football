import requests

from dateutil.parser import parse


class Player():
    """
    The Player class.
    """

    API_URL = "http://api.football-data.org/v1/"

    def __init__(self, player, team_id, team=None):
        self.contract_until = player["contractUntil"]
        self.date_of_bith = parse(player["dateOfBirth"])
        self.market_value = player["marketValue"] 
        self.name = player["name"]
        self.nationality = player["nationality"]
        self.number = player["jerseyNumber"]
        self.position = player["position"]
        self.team_id = team_id
        self.team_url = f"http://api.football-data.org/vi/teams/{team_id}"

        # If team not given, retrieve name
        if not team:
            self.team = self._team()
        else:
            self.team = team

    def _team(self):
        """
        Returns the player's team.
        """
        response = requests.get(f"{self.API_URL}teams/{self.team_id}").json()
        return response["name"]
