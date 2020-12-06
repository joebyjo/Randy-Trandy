import discord
from discord.ext import commands
import random
import sys
import contextlib
import io


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
    async def clean(self, ctx, amount=0):  # deletes specified amount of messages
        await ctx.channel.purge(limit=int(amount) + 1)
        await ctx.send(f"` Deleted  {amount} messages `")

    @clean.error
    async def clean_error(self, ctx, error):

        def Clean_error():
            choices = random.choice(
                ["Don't forget to specify the amount of messages to delete",
                 'you forgot the number of messages to delete',
                 'make sure all arguments are there'])
            return choices

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(Clean_error())

    @commands.command(name='run')
    @commands.is_owner()
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

    # @client.command(name='eval')
    # async def _eval(ctx, *, cmd):
    #     result = eval(cmd)
    #
    #     await ctx.send(f"{result}")

    # @client.command()
    # # @commands.has_role('Owner')
    # async def load(ctx, extension):
    #     await ctx.add_reaction("\N{THUMBS UP SIGN}")
    #     client.load_extension(f'Cogs.{extension}')

    @commands.command(hidden=True)
    async def load(self, ctx, *, module: str):
        try:
            self.client.load_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    async def unload(self, ctx, *, module: str):
        try:
            self.client.unload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')


def setup(client):
    client.add_cog(Utils(client))
