import os


def headers():
    api_key = os.environ["FOOTBALL_API_KEY"]
    return {"X-Auth-Token": api_key}
