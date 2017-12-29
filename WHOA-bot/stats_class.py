"""Stats class."""

import os.path
import pickle


class Stats_recorder(object):
    """Keep track of the stats for the server."""

    STATS_F = r"ressource//stats.p"

    def load(self):
        """Load stats."""
        if os.path.isfile(self.STATS_F):
            self.stats = pickle.load(open(self.STATS_F, "rb"))

    def __init__(self):
        """."""
        self.stats = {}
        self.load()

    def save(self):
        """Save stats."""
        pickle.dump(self.stats, open(self.STATS_F, "wb"))

    def add(self, id_server, author_name):
        """Add count to stats for author_name."""
        if id_server not in self.stats:
            self.stats[id_server] = {}
        if author_name not in self.stats[id_server]:
            self.stats[id_server][author_name] = 0
        self.stats[id_server][author_name] += 1
        self.save()

    def str_stats(self, id_server):
        """Make print str."""
        list_key = sorted(self.stats[id_server], key=self.stats[id_server].get, reverse=True)
        stre = ''
        for i in range(0, len(list_key)):
            stre += '%d. %s => %d\n' % ((i+1), list_key[i], self.stats[id_server][list_key[i]])
        return stre

    def str_stats_perc(self, id_server):
        """Make print str."""
        list_key = sorted(self.stats[id_server], key=self.stats[id_server].get, reverse=True)
        max_value = float(sum(self.stats[id_server][x] for x in list_key))
        stre = ''
        for i in range(0, len(list_key)):
            stre += '%d. %s => ' % ((i+1), list_key[i]) +\
                    "{0:.2f} %\n".format((self.stats[id_server][list_key[i]] / max_value) * 100)
        return stre
