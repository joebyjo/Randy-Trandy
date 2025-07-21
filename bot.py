import discord
from discord.ext import commands
import os
import aiohttp
from config import *
from Messages_bot import *
from Cogs.CounterBot import CounterBot
from discord.colour import Colour

# todo discord plays minecraft. https://www.dougdougw.com/twitch-plays-code
# todo try to use exit() to stop bot
# todo roast bot(check dank memer)
# todo timetable
# todo battleship by sending messages to dms
# todo get period
# todo clean up eval function
# todo watch live youtbe/twitch streams after joining a vc and the bot starts to stream
# todo bot channels


BOT_DEFAULT_PREFIX = '='  # default Bot prefix
token = DISCORD_TOKEN


def get_prefix(client, msg):  # returns customised bot prefix for server
    try:
        with open('Guilds.json', 'r') as f:
            prefixes = json.load(f)
            return prefixes[str(msg.guild.id)]['Guild prefix']
    except Exception:
        return BOT_DEFAULT_PREFIX


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def start(self, *args, **kwargs):
        self.session = aiohttp.ClientSession()
        await super().start(*args, **kwargs)

    async def close(self):
        await self.session.close()
        await super().close()


INTENTS = discord.Intents().all()
client = Bot(
    command_prefix=commands.when_mentioned_or(BOT_DEFAULT_PREFIX),
    owner_ids=OWNER_IDS,
    intents=INTENTS)


# -------------------------------- Event Triggers and Listeners -------------------------------- #

@client.event
async def on_ready():
    loaded_cogs = []
    blacklisted = ['Help.py', 'DiscordPlays.py', 'Game.py']  # 'TypingSpeed.py',
    for ext in os.listdir('Cogs'):
        if ext.endswith('.py') and ext not in blacklisted:
            ext = ext[:-3]  # removes the ".py"
            client.load_extension(f'Cogs.{ext}')  # loads all the extensions in the cogs folder
            loaded_cogs.append(ext)

    embed = discord.Embed(title=f'Bot is ready', description=f'**Loaded:** \n ```\n{loaded_cogs} \n```',
                          colour=Colour.random())

    await client.get_channel(BOT_CHANNEL).send(embed=embed,
                                               delete_after=20)  # BOT_CHANNEL is the id of the bot channel on my server


@client.event
async def on_message(msg):
    try:
        if msg.mentions[0] == client.user:
            pre = get_prefix(msg=msg, client=None)
            embed = discord.Embed(title=f'My prefix is `{pre}`', colour=Colour.random())
            await msg.channel.send(embed=embed)
    except:
        pass
    finally:
        await client.process_commands(msg)


@client.event
async def on_member_join(member):
    CounterBot(commands.Cog).add_member(member)


@client.event
async def on_member_remove(member):
    users = CounterBot(commands.Cog).open_json()  # test this function
    if CounterBot(commands.Cog).check_member(member):
        users[f"{member.guild.id}"]["Members"].pop(str(member.id))
        with open("Guilds.json", 'w') as f:
            json.dump(obj=users, fp=f, indent=4)


@client.event
async def on_invite_delete(invite):
    f = CounterBot.open_json()
    old_inv = f[str(invite.guild.id)]['Guild Invite']
    if old_inv == str(invite):
        new_inv = await CounterBot(commands.Cog).Invite(invite.guild)
        f[str(invite.guild.id)]['Guild Invite'] = f'{new_inv}'

        with open("Guilds.json", 'w') as file:
            json.dump(obj=f, fp=file, indent=4)


@client.event
async def on_guild_join(guild):
    invite = await CounterBot(commands.Cog).Invite(guild)
    CounterBot(commands.Cog).add_guild(guild, invite)
    f = CounterBot.open_json()
    for user in guild.members:
        CounterBot(commands.Cog).add_member(user)

    embed = discord.Embed(title=f'Bot Joined {guild.name}', url=invite)
    embed.add_field(name=f'Owner: ', value=f'{guild.owner}')
    embed.add_field(name=f'Total number of members: ', value=f'{guild.member_count}', inline=False)
    embed.add_field(name=f'Region: ', value=f'{guild.region}', inline=False)
    embed.add_field(name=f'Total text channels: ', value=f'{len(guild.text_channels)}', inline=False)
    embed.add_field(name=f'Total Voice channels: ', value=f'{len(guild.voice_channels)}', inline=False)
    embed.add_field(name=f'Total Roles: ', value=f'{len(guild.roles)}', inline=False)

    await client.get_channel(BOT_CHANNEL).send(embed=embed)


# --------------------------------------- Error Handling --------------------------------------- #

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if hasattr(ctx.command, 'on_error'):
        return

    elif isinstance(error, commands.CommandNotFound):
        def Command_doesnt_exist():
            choices = choice(['That command doesnt exist', 'That command doesnt exist you dumbfuk',
                              'WTF man,how many times do i have to tell you it doesnt exist',
                              'are you retarded?It doesnt fuking exist'])
            return choices

        embed = discord.Embed(title=Command_doesnt_exist(), colour=Colour.random())
        await ctx.send(embed=embed, delete_after=60)

    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(title='Check Arguments', colour=Colour.random())
        await ctx.send(embed=embed, delete_after=60)

    elif isinstance(error, commands.NotOwner):
        embed = discord.Embed(title='You are not the Owner of this Bot', colour=Colour.random())
        await ctx.send(embed=embed, delete_after=60)

    elif isinstance(error, commands.BotMissingPermissions):
        perms = error.missing_perms
        embed = discord.Embed(title=f'The bot does not have required Permissions\n Please give `{perms}` to the bot',
                              colour=Colour.random())
        await ctx.send(embed=embed, delete_after=60)

    else:
        await ctx.send(f"Error: ` {error} `", delete_after=60)


# ------------------------------------------ Run Code ------------------------------------------ #

if __name__ == '__main__':
    client.run(token)
