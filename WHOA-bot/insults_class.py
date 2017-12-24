"""Insults class"""

import json
import random

INSULTS_F = r"ressource//insults.json"


class Insults(object):
    """Insults class definiton."""

    def __init__(self):
        self.insults = [" is stupid."]
        with open(INSULTS_F, 'r') as f:
            self.insults += json.load(f)['insults']
        self.l_insults = len(self.insults)

    def get(self):
        return self.insults[random.randrange(0, self.l_insults * 1000) % self.l_insults]
