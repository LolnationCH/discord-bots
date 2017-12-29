"""Functions for the bot."""
from math import ceil
import random

from PyDictionary import PyDictionary
from weather import Weather

from meme_class import Meme
from ressource import RESPONSE_TYPE
from quotes_class import Quotes


weather = Weather()
meme = Meme()
quotes_obj = Quotes()


def generate_whoah():
    """:)."""
    return 'WHOA ' * random.randrange(0, 50)


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


def get_wheater_condition(msg='sherbrooke'):
    """Parse to get weather info."""
    location = weather.lookup_by_location(msg)
    forecast = location.forecast()[0]
    return RESPONSE_TYPE['MESSAGE'], '%s\n%s => High : %s \u2103, Low: %s \u2103' %\
        (msg.title(), forecast.text(), _farenheit_to_celcius_(forecast.high()),
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


def do_repeat(msg):
    """."""
    return RESPONSE_TYPE['MESSAGE'], msg


def get_fortune():
    """."""
    return RESPONSE_TYPE['MESSAGE'], 'Not implemented yet'


COMMAND_LIST = {
    'help': make_help_msg,
    'repeat': do_repeat,
    'fortune': get_fortune,
    'dictionary': search_dictionary,
    'addquote': quotes_obj.add,
    'quote': quotes_obj.get,
    'meme': meme.get_meme,
    'weather': get_wheater_condition}


def parse_commands(msg, author):
    """Function that parse the command and send a response if needed."""
    if msg.find('hello') == 0:
        return RESPONSE_TYPE['MESSAGE'], 'Hello %s' % author

    msg_cmd = msg.split(' ', 1)
    if msg_cmd[0] in COMMAND_LIST:
        try:
            return COMMAND_LIST[msg_cmd[0]](msg_cmd[1])
        except IndexError:
            return COMMAND_LIST[msg_cmd[0]]()

    return RESPONSE_TYPE['MESSAGE'], generate_whoah()
