import discord
from discord.ext import commands
import os
from config import *
from Messages_bot import *
from Cogs.CounterBot import CounterBot

BOT_DEFAULT_PREFIX = '='
token = DISCORD_TOKEN


def get_prefix(client, msg):
    try:
        with open('members.json', 'r') as f:
            prefixes = json.load(f)
            return prefixes[str(msg.guild.id)]['Guild prefix']
    except KeyError:
        return BOT_DEFAULT_PREFIX


INTENTS = discord.Intents().all()
client = commands.Bot(
    command_prefix=get_prefix,
    owner_ids=OWNER_IDS,
    intents=INTENTS,
    help_command=None)


# todo discord plays minecraft. https://www.dougdougw.com/twitch-plays-code
# todo try to use exit() to stop bot
# todo roast bot(check dank memer)
# todo timetable
# todo battleship by sending messages to dms
# todo get period
# todo clean up eval function
# todo watch live youtbe/twitch streams after joining a vc and the bot starts to stream
# todo bot channels

@client.event
async def on_ready():
    loaded_cogs = []
    blacklisted = []#'Help.py'
    for ext in os.listdir('Cogs'):
        if ext.endswith('.py') and ext not in blacklisted: # makesure __pycache__ doesnt gets loaded
            ext = ext[:-3]  # removes the .py because listdir returns with the file extension
            client.load_extension(f'Cogs.{ext}')  # loads all the extensions in the cogs folder
            loaded_cogs.append(ext)

    await client.get_channel(BOT_CHANNEL).send(f'Bot is ready.Loaded ` {loaded_cogs} `',
                                               delete_after=10)  # BOT_CHANNEL is the id of the bot channel on my server


#
# @client.event
# async def when_mentioned(msg):
#     prefix = get_prefix(client, msg)
#     await msg.channel.send(f" My prefix is ` {prefix} `")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        def Command_doesnt_exist():
            choices = choice(['That command doesnt exist', 'That command doesnt exist you dumbfuk',
                              'WTF man,how many times do i have to tell you it doesnt exist',
                              'are you retarded?It doesnt fuking exist'])
            return choices

        await ctx.send(Command_doesnt_exist())
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Error: ` {error} `", delete_after=60)

    else:
        await ctx.send(f"Error: ` {error} `", delete_after=60)


@client.event
async def on_member_join(member):
    CounterBot(commands.Cog).check_member(member)


@client.event
async def on_member_remove(member):
    users = CounterBot(commands.Cog).open_json()  # test this function
    if CounterBot(commands.Cog).check_member(member):
        users[f"{member.guild.id}"]["Members"].pop(str(member.id))
        with open("members.json", 'w') as f:
            json.dump(obj=users, fp=f, indent=4)


@client.event
async def on_guild_join(guild):
    invite = str(await guild.channels[1].create_invite())
    CounterBot(commands.Cog).check_guild(guild, invite)
    for user in guild.members:
        CounterBot(commands.Cog).check_member(user)

    embed = discord.Embed(title=f'Bot Joined {guild.name}', url=invite)
    embed.add_field(name=f'Owner: ', value=f'{guild.owner}')
    embed.add_field(name=f'Total number of members: ', value=f'{guild.member_count}', inline=False)
    embed.add_field(name=f'Region: ', value=f'{guild.region}', inline=False)
    embed.add_field(name=f'Total text channels: ', value=f'{len(guild.text_channels)}', inline=False)
    embed.add_field(name=f'Total Voice channels: ', value=f'{len(guild.voice_channels)}', inline=False)
    embed.add_field(name=f'Total Roles: ', value=f'{len(guild.roles)}', inline=False)

    await client.get_channel(BOT_CHANNEL).send(embed=embed)


client.run(token)
