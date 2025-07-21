import discord
from discord.ext import commands
import asyncio


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client



# ------------------------------------------ Load Cog ------------------------------------------ #

def setup(client):
    client.add_cog(Games(client))
