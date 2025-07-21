import discord
from discord.ext import commands
from json import loads
from Cogs.CounterBot import *
from discord.colour import Colour


# todo checkuser
# todo Visualize any hex or rgb color
# todo Get an invite for the bot or to the support server. Also some extra links to use.
# todo whitelist/black listed channels

class Utils(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='dm')  # allows the user to send a dm to the mentioned user
    async def direct_message(self, ctx, member: discord.Member, *, message):
        await member.send(message)
        await ctx.message.delete()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'ping {round(self.client.latency * 1000)} ms <:husk:768531113278046208>')  # sends the ping

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def clean(self, ctx, amount: int = 0):  # deletes specified amount of messages
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"` Deleted {amount} messages `", delete_after=7.5)

    # @commands.command()
    # @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    # @commands.cooldown(rate=1, per=10.0)
    # @commands.max_concurrency(2)
    # async def count(self, ctx, member: discord.Member = None):
    #     await ctx.message.add_reaction("\N{THUMBS UP SIGN}")
    #     await ctx.send("This proccess may take a couple of Minutes depending on the number of messages sent")
    #     try:
    #         async with ctx.channel.typing():
    #             channel = ctx.channel
    #             messages = await channel.history(limit=None).flatten()
    #             count = 0
    #             if member is not None:
    #                 for message in messages:
    #                     if message.author == member:
    #                         count += 1
    #                 description = f"{member.mention} sent `{count}` messages in {channel.mention}"
    #             else:
    #                 count = len(messages)
    #                 description = f"There were `{count}` messages in {channel.mention}"
    #             embed = discord.Embed(
    #                 title="Total Messages",
    #                 colour=Colour.random(),
    #                 description=description)
    #             await ctx.send(embed=embed)
    #
    #     except Exception as e:
    #         await ctx.send(e)

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    @commands.cooldown(rate=1, per=10.0)
    @commands.max_concurrency(2)
    async def count(self, ctx, member: discord.Member = None):
        await ctx.message.add_reaction("\N{THUMBS UP SIGN}")
        await ctx.send("This proccess may take a couple of Minutes depending on the number of messages sent")
        try:
            async with ctx.channel.typing():
                channel = ctx.channel
                messages = await channel.history(limit=None).flatten()
                count = 0
                if member is not None:
                    for message in messages:
                        if message.author == member:
                            count += 1
                    description = f"{member.mention} sent `{count}` messages in {channel.mention}"
                else:
                    count = len(messages)
                    description = f"There were `{count}` messages in {channel.mention}"
                embed = discord.Embed(
                    title="Total Messages",
                    colour=Colour.random(),
                    description=description)
                await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(e)

    @commands.command()
    async def colorviewer(self, ctx, color: str):
        def clean_color(clr: str):
            if clr.startswith("#"):
                return clr[1:]
            else:
                return clr

        color = clean_color(color)
        payload = {'hex': color}
        async with self.client.session.get('https://some-random-api.ml/canvas/colorviewer',
                                           params=payload) as req:
            emb = discord.Embed(title=f"#{color.upper()}", color=int(color, 16))
            emb.set_image(url=req.url)
            await ctx.send(embed=emb)

    @commands.command(aliases=['b64'])
    async def base64(self, ctx, *, string: str):
        type = ''
        msg = ''
        await ctx.message.delete()
        if string.endswith('='):
            type = 'decode'
            async with self.client.session.get(f'https://some-random-api.ml/base64?decode={string}') as req:
                req = loads(await req.read())
                msg = req['text']

        else:
            type = 'encode'
            async with self.client.session.get(f'https://some-random-api.ml/base64?encode={string}') as req:
                req = loads(await req.read())
                msg = req['base64']

        embed = discord.Embed(title=f"{type}d message", description=(f"`{msg}`"), colour=Colour.random())
        await ctx.send(embed=embed)

    @commands.command()
    async def binary(self, ctx, *, string: str):
        type = ''
        msg = ''
        await ctx.message.delete()
        if '1' and '0' in string:
            type = 'decode'
            async with self.client.session.get(f'https://some-random-api.ml/binary?decode={string}') as req:
                req = loads(await req.read())
                msg = req['text']

        else:
            type = 'encode'
            async with self.client.session.get(f'https://some-random-api.ml/binary?text={string}') as req:
                req = loads(await req.read())
                msg = req['binary']

        embed = discord.Embed(title=f"{type}d message", description=(f"`{msg}`"), colour=Colour.random())
        await ctx.send(embed=embed)

    @commands.command()
    async def status(self, ctx, target: discord.Member = None):
        """     sends the member's "lol" and "bruh" count"""
        target = target or ctx.author

        if CounterBot(commands.Cog).check_member(target):
            member = CounterBot(commands.Cog).open_json()

            bruh_count = member[str(ctx.guild.id)]['Members'][str(target.id)]['bruh_count']
            lol_count = member[str(ctx.guild.id)]['Members'][str(target.id)]['lol_count']

            em = discord.Embed(title=f"{target.display_name}'s bruh count", colour=Colour.random())
            em.add_field(name='Bruh count', value=f'{bruh_count}')
            em.add_field(name='Lol count', value=f'{lol_count}')
            await ctx.send(embed=em)


# ------------------------------------------ Load Cog ------------------------------------------ #

def setup(client):
    client.add_cog(Utils(client))
