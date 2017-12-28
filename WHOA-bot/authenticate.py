"""Get token for the bot."""
import json


RESPONSE_TYPE = {'NONE': -1, 'INVITE': 0, 'MESSAGE': 1, 'FILE': 2}
AUTH = r"ressource//auth.json"


def get_token():
    """Get token."""
    with open(AUTH, 'r') as fp:
        return json.load(fp)['token']
