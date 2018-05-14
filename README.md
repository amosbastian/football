football
-------


[![PyPI](https://img.shields.io/pypi/v/football.svg)](https://pypi.org/project/football/)
 ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/football.svg)

A Python wrapper around the [football-data API](https://www.football-data.org).

### Installing

The recommended way to install `football` is with pip

```bash
pip install football
```

You can also use pip to install `football` directly from GitHub

```bash
pip install git+https://github.com/amosbastian/football.git
```

or you can install the project in "editable" mode like so

```bash
git clone https://github.com/amosbastian/football.git
cd football
pip install -e .
```

### Usage

Currently the way to use `football` is to instantiate a `Football` class using your API key (can also be used without), which can be request [here](https://www.football-data.org/client/register)

```python
from football import Football
football = Football("your_api_key")

manchester_united = football.team(66)
```

The following (sub) resources are available

### Get all available competitions
```python
# This year
competitions = football.competitions()
# Given year
competitions = football.competitions(2015)
```
### Get all teams in the given competition
```python
teams = football.teams()
```
### Get the league table / current standings on the given competition
```python
# Get the Premier League table
table = football.table("PL")
```
### Get all fixtures of the given competition
```python
# Get the fixtures of the Premier League
fixtures = football.competition_fixtures("PL")
```
### Get all fixtures across competitions
```python
fixtures = football.fixtures()
```
### Get a single fixture
* Currently not working!
### Get all fixtures of a given team
```python
# Get Manchester United's fixtures
fixtures = football.team_fixtures(66)
```
### Get a team
```python
# Get Manchester United
team = football.team(66)
```
### Get all players of the given team
```python
# Get Manchester United's players
team = football.players(66)
```

## Contributing

Please read [CONTRIBUTING.md](https://github.com/amosbastian/football/blob/master/CONTRIBUTING.md) for details on how to contribute to `football` and what the best way to go about this is!

## Roadmap

* Create classes for each (sub) resource
* Add helper functions
* Improve the use of filters
* Add utilities for team/league/competition codes, names etc.
* ...

## Authors

* **Amos Bastian** - *Initial work* - [@amosbastian](https://github.com/amosbastian)

See also the list of [contributors](https://github.com/amosbastian/football/graphs/contributors) who participated in this project.

## Changelog

#### 0.1.1 - 2018-05-14
##### Added
- Initial release - contains functions for each (sub) resource of the football-data API, including filtering.

## License

This project is licensed under the AGPL-3.0 license - see the [LICENSE](https://github.com/amosbastian/football/blob/master/LICENSE) file for details.

## Acknowledgements

* Daniel Freitag - creator of the [football-data API](https://www.football-data.org/) 
