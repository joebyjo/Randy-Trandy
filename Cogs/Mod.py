import discord
from discord.ext import commands
from Cogs.CounterBot import CounterBot
import json
from Cogs.Fun import random_color


class ModTools(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='run',hidden=True)
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def __exec(self, ctx, *, msg):
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
            await ctx.send(f" `{e}` ")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def prefix(self, ctx, *, prefix):
        users = CounterBot(commands.Cog).open_json()
        users[str(ctx.guild.id)]['Guild prefix'] = prefix
        with open("members.json", 'w') as f:
            json.dump(obj=users, fp=f, indent=4)

        await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def addguild(self, ctx):
        invite = str(await ctx.guild.channels[1].create_invite())
        CounterBot(commands.Cog).check_guild(ctx.guild, invite)
        for user in ctx.guild.members:
            CounterBot(commands.Cog).check_member(user)
        await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def addbruh(self, ctx, count: int = 1, member: discord.Member = None):
        member = member or ctx.author
        CounterBot(commands.Cog).add_bruh(member=member, count=count)
        await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def addlol(self, ctx, count: int = 1, member: discord.Member = None):

        member = member or ctx.author

        CounterBot(commands.Cog).add_lol(member=member, count=count)
        await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, *, module: str):
        try:
            self.client.load_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, *, module: str):
        try:
            self.client.unload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, *, module: str):
        try:
            self.client.reload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command()
    @commands.is_owner()
    async def close(self, ctx):
        await self.client.close()
        await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx):
        em = discord.Embed(title='test', color=random_color())
        await ctx.send(embed=em)



def setup(client):
    client.add_cog(ModTools(client))
