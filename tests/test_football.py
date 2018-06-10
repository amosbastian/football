"""
Contains unit tests for all functions in football.py.
"""
import os
import unittest
from football import Football
from football.models.competition import Competition
from football.models.fixture import Fixture
from football.models.player import Player
from football.models.table import Standing
from football.models.table import Table
from football.models.team import Team


class TestFootball(unittest.TestCase):
    """
    Class for unit testing football.py.
    """
    football = Football(os.environ["FOOTBALL_API_KEY"])

    def test_competitions(self):
        """
        Tests for the football.competitions function.
        """
        # General tests
        competitions = self.football.competitions()
        competition = competitions[0]
        self.assertIsInstance(competition, Competition)
        self.assertEqual(competition.id, 444)
        self.assertEqual(competition.year, "2017")
        self.assertEqual(competition.shortname, "BSA")
        self.assertEqual(competition.number_matchdays, 38)
        self.assertEqual(competition.number_teams, 20)
        self.assertEqual(competition.number_games, 380)

        # Test with query parameters
        competitions = self.football.competitions(2015)
        competition = competitions[0]
        self.assertEqual(competition.year, "2015")
        self.assertRaises(ValueError, self.football.competitions, "abc")

    def test_competition(self):
        """
        Tests for the football.competition function.
        """
        # General tests
        competition = self.football.competition(444)
        self.assertIsInstance(competition, Competition)
        self.assertEqual(competition.id, 444)
        self.assertEqual(competition.year, "2017")
        self.assertEqual(competition.shortname, "BSA")
        self.assertEqual(competition.number_matchdays, 38)
        self.assertEqual(competition.number_teams, 20)
        self.assertEqual(competition.number_games, 380)

        # Tests with query parameters
        self.assertRaises(ValueError, self.football.competition, 444, "2015")
        competition = self.football.competition(394, "2015")
        self.assertEqual(competition.year, "2015")

    def test_teams(self):
        """
        Tests for the football.teams function.
        """
        # General tests
        teams = self.football.teams(445)
        self.assertIsInstance(teams, list)
        team_names = [team.name for team in teams]
        team = teams[0]
        self.assertIsInstance(team, Team)
        self.assertEqual(team.name, "Arsenal FC")

        # Get fixtures and players, test these
        fixtures = team.fixtures()
        players = team.players()

        self.assertIsInstance(fixtures[0], Fixture)
        self.assertIsInstance(players[0], Player)
        self.assertTrue("Manchester United FC" in team_names)

    def test_table(self):
        """
        Tests for the football.table function.
        """
        # General tests
        table = self.football.table(445)
        self.assertIsInstance(table, Table)
        self.assertIsInstance(table.standing, list)
        standing = table.standing
        self.assertIsInstance(standing[0], Standing)

        # Test with query parameters
        table = self.football.table(445, 1)
        self.assertEqual(table.matchday, 1)
        self.assertRaises(ValueError, self.football.table, 445, "abc")

    def test_competition_fixtures(self):
        """
        Tests for the football.competition_fixtures function.
        """
        # General tests
        competition_fixtures = self.football.competition_fixtures(445)
        self.assertIsInstance(competition_fixtures, list)
        if len(competition_fixtures) > 0:
            self.assertIsInstance(competition_fixtures[0], Fixture)

        # Test with query parameters
        self.assertRaises(
            ValueError, self.football.competition_fixtures, 445, "abc")

    def test_fixtures(self):
        """
        Tests for the football.fixtures function.
        """
        # General tests
        fixtures = self.football.fixtures()
        self.assertIsInstance(fixtures, list)
        if len(fixtures) > 0:
            self.assertIsInstance(fixtures[0], Fixture)

        # Test with query parameters
        self.assertRaises(ValueError, self.football.fixtures, time_frame="abc")
        self.assertRaises(ValueError, self.football.fixtures, league_code=123)

    def test_fixture(self):
        """
        Tests for the football.fixture function.
        """
        fixture = self.football.fixture(159321)
        self.assertIsInstance(fixture, Fixture)
        self.assertEqual(fixture.home_team, "Manchester United FC")

    def test_team_fixtures(self):
        """
        Tests for the football.team_fixtures function.
        """
        # General tests
        team_fixtures = self.football.team_fixtures(66)
        self.assertIsInstance(team_fixtures, list)
        if len(team_fixtures) > 0:
            self.assertIsInstance(team_fixtures[0], Fixture)

        # Test with query parameters
        self.assertRaises(
            ValueError, self.football.team_fixtures, 66, time_frame="abc")
        self.assertRaises(
            ValueError, self.football.team_fixtures, 66, season="abc")
        self.assertRaises(
            ValueError, self.football.team_fixtures, 66, venue="abc")

        # Test with team name, shortname and code
        code_fixtures = self.football.team_fixtures("MUFC")
        shortname_fixtures = self.football.team_fixtures("ManU")
        name_fixtures = self.football.team_fixtures("Manchester United FC")

        self.assertEqual(team_fixtures[0].winner, code_fixtures[0].winner)
        self.assertEqual(team_fixtures[0].winner, shortname_fixtures[0].winner)
        self.assertEqual(team_fixtures[0].winner, name_fixtures[0].winner)

    def test_team(self):
        """
        Tests for the football.team function.
        """
        # General tests
        team = self.football.team(66)
        self.assertIsInstance(team, Team)
        self.assertEqual(team.name, "Manchester United FC")
        self.assertEqual(team.code, "MUFC")
        self.assertEqual(team.shortname, "ManU")

        # Test with team name, shortname and code
        code_team = self.football.team("MUFC")
        shortname_team = self.football.team("ManU")
        name_team = self.football.team("Manchester United FC")

        self.assertEqual(team.name, code_team.name)
        self.assertEqual(team.name, shortname_team.name)
        self.assertEqual(team.name, name_team.name)

    def test_players(self):
        """
        Tests for the football.players function.
        """
        # General tests
        players = self.football.players(66)
        self.assertIsInstance(players, list)
        player_names = [player.name for player in players]
        self.assertIn("Eric Bailly", player_names)

        # Test with team name, shortname and code
        code_players = self.football.players("MUFC")
        shortname_players = self.football.players("ManU")
        name_players = self.football.players("Manchester United FC")

        self.assertEqual(players[0].name, code_players[0].name)
        self.assertEqual(players[0].name, shortname_players[0].name)
        self.assertEqual(players[0].name, name_players[0].name)

    def test__generate_url(self):
        """
        Tests for the football._generate_url function.
        """
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
