"""Functions for the bot."""
from os import walk
import os.path
import json
import pickle
from math import ceil
import random
from PyDictionary import PyDictionary

import msgpack
from weather import Weather

# CONSTANTS
AUTH = r"ressource\auth.json"
STATS_F = r"ressource\stats.p"
QUOTES_F = r"ressource\quotes.msgpack"
INSULTS_F = r"ressource\insults.json"
MEMES_F = r"ressource\memes"
INTERNET_MEME_F = r"ressource\memes\internet.json"
COMMAND_PREFIX = 'WHOA'
#

weather = Weather()

insults = [" is stupid."]
with open(INSULTS_F, 'r') as f:
    insults = json.load(f)['insults']
l_insults = len(insults)


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
    if msg.upper().startswith(COMMAND_PREFIX):
        return (True, msg[len(COMMAND_PREFIX) + 1:])
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


def parse_commands(msg, message_obj, client_obj, stats_count, quotes):
    """Function that parse the command and send a response if needed."""
    if msg.find('hello') == 0:
        return ('message', 'Hello {0.author.mention}'.format(message_obj))

    if msg.find('repeat') == 0:
        return ('message', msg[len('repeat'):])

    if msg.find('stats_perc') == 0:
        return ('message', make_str_stats_perc(stats_count))

    if msg.find('stats') == 0:
        return ('message', make_str_stats(stats_count))

    if msg.find('weather') == 0:
        return ('message', get_wheater_condition(msg))

    if msg.find('fortune') == 0:
        return ('message', 'Not implemented yet')

    if msg.find('dictionary') == 0:
        return ('message', search_dictionnary(msg))

    if msg.find('addquote') == 0:
        n_msg = msg[len('addquotes'):]
        n_msg = n_msg.split(" *** ", 1)
        add_quotes(n_msg[0], n_msg[1], quotes)
        return ('message', '')

    if msg.find('quote') == 0:
        return ('message', show_quote(quotes))

    if msg.find('help') == 0:
        return ('message', make_help_msg())

    if msg.find('meme') == 0:
        return get_meme_path()

    return ('message', generate_whoah())


def search_dictionnary(msg):
    """Get word meaning, synonym, antonym and translation."""
    lt_w = msg.split(' ')
    dictionary = PyDictionary(lt_w[-1])
    stre = lt_w[-1]
    if 'meaning' in lt_w:
        stre += '\n' + str(dictionary.getMeanings()[lt_w[-1]])
    if 'synonym' in lt_w:
        stre += '\n' + str(dictionary.getSynonyms()[0][lt_w[-1]])
    if 'antonym' in lt_w:
        stre += '\n' + str(dictionary.getAntonyms()[0][lt_w[-1]])
    if 'translate' in lt_w:
        stre += '\n' + dictionary.translateTo(lt_w[lt_w.index('translate') + 1])[0]
    return stre

def add_quotes(msg, author, quotes):
    """Add quotes."""
    index = len(quotes)
    quotes[index] = {b'quote': msg, b'author': author}


def show_quote(quotes):
    """Show quotes."""
    ind = random.randrange(0, len(quotes))
    return str(quotes[ind][b'quote'])[2:-1] + '\n\t- ' + str(quotes[ind][b'author'])[2:-1]


def get_meme_path():
    """."""
    files = []
    if random.randrange(0, 2) == 0:
        for (_, _, filenames) in walk(MEMES_F):
            files.extend(filenames)
            break
    if not files:
        with open(INTERNET_MEME_F, 'r') as fi:
            files = json.load(fi)
            return ('message', files[random.randrange(0, len(files))])
    return ('file', MEMES_F + '\\' + files[random.randrange(0, len(files))])


def formatted_correctly(message):
    """."""
    bracket_open = ['{', '[', '(', '"""', '"', '/*', '<']
    bracket_close = ['}', ']', ')', '"""', '"', '*/', '>']
    lst_state = []
    msg = message.content

    ind = 0
    max_l = len(msg)
    while ind < max_l:
        cond = True
        for ch in bracket_open:
            if msg[ind:ind + len(ch)] == ch:
                lst_state.append(bracket_open.index(ch))
                ind += len(ch)
                cond = False
                break

        if lst_state:
            ch = bracket_close[lst_state[-1]]
            char_msg = msg[ind:ind + len(ch)]
            if char_msg in bracket_close:
                if msg[ind:ind + len(ch)] != ch:
                    return message.author.mention +\
                        insults[random.randrange(0, l_insults * 1000) % l_insults]
                del lst_state[-1]
                ind += len(ch)
                cond = False
                continue

        if cond:
            # Normal character
            ind += 1

    lst_state.reverse()
    return "".join([bracket_close[x] for x in lst_state])
