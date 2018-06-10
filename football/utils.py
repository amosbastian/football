import os


def headers():
    api_key = os.environ["FOOTBALL_API_KEY"]
    return {"X-Auth-Token": api_key}

LEAGUE_ID = {
    "444": "BSA",
    "445": "PL",
    "446": "ELC",
    "447": "EL1",
    "448": "EL2",
    "449": "DED",
    "450": "FL1",
    "451": "FL2",
    "452": "BL1",
    "453": "BL2",
    "455": "PD",
    "456": "SA",
    "457": "PPL",
    "458": "DFB",
    "459": "SB",
    "464": "CL",
    "466": "AAL"
}

LEAGUE_CODE = {
    "BSA": 444,
    "PL": 445,
    "ELC": 446,
    "EL1": 447,
    "EL2": 448,
    "DED": 449,
    "FL1": 450,
    "FL2": 451,
    "BL1": 452,
    "BL2": 453,
    "PD": 455,
    "SA": 456,
    "PPL": 457,
    "DFB": 458,
    "SB": 459,
    "CL": 464,
    "AAL": 466
}

MAX_TEAM_NAME = 20
