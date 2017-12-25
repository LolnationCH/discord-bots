"""Stats class."""

from os import walk
import os.path
import pickle


class Stats_recorder(object):
    """Keep track of the stats for the server."""

    STATS_F = r"ressource//stats"

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
        if self.stats != None:
            list_tup = sorted(self.stats[id_server].items(), reverse=True)
            stre = ''
            for i in range(0, len(list_tup)):
                stre += str(i + 1) + '. ' + list_tup[i][0] + ' => ' + str(list_tup[i][1])
            return stre
        return ''
    
    
    def str_stats_perc(self, id_server):
        """Make print str."""
        if self.stats:
            list_tup = sorted(self.stats[id_server].items(), reverse=True)
            max_value = float(sum(x for _, x in list_tup))
            stre = ''
            for i in range(0, len(list_tup)):
                stre += str(i + 1) + '. ' + list_tup[i][0] + ' => ' +\
                        "{0:.2f} %".format((list_tup[i][1] / max_value) * 100)
            return stre
        return ''
