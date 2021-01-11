import discord
from discord.ext import commands
import sys
import contextlib
import io
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
    async def eval(self, ctx, *, code: str):
        try:
            if code.startswith('```py') and code.endswith('```'):
                code = code[5:-3]
            elif code.startswith('`') and code.endswith('`'):
                code = code[1:-1]

            @contextlib.contextmanager
            def evaluate(stdout=None):
                old = sys.stdout
                if stdout is None:
                    sys.stdout = io.StringIO()
                yield sys.stdout
                sys.stdout = old

            with evaluate() as e:
                exec(code, {})
            msg = await ctx.send('Evaluating...')
            await msg.delete()
            await ctx.send(f"{ctx.author.mention} Finished Evaluating!")
            embed = discord.Embed(title=f'Results: \n', description=e.getvalue(),
                                  color=discord.Colour.from_rgb(255, 221, 170))
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title='Ran into a error while evaluating...')
            embed.add_field(name='Error: ', value=str(e))
            await ctx.send(embed=embed)




#=run await ctx.send(str(await ctx.guild.system_channel.create_invite()))

def setup(client):
    client.add_cog(Utils(client))
