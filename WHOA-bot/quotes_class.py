"""Class to manipulate addition and showing of quotes."""

import os
import random
import msgpack

from ressource import RESPONSE_TYPE


class Quotes(object):
    """Class to manipulate addition and showing of quotes."""

    QUOTES_F = r"ressource//quotes.msgpack"

    def load(self):
        """Load files."""
        if os.path.isfile(self.QUOTES_F):
            self.quotes = msgpack.load(open(self.QUOTES_F, "rb"))

    def __init__(self):
        """."""
        self.quotes = []
        self.load()

    def save(self):
        """Save files."""
        msgpack.dump(self.quotes, open(self.QUOTES_F, "wb"))

    def add(self, msg):
        """Add quotes."""
        msg = msg.split(" *** ", 1)
        self.quotes.append({b'quote': msg[0], b'author': msg[1]})
        self.save()
        return RESPONSE_TYPE['NONE'], ''

    def get(self):
        """Show quotes."""
        ind = random.randrange(0, len(self.quotes))
        return RESPONSE_TYPE['MESSAGE'], '%s\n\t- %s' %\
            (str(self.quotes[ind][b'quote'])[2:-1], str(self.quotes[ind][b'author'])[2:-1])
