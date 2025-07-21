import discord
from discord.ext import commands
from pynput.keyboard import Controller, Key
import time
import pyautogui
import pynput


class DiscordPlays(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='walk')
    async def __w(self, ctx):
        pass
        kb = Controller()
        time.sleep(2)
        kb.type('w')
        kb.press(Key)


# ------------------------------------------ Load Cog ------------------------------------------ #

def setup(client):
    client.add_cog(DiscordPlays(client))
