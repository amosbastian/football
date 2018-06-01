class Fixture():
    """
    The Fixture class.
    """
    def __init__(self, fixture):
        self._away_team_url = fixture["_links"]["awayTeam"]["href"]
        self._competition_url = fixture["_links"]["competition"]["href"]
        self._home_team_url = fixture["_links"]["homeTeam"]["href"]
        self._fixtures_url = fixture["_links"]["self"]["href"]

        self.away_goals = fixture["result"]["goalsAwayTeam"]
        self.away_team = fixture["awayTeamName"]
        self.date = fixture["date"]
        self.home_goals = fixture["result"]["goalsHomeTeam"]
        self.home_team = fixture["homeTeamName"]
        self.matchday = fixture["matchday"]
        self.odds = fixture["odds"]
        self.status = fixture["status"]
        self.winner = self._winner()

        if "halfTime" in fixture["result"].keys():
            self.away_goals_ht = fixture["result"]["halfTime"]["goalsAwayTeam"]
            self.home_goals_ht = fixture["result"]["halfTime"]["goalsHomeTeam"]
        else:
            self.away_goals_ht = self.away_goals
            self.home_goals_ht = self.home_goals

    def _winner(self):
        """
        Return name of the winning team, except return None in case of a draw.
        """
        if self.home_goals > self.away_goals:
            return self.home_team
        elif self.away_goals > self.home_goals:
            return self.away_team
        return None
