import discord
import os
from config import DISCORD_TOKEN
from Messages_bot import *
from Cogs.TypingSpeed import *

token = DISCORD_TOKEN
client = commands.Bot(command_prefix='=')

# todo use exit() to stop bot
# todo use try except to error handle
# todo roast bot(check dank memer)
# todo timetable
# todo battleship by sending messages to dms
# todo get period
# todo clean up eval function
# todo watch live youtbe/twitch streams after joing a vc and the bot starts to stream
# todo discord play minecraft

@client.event
async def on_ready():
    for ext in os.listdir('Cogs'):
        if ext.endswith('.py'):  # makesure __pycache__ doesnt gets loaded
            ext = ext[:-3]  # removes the .py because listdir returns with the file extension
            print(ext)
            client.load_extension(f'Cogs.{ext}')  # loads all the extensions in cogs folder

    await client.get_channel(783994812466593812).send('Bot is ready')  # 783994812466593812 - Bot channel , 760069306708131860 - Admin channel


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(Command_doesnt_exist())


@client.command()
async def ping(ctx):
    await ctx.send(f'ping {round(client.latency * 1000)} ms <:husk:768531113278046208>')  # sends the ping


@client.command()
async def clean(ctx, amount=0):  # deletes specified amount of messages
    await ctx.channel.purge(limit=int(amount) + 1)
    await ctx.send(f"` Deleted  {amount} messages `")


@clean.error
async def clean_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(Clean_error())


@client.command(name='eval')
async def _eval(ctx, *, cmd):
    result = eval(cmd)

    await ctx.send(f"{result}")


@client.command(name='run')
@commands.is_owner()
async def __exec(ctx, *, msg):
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.message.delete()
    msg = msg.replace("“", "\"")
    msg = msg.replace("‘", "'")
    try:
        exec(
            f'async def __ex(ctx): ' +
            ''.join(f'\n {line}' for line in msg.split('\n'))
        )
        return await locals()['__ex'](ctx)
    except Exception as e:
        await ctx.send(e)


# @client.command()
# # @commands.has_role('Owner')
# async def load(ctx, extension):
#     await ctx.add_reaction("\N{THUMBS UP SIGN}")
#     client.load_extension(f'Cogs.{extension}')

@client.command(hidden=True)
async def load(ctx, *, module):
    try:
        client.load_extension(module)
    except commands.ExtensionError as e:
        await ctx.send(f'{e.__class__.__name__}: {e}')
    else:
        await ctx.send('\N{OK HAND SIGN}')

@client.command(hidden=True)
async def unload(ctx, *, module):
    try:
        client.unload_extension(module)
    except commands.ExtensionError as e:
        await ctx.send(f'{e.__class__.__name__}: {e}')
    else:
        await ctx.send('\N{OK HAND SIGN}')

client.run(token)
