"""Functions for the bot."""
import os.path
import json
import pickle
import msgpack
from math import ceil
import random

from weather import Weather

# CONSTANTS
AUTH = r"ressource\auth.json"
STATS_F = r"ressource\stats.p"
QUOTES_F = r"ressource\quotes.msgpack"
#

weather = Weather()


def save_files(stats, quotes):
    """Save files."""
    pickle.dump(stats, open(STATS_F, "wb"))
    msgpack.dump(quotes, open(QUOTES_F, "wb"))


def load_files():
    """Load files."""
    if os.path.isfile(STATS_F):
        n_dic = pickle.load(open(STATS_F, "rb"))
    else:
        n_dic = {}
    if os.path.isfile(QUOTES_F):
        n_dic2 = msgpack.load(open(QUOTES_F, "rb"))
    else:
        n_dic2 = {}
    return n_dic, n_dic2


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


def parse_commands(msg, message_obj, stats_count, quotes):
    """Function that parse the command and send a response if needed."""
    if msg.find('hello') == 0:
        return 'Hello {0.author.mention}'.format(message_obj)

    if msg.find('repeat') == 0:
        return msg[len('repeat'):]

    if msg.find('stats_perc') == 0:
        return make_str_stats_perc(stats_count)

    if msg.find('stats') == 0:
        return make_str_stats(stats_count)

    if msg.find('weather') == 0:
        return get_wheater_condition(msg)

    if msg.find('fortune') == 0:
        return 'Not implemented yet'

    if msg.find('addquote') == 0:
        n_msg = msg[len('addquotes'):]
        n_msg = n_msg.split(" *** ", 1)
        add_quotes(n_msg[0], n_msg[1], quotes)
        return ''
    if msg.find('quote') == 0:
        return show_quote(quotes)

    if msg.find('help') == 0:
        return make_help_msg()

    return generate_whoah()


def add_quotes(msg, author, quotes):
    """Add quotes."""
    index = len(quotes)
    quotes[index] = (msg, author)


def show_quote(quotes):
    """Show quotes."""
    ind = random.randrange(0, len(quotes))
    return quotes[ind][0] + '\n\t- ' + quotes[ind][1]


def formatted_correctly(msg):
    """."""
