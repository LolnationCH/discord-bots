"""Class to manipulate addition and showing of quotes."""

import os
import msgpack

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

    
    def add(self, msg, author):
        """Add quotes."""
        index = len(self.quotes)
        self.quotes[index] = {b'quote': msg, b'author': author}
        self.save()
    
    
    def get(self):
        """Show quotes."""
        ind = random.randrange(0, len(self.quotes))
        return str(self.quotes[ind][b'quote'])[2:-1] + '\n\t- ' + str(self.quotes[ind][b'author'])[2:-1]
