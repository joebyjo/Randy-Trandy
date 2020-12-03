from discord.ext import commands
import asyncio
import json


class Typing(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def typingspeed(self, ctx):
        user_input = None

        def is_correct(m):
            return m.author == ctx.author

        try:
            user_input = await self.client.wait_for('message', check=is_correct, timeout=20)  # returns of Message class
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond")

        timetaken = int(user_input.created_at.strftime('%-S')) - int(ctx.message.created_at.strftime('%-S'))
        await ctx.send(timetaken)



def setup(client):
    client.add_cog(Typing(client))
