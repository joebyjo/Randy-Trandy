import discord
from discord.ext import commands
from Messages_bot import *
import json


class CounterBot(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, msg):

        try:
            if 'bruh' in msg.content.lower() and not msg.author.bot:
                self.add_bruh(msg.author)
            if 'lol' in msg.content.lower() and not msg.author.bot:
                self.add_lol(msg.author)

        except KeyError:
            await msg.channel.send(f"{msg.author.mention} just said his first bruh/lol ")

    @commands.command()
    async def status(self, ctx, target: discord.Member = None):
        if target is None:
            target = ctx.author

        if self.check_member(target):
            member = self.get_member_details()
            bruh_count = member[str(target.id)]['bruh_count']
            lol_count = member[str(target.id)]['lol_count']
            em = discord.Embed(title=f"{target.display_name}'s bruh count", colour=random_color())
            em.add_field(name='Bruh count', value=f'{bruh_count}')
            em.add_field(name='Lol count', value=f'{lol_count}')
            await ctx.send(embed=em)

    def get_member_details(self):
        File = "members.json"
        with open(File, 'r') as f:
            users = json.load(f)
        return users

    def check_member(self, member):
        users = self.get_member_details()
        if str(member.id) in users:
            return True

        else:
            users[str(member.id)] = {}
            users[str(member.id)]['username'] = str(member.name)
            users[str(member.id)]['nickname'] = str(member.display_name)
            users[str(member.id)]['joined discord'] = f"""{member.created_at.strftime("%H:%M %b-%d-%Y")}"""
            users[str(member.id)]['joined server'] = f"{member.joined_at}"
            users[str(member.id)]["bruh_count"] = 1
            users[str(member.id)]["lol_count"] = 1
            with open("members.json", 'w') as f:
                json.dump(obj=users, fp=f, indent=4)
            return True

    def add_bruh(self, member, count=1):  # add bruh rights to the admin
        users = self.get_member_details()
        if self.check_member(member):
            users[str(member.id)]["bruh_count"] += count
            with open("members.json", 'w') as f:
                json.dump(obj=users, fp=f, indent=4)
        else:
            self.add_bruh(member=member, count=count)

    def add_lol(self, member, count=1):
        users = self.get_member_details()
        if self.check_member(member):
            users[str(member.id)]["lol_count"] += count
            with open("members.json", 'w') as f:
                json.dump(obj=users, fp=f, indent=4)
        else:
            self.add_lol(member=member, count=count)


def setup(client):
    client.add_cog(CounterBot(client))
