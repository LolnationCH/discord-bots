"""Functions for the bot."""
from math import ceil
import random

from PyDictionary import PyDictionary
from weather import Weather

from meme_class import Meme
from authenticate import RESPONSE_TYPE
from quotes_class import Quotes


weather = Weather()
meme = Meme()
quotes_obj = Quotes()


def generate_whoah():
    """:)."""
    return 'WHOAH ' * random.randrange(0, 50)


def make_help_msg():
    """."""
    return RESPONSE_TYPE['MESSAGE'],\
        'Commands list : \n' +\
        'addquote : add a quote to the quote database. Format : msg *** author\n' +\
        'dictionary : Search for word. Usage :' +\
        '[meaning] [antonym] [synonym] [translate {language shortcut}] word\n' +\
        'fortune : display fortune\n' +\
        'hello : display a hello msg to the auhtor\n' +\
        'help : display this message\n' +\
        'invite : returns a invite for this server\n' +\
        'meme : display a random meme from server or the net\n' +\
        'quote : display a random quote from database\n' +\
        'repeat : display the message said after "repeat"\n' +\
        'stats : display total of messages sent by user\n' +\
        'stats_perc : display percentage of messages sent by user\n' +\
        'weather : diplay weather for location, default:sherbrooke\n' +\
        '<nothing> : Try it :)'


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
    return RESPONSE_TYPE['MESSAGE'], '%s => High : %s \u2103, Low: %s \u2103' %\
        (forecast.text(), _farenheit_to_celcius_(forecast.high()),
         _farenheit_to_celcius_(forecast.low()))


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
    return RESPONSE_TYPE['MESSAGE'], stre


def parse_commands(msg, author):
    """Function that parse the command and send a response if needed."""

    if msg.find('hello') == 0:
        return RESPONSE_TYPE['MESSAGE'], 'Hello %s' % author

    if msg.find('help') == 0:
        return make_help_msg()

    if msg.find('repeat') == 0:
        return RESPONSE_TYPE['MESSAGE'], msg[len('repeat'):]

    if msg.find('fortune') == 0:
        return RESPONSE_TYPE['MESSAGE'], 'Not implemented yet'

    if msg.find('dictionary') == 0:
        return search_dictionary(msg)

    if msg.find('addquote') == 0:
        return quotes_obj.add(msg[len('addquotes'):])

    if msg.find('quote') == 0:
        return quotes_obj.get()

    if msg.find('meme') == 0:
        return meme.get_meme()

    if msg.find('weather') == 0:
        return get_wheater_condition(msg)

    return RESPONSE_TYPE['MESSAGE'], generate_whoah()
