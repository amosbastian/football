import requests


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
        self.last_update = competition["lastUpdated"]
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
        response = requests.get(self._fixtures_url)
        return response.json()

    def teams(self):
        """
        Returns all teams currently participating in the competition.
        """
        response = requests.get(self._teams_url)
        return response.json()

    def league_table(self):
        """
        Returns the current league table of the competition.
        """
        response = requests.get(self._league_table_url)
        return response.json()
