"""WHOAH bot script."""
import discord
from authenticate import get_token, RESPONSE_TYPE
from message_parsing import Message_parser

# Create the discord client object
client = discord.Client()
msg_parser = Message_parser()


# Call on every message on the server
@client.event
async def on_message(message):
    """Function to handle message."""
    # Message sent by our bot
    if message.author == client.user:
        return

    type_rep, response = msg_parser.parse_message(message)

    # This is an invite request
    if type_rep == 0:
        invite = await client.create_invite(message.channel, max_age=15)
        await client.send_message(message.channel, invite)
        return

    # This is a messaege/file to be sent
    elif type_rep > 0 and response != '':
        if type_rep == RESPONSE_TYPE['MESSAGE']:
            await client.send_message(message.channel, response)
        elif type_rep == RESPONSE_TYPE['FILE']:
            await client.send_file(message.channel, response)


# Call after the bot is done connecting to Discord
@client.event
async def on_ready():
    """Function when start up."""
    print('Logged in as')
    print('USERNAME : %s' % client.user.name)
    print('USER ID : %s' % client.user.id)
    print('------')


# Start the bot
client.run(get_token())
