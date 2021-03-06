from discord.ext import commands
import discord
import logging
import traceback
import sys
import json, asyncio
from collections import Counter
import datetime

description = """
Beatrice.
"""

initial_extensions =[
    'cogs.maid_cog'
]

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='beatrice.log', encoding='utf-8', mode='a')
log.addHandler(handler)

help_attrs = dict(hidden=True)

prefix = ['maid.']
bot = commands.Bot(command_prefix=prefix, description=description, pm_help=None, help_attrs=help_attrs)

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.author, 'Sorry. This command is disabled and cannot be used.')
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)

@bot.event
async def on_ready():
    print('Logged in as:')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('------')
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()

@bot.event
async def on_command(command, ctx):
    bot.commands_used[command.name] += 1
    message = ctx.message
    destination = None

    #if message.channel.is_private:
    #    destination = 'Private Message'
    #else:
    #    destination = '#{0.channel.name} ({0.server.name})'.format(message)
    #log.info('{0.timestamp}: {0.author.name} in {1}: {0.content}'.format(message, destination))

@bot.event
async def on_resumed():
    print('resumed...')

@bot.event
async def on_message(message):
    if message.channel.is_private:
        destination = 'Private Message'
    else:
        destination = '#{0.channel.name} ({0.server.name})'.format(message)
    #log.info('{0.timestamp}: {0.author.name} in {1}: {0.content}'.format(message, destination))
    if message.author.bot:
        return

    await bot.process_commands(message)


def load_credentials():
    with open('credentials.json') as f:
        return json.load(f)

if __name__ == '__main__':
    if any('debug' in arg.lower() for arg in sys.argv):
        bot.command_prefix = '$'

    #credentials = load_credentials()
    #bot.client_id = credentials['client_id']
    bot.commands_used = Counter()
    #bot.carbon_key = credentials['carbon_key']
    #bot.bots_key = credentials['bots_key']
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

bot.run("maid.saika.totsuka@gmail.com", "itachi123")
handlers = log.handlers[:]
for hdlr in handlers:
    hdlr.close()
    log.removeHandler(hdlr)