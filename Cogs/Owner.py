import discord
from discord.ext import commands
import textwrap
from traceback import format_exception
import contextlib
import io
from discord.ext.buttons import Paginator
from discord.colour import Colour


class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        if await self.client.is_owner(ctx.author):
            return True
        else:
            raise commands.NotOwner

    def clean_code(self, content):
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:])[:-3]
        else:
            return content

    @commands.command(name="run", aliases=["exec"], hidden=True)
    async def _eval(self, ctx, *, code):
        """ Runs code and sends the results in a paginated form"""

        code = self.clean_code(code)
        local_variables = {
            "discord": discord,
            "commands": commands,
            "bot": self.client,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables)

                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}\n-- {obj}\n"
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        pager = Pag(
            timeout=60,
            entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
            length=1,
            prefix="```py\n",
            suffix="```",
            colour=Colour.random()

        )

        await pager.start(ctx)

    @commands.command(hidden=True)
    async def close(self, ctx):
        """ Closes the bot"""
        embed = discord.Embed(title=f"`Closing bot...\n`",
                              color=Colour.random())
        await self.client.close()
        await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command(hidden=True)
    async def load(self, ctx, *, module: str):
        """ Loads Cog"""
        try:
            self.client.load_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command(hidden=True)
    async def unload(self, ctx, *, module: str):
        """ Unloads Cog"""
        try:
            self.client.unload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

    @commands.command(hidden=True)
    async def reload(self, ctx, *, module: str):
        """ Reloads Cog"""
        try:
            self.client.reload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.message.add_reaction("\N{THUMBS UP SIGN}")

# ------------------------------------------ Load Cog ------------------------------------------ #

def setup(client):
    client.add_cog(Owner(client))
