import discord
from discord.ext import commands
import asyncio
from json import loads
import random
from discord import Colour
from Cogs.CounterBot import *


# todo typing speed user_input ..... Message has .created_at
# todo text generator
# todo leaderboard


class Typing(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def typingspeed(self, ctx):
        user_input = None
        color = Colour.random()
        text = await self.get_text()

        emb = discord.Embed(description=f"```yaml\n{text}\n```", colour=color)
        emb.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=emb)

        def is_correct(m):
            return m.author == ctx.author

        try:
            user_input = await self.client.wait_for('message', check=is_correct, timeout=20)  # returns of Message class
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond")

        # todo have to find a way to account for client latency

        timetaken = round((user_input.created_at - msg.created_at).total_seconds(), 1)
        input_text = user_input.content
        await user_input.delete()

        if "\u200e " in user_input.content:
            await ctx.send("Nice Try but that ain't happening here")
        else:
            net_wpm = await Typing.net_wpm(input_text, text, timetaken)
            gross_wpm = await Typing.gross_wpm(input_text, timetaken)
            accuracy, errors = await Typing.accuracy(input_text, text)
            if not self.get_user_data(ctx.author) or (self.get_user_data(ctx.author))["net_wpm"] < net_wpm:
                self.add_typing_user(ctx.author, net_wpm, gross_wpm, accuracy, errors, timetaken,
                                     text.replace("\u200e ", " "))

            em = discord.Embed(colour=color)
            # em.set_author(name=f"{ctx.author}\'s Results", icon_url=ctx.author.avatar_url)
            em.add_field(name=f"Entered Text: ", value=f"```fix\n{input_text}\n```", inline=False)
            em.add_field(name=f"Net Wpm:", value=f"```css\n{net_wpm} wpm\n```")
            em.add_field(name=f"Accuracy:", value=f"```css\n{accuracy} %\n```")
            em.add_field(name=f"Gross Wpm:", value=f"```css\n{gross_wpm} wpm\n```")
            em.add_field(name=f"Time Taken:", value=f"```css\n{timetaken} seconds\n```")
            em.add_field(name=f"Errors:", value=f"```css\n{errors}\n```")

            await ctx.send(embed=em)

    @staticmethod
    async def accuracy(input_text, text):
        text = text.replace("\u200e ", " ")
        error = 0

        text_lst = text.split()
        inp_lst = input_text.split()

        for i, c in enumerate(text_lst):
            for itr, cont in enumerate(c):
                try:
                    if inp_lst[i][itr] == cont:
                        continue

                    elif inp_lst[i][itr] != cont:
                        error += 1

                except IndexError:
                    pass

        if len(input_text) > len(text):
            error += 2 * (len(input_text) - len(text))

        accuracy = ((len(input_text) - error) / len(text)) * 100

        if accuracy < 0:
            accuracy = 0.0

        return round(accuracy), error

    @staticmethod
    async def gross_wpm(input_text, total_time):
        wpm = len(input_text) * 60 / (5 * total_time)
        return round(wpm)

    @staticmethod
    async def net_wpm(input_text, text, total_time):
        errors = (await Typing.accuracy(input_text, text))[1]
        wpm = ((len(input_text) - errors) * 60) / (total_time * 5)
        if wpm > 0:
            return round(wpm)
        else:
            return 0

    async def get_text(self):
        async with self.client.session.get("https://rentry.co/6dabk/raw") as req:
            req = loads(await req.read())
        words = []
        x = 5
        for i in range(x):
            word = random.choice(req['WordList'])
            if word not in words:
                words.append(word)
            else:
                x += 1
                continue

        return '\u200e '.join(words)

    def add_typing_user(self, member, net_wpm, gross_wpm, accuracy, errors, timetaken, text):
        users = CounterBot.open_json()
        user = users[str(member.guild.id)]['Typing Speed']

        if any(d["id"] == str(member.id) for d in user):
            for i in range(len(user)):
                if user[i].get("id") == str(member.id):
                    user[i]["net_wpm"] = net_wpm
                    user[i]["gross_wpm"] = gross_wpm
                    user[i]["accuracy"] = accuracy
                    user[i]["errors"] = errors
                    user[i]["timetaken"] = timetaken
                    user[i]["text"] = text

        else:
            user.append({"user": f"{member.name}#{member.discriminator}",
                         "id": str(member.id),
                         "net_wpm": net_wpm,
                         "gross_wpm": gross_wpm,
                         "accuracy": accuracy,
                         "errors": errors,
                         "timetaken": timetaken,
                         "text": text})

        with open("Guilds.json", 'w') as f:
            json.dump(obj=users, fp=f, indent=4)

    @staticmethod
    def get_user_data(member):
        user = CounterBot.open_json()
        users = user[str(member.guild.id)]['Typing Speed']

        if any(d["id"] == str(member.id) for d in users):
            for i in range(len(users)):
                if users[i].get("id") == str(member.id):
                    return users[i]
        else:
            return None

    @commands.command()
    async def typingscores(self, ctx, target=None):
        target = target or ctx.author
        data = self.get_user_data(target)
        user = data.get("user")
        net_wpm = data.get("net_wpm")
        gross_wpm = data.get("gross_wpm")
        accuracy = data.get("accuracy")
        errors = data.get("errors")
        timetaken = data.get("timetaken")
        text = data.get("text")

        em = discord.Embed(title=f"{user}'s Typing Highscore", colour=Colour.random())
        em.add_field(name=f"Text: ", value=f"```fix\n{text}\n```", inline=False)
        em.add_field(name=f"Net Wpm:", value=f"```css\n{net_wpm} wpm\n```")
        em.add_field(name=f"Accuracy:", value=f"```css\n{accuracy} %\n```")
        em.add_field(name=f"Gross Wpm:", value=f"```css\n{gross_wpm} wpm\n```")
        em.add_field(name=f"Time Taken:", value=f"```css\n{timetaken} seconds\n```")
        em.add_field(name=f"Errors:", value=f"```css\n{errors}\n```")

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Typing(client))
