"""WHOAH bot script."""
import discord
import bot_functions as bf
from stats_class import Stats_recorder
from authenticate import get_token

stats_obj = Stats_recorder()
client = discord.Client()


@client.event
async def on_message(message):
    """Function to handle message."""
    # Message sent by our bot
    if message.author == client.user:
        return

    # Check if message is command
    msg_tup = bf.is_command(message.content)
    if msg_tup[0]:
        if msg_tup[1].find('invite') == 0:
            invite = await client.create_invite(message.channel, max_age=15)
            await client.send_message(message.channel, invite)
            return

        val, msg = bf.parse_commands(msg_tup[1], message, client, stats_obj)
        if msg != '' and val == 'message':
            await client.send_message(message.channel, msg)
        elif val == 'file':
            await client.send_file(message.channel, msg)
        return

    # Not a command
    msg = bf.formatted_correctly(message)
    if msg != '':
        await client.send_message(message.channel, msg)

    stats.add(message.author.mention)


@client.event
async def on_ready():
    """Function when start up."""
    print('Logged in as')
    print('USERNAME : %s' % client.user.name)
    print('USER ID : %s' % client.user.id)
    print('------')


client.run(get_token())
