import discord
from discord.ext import commands
from Cogs.CounterBot import CounterBot
from config import DISCORD_CLIENT_ID
import json
from discord.colour import Colour


class ModTools(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def prefix(self, ctx, *, prefix):
        """    Changes server prefix """
        users = CounterBot(commands.Cog).open_json()
        users[str(ctx.guild.id)]['Guild prefix'] = prefix
        with open("Guilds.json", 'w') as f:
            json.dump(obj=users, fp=f, indent=4)

        await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def addguild(self, ctx):
        """     Adds guild to Guilds.json"""
        invite = str(await ctx.guild.channels[1].create_invite())
        CounterBot(commands.Cog).add_guild(ctx.guild, invite)
        for user in ctx.guild.members:
            CounterBot(commands.Cog).add_member(user)
        await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def addbruh(self, ctx, count: int = 1, member: discord.Member = None):
        """     Adds `bruh` for a certain user"""
        member = member or ctx.author
        CounterBot(commands.Cog).add_bruh(member=member, count=count)
        await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def addlol(self, ctx, count: int = 1, member: discord.Member = None):
        """     Adds `Lol` for a certain user"""
        member = member or ctx.author
        CounterBot(commands.Cog).add_lol(member=member, count=count)
        await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command()
    async def invite(self,ctx):
        bot_invite = discord.utils.oauth_url(client_id=DISCORD_CLIENT_ID,permissions=discord.Permissions(8))
        embed = discord.Embed(title='Invite me to your server', colour=Colour.random(), url=bot_invite)
        await ctx.send(embed=embed)


# ------------------------------------------ Load Cog ------------------------------------------ #

def setup(client):
    client.add_cog(ModTools(client))
