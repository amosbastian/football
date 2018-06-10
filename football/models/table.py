from operator import attrgetter
from prettytable import PrettyTable


class Table():
    """
    The Table class.
    """
    def __init__(self, table):
        self.table_url = table["_links"]["self"]["href"]
        self.competition_url = table["_links"]["competition"]["href"]
        self.league_name = table["leagueCaption"]
        self.matchday = table["matchday"]
        self.standing = [Standing(standing) for standing in table["standing"]]

    def sort(self, column, reverse=False):
        """
        Sorts the table by the given column.
        """
        if not hasattr(self.standing[0], column):
            raise ValueError(f"Can't sort table by given column: {column}")

        self.standing = sorted(
            self.standing, key=attrgetter(column), reverse=reverse)

    def __str__(self):
        """
        Use PrettyTable to represent the table when it is printed.
        """
        # Table header
        table = PrettyTable(
            ["#", "Team", "Played", "Won", "Drawn", "Lost", "For", "Against",
             "GD", "Points"])

        # Align column left
        table.align["Team"] = "l"

        # Add rows to the table
        for row in self.standing:
            table.add_row([
                row.position, row.team_name, row.played, row.wins, row.draws,
                row.losses, row.goals_for, row.goals_against,
                row.goal_difference, row.points])

        return str(table)


class Standing():
    """
    The Standing class.
    """
    def __init__(self, standing):
        self.away_form = standing["away"]
        self.badge = standing["crestURI"]
        self.draws = standing["draws"]
        self.goals_for = standing["goals"]
        self.goals_against = standing["goalsAgainst"]
        self.goal_difference = standing["goalDifference"]
        self.home_form = standing["home"]
        self.losses = standing["losses"]
        self.points = standing["points"]
        self.position = standing["position"]
        self.team_url = standing["_links"]["team"]["href"]
        self.team_name = standing["teamName"]
        self.wins = standing["wins"]

        self.played = self.wins + self.draws + self.losses
