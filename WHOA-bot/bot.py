"""WHOAH bot script."""
import atexit
import discord
import bot_functions as bf

# CONSTANTS
STATS_F = "stats.p"
#

stats_count, quotes = bf.load_files()


def exit_handler():
    """Handle exit."""
    bf.save_files(stats_count, quotes)


atexit.register(exit_handler)
client = discord.Client()


@client.event
async def on_message(message):
    """Function to handle message."""
    # Message sent by our bot
    if message.author == client.user:
        return

    msg_tup = bf.is_command(message.content)
    if msg_tup[0]:
        if msg_tup[1].find('invite') == 0:
            invite = await client.create_invite(message.channel, max_age=15)
            await client.send_message(message.channel, invite)
            return

        val, msg = bf.parse_commands(msg_tup[1], message, client, stats_count, quotes)
        if msg != '' and val == 'message':
            await client.send_message(message.channel, msg)
        elif val == 'file':
            await client.send_file(message.channel, msg)
        bf.save_files(stats_count, quotes)
        return

    msg = bf.formatted_correctly(message)
    if msg != '':
        await client.send_message(message.channel, msg)

    # Stats stuff
    if message.author.mention not in stats_count:
        stats_count[message.author.mention] = 0
    stats_count[message.author.mention] += 1
    bf.save_files(stats_count, quotes)


@client.event
async def on_ready():
    """Function when start up."""
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(bf.get_token())
