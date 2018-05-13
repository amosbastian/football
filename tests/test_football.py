import os
import unittest
from football import Football


class TestFootball(unittest.TestCase):
    football = Football(os.environ["FOOTBALL_API_KEY"])

    def test_competitions(self):
        # General tests
        competitions = self.football.competitions()
        self.assertIsInstance(competitions, list)
        self.assertEqual(competitions[0]["id"], 444)
        self.assertEqual(competitions[0]["year"], "2017")
        self.assertEqual(competitions[0]["league"], "BSA")
        self.assertEqual(competitions[0]["numberOfMatchdays"], 38)
        self.assertEqual(competitions[0]["numberOfTeams"], 20)
        self.assertEqual(competitions[0]["numberOfGames"], 380)

        # Test with query parameters
        competitions = self.football.competitions(2015)
        self.assertEqual(competitions[0]["year"], "2015")
        self.assertRaises(ValueError, self.football.competitions, "abc")

    def test_teams(self):
        # General tests
        teams = self.football.teams(445)
        self.assertIsInstance(teams, dict)
        self.assertEqual(teams["count"], 20)
        self.assertIsInstance(teams["teams"], list)
        self.assertEqual(teams["count"], len(teams["teams"]))

    def test_table(self):
        # General tests
        table = self.football.table(445)
        self.assertIsInstance(table, dict)
        self.assertIsInstance(table["standing"], list)
        self.assertEqual(len(table["standing"]), 20)

        # Test with query parameters
        table = self.football.table(445, 1)
        self.assertEqual(table["matchday"], 1)
        self.assertRaises(ValueError, self.football.table, 445, "abc")

    def test_competition_fixtures(self):
        # General tests
        competition_fixtures = self.football.competition_fixtures(445)
        self.assertIsInstance(competition_fixtures, dict)
        self.assertIsInstance(competition_fixtures["fixtures"], list)
        self.assertEqual(competition_fixtures["count"],
                         len(competition_fixtures["fixtures"]))

        # Test with query parameters
        self.assertRaises(
            ValueError, self.football.competition_fixtures, 445, "abc")
        self.assertEqual(
            self.football.competition_fixtures(445, matchday=38),
            self.football.competition_fixtures(445, time_frame="n38"))

    def test_fixtures(self):
        # General tests
        fixtures = self.football.fixtures()
        self.assertIsInstance(fixtures, dict)
        self.assertIsInstance(fixtures["fixtures"], list)
        self.assertEqual(fixtures["count"], len(fixtures["fixtures"]))

        # Test with query parameters
        self.assertRaises(ValueError, self.football.fixtures, time_frame="abc")
        self.assertRaises(ValueError, self.football.fixtures, league_code=123)
        self.assertEqual(
            self.football.fixtures(league_code="PL")["fixtures"],
            self.football.competition_fixtures(445, matchday=38)["fixtures"])

    def test_fixture(self):
        pass

    def test_team_fixtures(self):
        # General tests
        team_fixtures = self.football.team_fixtures(66)
        self.assertIsInstance(team_fixtures, dict)
        self.assertIsInstance(team_fixtures["fixtures"], list)
        self.assertEqual(len(team_fixtures["fixtures"]),
                         team_fixtures["count"])
        self.assertEqual(team_fixtures["fixtures"][0]["matchday"], 1)

        # Test with query parameters
        self.assertRaises(
            ValueError, self.football.team_fixtures, 66, time_frame="abc")
        self.assertRaises(
            ValueError, self.football.team_fixtures, 66, season="abc")
        self.assertRaises(
            ValueError, self.football.team_fixtures, 66, venue="abc")

    def test_team(self):
        # General tests
        team = self.football.team(66)
        self.assertIsInstance(team, dict)
        self.assertEqual(team["name"], "Manchester United FC")
        self.assertEqual(team["code"], "MUFC")
        self.assertEqual(team["shortName"], "ManU")

    def test_players(self):
        # General tests
        players = self.football.players(66)
        self.assertIsInstance(players, dict)
        self.assertIsInstance(players["players"], list)
        self.assertEqual(len(players["players"]), players["count"])

    def test__generate_url(self):
        # General tests
        url = self.football._generate_url("competitions")
        self.assertEqual(url, "http://api.football-data.org/v1/competitions/")
        url = self.football._generate_url("competitions", {"season": 2015})
        self.assertEqual(
            url, "http://api.football-data.org/v1/competitions/?season=2015")
        url = self.football._generate_url(
            "competitions/445/fixtures", {"matchday": 1, "timeFrame": "n14"})
        self.assertEqual(url, ("http://api.football-data.org/v1/competitions/"
                               "445/fixtures?matchday=1&timeFrame=n14"))


if __name__ == '__main__':
    unittest.main()
