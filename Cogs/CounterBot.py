import discord
from discord.ext import commands
# import asyncio
import json
# from discord.colour import Colour
# from Cogs.Utils import Utils


BOT_DEFAULT_PREFIX = '='


# todo bruh/lol bot.calculates how many bruh/lol u hve said
# todo add bruh rights to the admin
# todo bday bot
# todo fix status returning 1


class CounterBot(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.BOT_DEFAULT_PREFIX = BOT_DEFAULT_PREFIX

    @commands.Cog.listener()
    async def on_message(self, msg):
        """ Listens for "bruh" and "lol" """
        if not msg.author.bot:
            try:
                if 'bruh' in msg.content.lower():
                    self.add_bruh(msg.author)
                if 'lol' in msg.content.lower():
                    self.add_lol(msg.author)

            except KeyError:
                await msg.channel.send(f"{msg.author.mention} just said his first bruh/lol ")

    @staticmethod
    def open_json():
        File = "Guilds.json"
        with open(File, 'r') as f:
            users = json.load(f)
        return users

    @staticmethod
    async def Invite(guild):
        """ Creates invite to the server"""
        try:
            Invite = str(await guild.system_channel.create_invite())
        except AttributeError:
            Invite = str(await guild.channels[1].create_invite())
        return Invite

    def add_guild(self, guild, invite):
        """ Adds guild to Guilds.json"""
        guilds = self.open_json()
        guilds[str(guild.id)] = {}
        guilds[str(guild.id)]['Guild Name'] = f'{guild.name}'
        guilds[str(guild.id)]['Owner'] = f'{guild.owner}'
        guilds[str(guild.id)]['Region'] = f'{guild.region}'
        guilds[str(guild.id)]['Guild Invite'] = f'{invite}'
        guilds[str(guild.id)]['Created at'] = f'{guild.created_at}'
        guilds[str(guild.id)]['Total members'] = f'{guild.member_count}'
        guilds[str(guild.id)]['Total Text Channels'] = f'{len(guild.text_channels)}'
        guilds[str(guild.id)]['Total Voice Channels'] = f'{len(guild.voice_channels)}'
        guilds[str(guild.id)]['Total Number of Roles'] = f'{len(guild.roles)}'
        guilds[str(guild.id)]['Guild prefix'] = f'{BOT_DEFAULT_PREFIX}'
        guilds[str(guild.id)]['Members'] = {}
        guilds[str(guild.id)]['Typing Speed'] = []

        with open("Guilds.json", 'w') as f:
            json.dump(obj=guilds, fp=f, indent=4)

    def check_guild(self, guild):
        """ Checks if guild exists in Guilds.json"""
        guilds = self.open_json()
        if guild.id in guilds:
            return True
        else:
            self.add_guild(guild, self.Invite)

    def add_member(self, member):
        """ Adds the member to Guilds.json"""
        users = self.open_json()
        if not member.bot:
            users[str(member.guild.id)]['Members'][str(member.id)] = {}
            users[str(member.guild.id)]['Members'][str(member.id)]['username'] = f"{member.name}#{member.discriminator}"
            users[str(member.guild.id)]['Members'][str(member.id)]['nickname'] = str(member.display_name)
            users[str(member.guild.id)]['Members'][str(member.id)]['joined discord'] = f"""{member.created_at}"""
            users[str(member.guild.id)]['Members'][str(member.id)]['joined server'] = f"{member.joined_at}"
            users[str(member.guild.id)]['Members'][str(member.id)]["bruh_count"] = 1
            users[str(member.guild.id)]['Members'][str(member.id)]["lol_count"] = 1
            with open("Guilds.json", 'w') as f:
                json.dump(obj=users, fp=f, indent=4)

    def check_member(self, member):
        """ Checks if a member already exists in Guilds.json"""
        users = self.open_json()
        if str(member.id) in users[str(member.guild.id)]['Members']:
            return True
        else:
            self.add_member(member)

    @commands.command(hidden=True)
    async def update_user(self, ctx, member: discord.Member):
        """     Updates user in Guilds.json"""
        users = self.open_json()
        if str(member.id) in users[str(member.guild.id)]['Members']:
            users[str(member.guild.id)]['Members'][str(member.id)] = {}
            users[str(member.guild.id)]['Members'][str(member.id)]['username'] = f"{member.name}#{member.discriminator}"
            users[str(member.guild.id)]['Members'][str(member.id)]['nickname'] = str(member.display_name)
            users[str(member.guild.id)]['Members'][str(member.id)]['joined discord'] = f"""{member.created_at}"""
            users[str(member.guild.id)]['Members'][str(member.id)]['joined server'] = f"{member.joined_at}"
            users[str(member.guild.id)]['Members'][str(member.id)]["bruh_count"] += 0
            users[str(member.guild.id)]['Members'][str(member.id)]["lol_count"] += 0
            with open("Guilds.json", 'w') as f:
                json.dump(obj=users, fp=f, indent=4)

            try:
                await ctx.message.add_reaction("\N{THUMBS UP SIGN}")
            except Exception:
                pass
        else:
            self.add_member(member)

    def add_bruh(self, member, count: int = 1):  # add bruh rights to the admin
        """ Adds "bruh" for a certain user"""
        users = self.open_json()
        if self.check_member(member):
            users[str(member.guild.id)]['Members'][str(member.id)]["bruh_count"] += count

            with open("Guilds.json", 'w') as f:
                json.dump(obj=users, fp=f, indent=4)
        else:
            self.add_bruh(member=member, count=count)

    def add_lol(self, member, count=1):
        """ Adds "Lol" for a user"""
        users = self.open_json()
        if self.check_member(member):
            users[str(member.guild.id)]['Members'][str(member.id)]["lol_count"] += count
            with open("Guilds.json", 'w') as f:
                json.dump(obj=users, fp=f, indent=4)
        else:
            self.add_lol(member=member, count=count)

# ------------------------------------------ Load Cog ------------------------------------------ #


def setup(client):
    client.add_cog(CounterBot(client))
