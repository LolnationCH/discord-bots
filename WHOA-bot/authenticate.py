"""Get token for the bot."""
import json


AUTH = r"ressource//auth.json"


def get_token():
    """Get token."""
    with open(AUTH, 'r') as fp:
        return json.load(fp)['token']
