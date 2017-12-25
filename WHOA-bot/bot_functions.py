"""Functions for the bot."""
import os
import json
from math import ceil
import random
from PyDictionary import PyDictionary

from weather import Weather
from meme_class import Meme
from quotes_class import Quotes
from insults_class import Insults

# CONSTANTS
COMMAND_PREFIX = 'WHOA'
#

weather = Weather()
meme = Meme()
quotes_obj = Quotes()
insults = Insults()

def is_command(msg):
    """Parse to see if command."""
    if msg.upper().startswith(COMMAND_PREFIX):
        return (True, msg[len(COMMAND_PREFIX) + 1:])
    return (False, msg)


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
    # TODO update this message
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


def parse_commands(msg, message_obj, client_obj, stats_obj):
    """Function that parse the command and send a response if needed."""
    if msg.find('hello') == 0:
        return ('message', 'Hello {0.author.mention}'.format(message_obj))

    if msg.find('repeat') == 0:
        return ('message', msg[len('repeat'):])

    if msg.find('stats_perc') == 0:
        return ('message', stats_obj.str_stats_perc(message_obj.server.id))

    if msg.find('stats') == 0:
        return ('message', stats_obj.str_stats(message_obj.server.id))

    if msg.find('weather') == 0:
        return ('message', get_wheater_condition(msg))

    if msg.find('fortune') == 0:
        return ('message', 'Not implemented yet')

    if msg.find('dictionary') == 0:
        return ('message', search_dictionary(msg))

    if msg.find('addquote') == 0:
        n_msg = msg[len('addquotes'):]
        n_msg = n_msg.split(" *** ", 1)
        quotes_obj.add(n_msg[0], n_msg[1])
        return ('message', '')

    if msg.find('quote') == 0:
        return ('message', quotes_obj.get())

    if msg.find('help') == 0:
        return ('message', make_help_msg())

    if msg.find('meme') == 0:
        return meme.get_meme()

    return ('message', generate_whoah())


def search_dictionary(msg):
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
                    return message.author.mention + insults.get()
                del lst_state[-1]
                ind += len(ch)
                cond = False
                continue

        if cond:
            # Normal character
            ind += 1

    lst_state.reverse()
    return "".join([bracket_close[x] for x in lst_state])
