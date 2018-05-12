import os
import unittest
from football import Football


class TestFootball(unittest.TestCase):
    football = Football(os.environ["FOOTBALL_API_KEY"])

    def test_competitions(self):
        competitions = self.football.competitions()
        self.assertIsInstance(competitions, list)
        self.assertEqual(competitions[0]["id"], 444)
        self.assertEqual(competitions[0]["year"], "2017")
        self.assertEqual(competitions[0]["league"], "BSA")
        self.assertEqual(competitions[0]["numberOfMatchdays"], 38)
        self.assertEqual(competitions[0]["numberOfTeams"], 20)
        self.assertEqual(competitions[0]["numberOfGames"], 380)

    def test_teams(self):
        teams = self.football.teams(445)
        self.assertIsInstance(teams, dict)
        self.assertEqual(teams["count"], 20)
        self.assertIsInstance(teams["teams"], list)
        self.assertEqual(teams["count"], len(teams["teams"]))

    def test_table(self):
        table = self.football.table(445)
        self.assertIsInstance(table, dict)
        self.assertIsInstance(table["standing"], list)
        self.assertEqual(len(table["standing"]), 20)

    def test_competition_fixtures(self):
        competition_fixtures = self.football.competition_fixtures(445)
        self.assertIsInstance(competition_fixtures, dict)
        self.assertIsInstance(competition_fixtures["fixtures"], list)
        self.assertEqual(competition_fixtures["count"],
                         len(competition_fixtures["fixtures"]))

    def test_fixtures(self):
        fixtures = self.football.fixtures()
        self.assertIsInstance(fixtures, dict)
        self.assertIsInstance(fixtures["fixtures"], list)
        self.assertEqual(fixtures["count"], len(fixtures["fixtures"]))

    def test_fixture(self):
        pass

    def test_team_fixtures(self):
        team_fixtures = self.football.team_fixtures(66)
        self.assertIsInstance(team_fixtures, dict)
        self.assertIsInstance(team_fixtures["fixtures"], list)
        self.assertEqual(len(team_fixtures["fixtures"]),
                         team_fixtures["count"])
        self.assertEqual(team_fixtures["fixtures"][0]["matchday"], 1)

    def test_team(self):
        team = self.football.team(66)
        self.assertIsInstance(team, dict)
        self.assertEqual(team["name"], "Manchester United FC")
        self.assertEqual(team["code"], "MUFC")
        self.assertEqual(team["shortName"], "ManU")

    def test_players(self):
        players = self.football.players(66)
        self.assertIsInstance(players, dict)
        self.assertIsInstance(players["players"], list)
        self.assertEqual(len(players["players"]), players["count"])

if __name__ == '__main__':
    unittest.main()
