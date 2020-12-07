import discord
import os
from config import *
from Messages_bot import *
from Cogs.TypingSpeed import *

token = DISCORD_TOKEN
intents = discord.Intents().all()
client = commands.Bot(command_prefix='=', owner_ids=OWNER_IDS, intents=intents)


# todo discord plays minecraft. https://www.dougdougw.com/twitch-plays-code
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

    await client.get_channel(BOT_CHANNEL).send('Bot is ready')  # BOT_CHANNEL is the id of the bot channel on my server


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(Command_doesnt_exist())
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Error: ` {error} `")

    else:
        await ctx.send(f"Error: ` {error} `")


client.run(token)
