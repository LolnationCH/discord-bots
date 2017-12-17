"""Functions for the bot."""
import os.path
import json
import pickle
from math import ceil
import random

from weather import Weather

# CONSTANTS
AUTH = "auth.json"
STATS_F = "stats.p"
#

weather = Weather()


def save_stats(stats):
    """Save stats."""
    pickle.dump(stats, open(STATS_F, "wb"))


def load_stats():
    """Save stats."""
    if os.path.isfile(STATS_F):
        return pickle.load(open(STATS_F, "rb"))
    return {}


def is_command(msg):
    """Parse to see if command."""
    if msg.startswith('WHOAH'):
        return (True, msg[6:])
    return (False, msg)


def make_str_stats(stats_count):
    """Make print str."""
    list_tup = sorted(stats_count.items(), key=stats_count.get, reverse=True)
    stre = ''
    for i in range(0, len(list_tup)):
        stre += str(i + 1) + '. ' + list_tup[i][0] + ' => ' + str(list_tup[i][1])
    return stre


def make_str_stats_perc(stats_count):
    """Make print str."""
    list_tup = sorted(stats_count.items(), key=stats_count.get, reverse=True)
    max_value = float(sum(x for _, x in list_tup))
    stre = ''
    for i in range(0, len(list_tup)):
        stre += str(i + 1) + '. ' + list_tup[i][0] + ' => ' +\
                str((list_tup[i][1] / max_value) * 100)
    return stre


def get_token():
    """Get token."""
    with open(AUTH, 'r') as fp:
        return json.load(fp)['token']


def _farenheit_to_celcius_(faren):
    """."""
    return str(ceil((int(faren) - 32) * 5.0/9.0))


def get_wheater_condition(msg):
    """Parse to get weather info."""
    n_m = msg[len('weather'):]
    if n_m != '':
        location = weather.lookup_by_location(n_m)
    else:
        location = weather.lookup_by_location('sherbrooke')
    forecast = location.forecast()[0]
    return forecast.text() + ' => High : ' + _farenheit_to_celcius_(forecast.high())\
        + u" \u2103" + ', Low : ' + _farenheit_to_celcius_(forecast.low()) + u" \u2103"


def make_help_msg():
    """."""
    return 'Commands list : \n' +\
        'hello : returns a hello msg to the auhtor\n' +\
        'repeat : returns the message said after "repeat"\n' +\
        'stats_perc : returns percentage of messages sent by user\n' +\
        'stats : returns total of messages sent by user\n' +\
        'fortune : returns fortune\n' +\
        'weather : returns weather for location, default:sherbrooke\n' +\
        '<nothing> : Try it :)'


def generate_whoah():
    """:)."""
    return 'WHOAH ' * random.randrange(0, 50)
