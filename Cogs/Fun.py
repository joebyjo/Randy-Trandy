import discord
from discord.ext import commands
import praw
import random
from config import *
from Messages_bot import *


r = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                client_secret=REDDIT_CLIENT_SECRET,
                user_agent=REDDIT_USER_AGENT)


# todo https://some-random-api.ml/
# todo Make the bot say whatever you want with sass!
# todo See how dank you are, 100% official dank score
# todo Hack your friends! Or your enemies...
# todo See a random site from https://theuselessweb.com/
# todo Answer some trivia for a chance to win some coins.

def random_color():
    # 1000 possible colors
    with open('Cogs/colors.txt', 'r') as f:
        color = int(choice(f.readlines()),16)
    return color

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def gayrate(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        gayrate = random.randint(0, 100)
        color = random_color()
        embed = discord.Embed(title=f"How Gay are you?", description=f"{member.display_name} is {gayrate}% gay 🌈",
                              color=color)  # ,colour='green'
        await ctx.send(embed=embed)

    @commands.command(name='pp', aliases=['penis', 'pprate'])
    async def ppsize(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        size = random.randint(0, 25)
        color = random_color()
        embed = discord.Embed(title=f"{member.display_name}'s pp size", description=f'''8{'=' * size}D''',
                              color=color)  # ,colour='green'
        await ctx.send(embed=embed)


    @commands.command()
    async def simprate(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        simprate = random.randint(0, 100)
        color = random_color()
        embed = discord.Embed(title=f"How much of a Simp are you?",
                              description=f"{member.display_name} is {simprate}% simp",
                              color=color)  # ,colour='green'
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, msg, minimum_upvotes: int = 0):
        if msg.content.startswith('r/') and not msg.author.bot:
            await msg.add_reaction("\N{THUMBS UP SIGN}")
            x = msg.content.split(" ")
            subreddit = x[0]
            subreddit = subreddit[2:]
            if len(x) > 1:
                minimum_upvotes = int(x[1])
            try:
                await self.memes(msg, sub=subreddit, min_ups=minimum_upvotes)

            except Exception as e:
                await msg.channel.send(e)
        # await client.process_commands(msg)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0)
    @commands.max_concurrency(2)
    async def memes(self, ctx, sub='memes', min_ups: int = 2000):
        def check_domain(url, blacklisted):
            for words in blacklisted:
                if words in url:
                    return True
        in_sub = r.subreddit(sub).random()
        blacklisted = ['v.redd.it', 'youtube', 'redgifs']
        async with ctx.channel.typing():
            if in_sub.ups >= int(min_ups) and not check_domain(in_sub.url, blacklisted):
                title = in_sub.title
                author = in_sub.author
                pic_link = in_sub.url
                url = "https://www.reddit.com/" + str(in_sub.id)

                upvotes = in_sub.ups

                embed = discord.Embed(title=title,
                                      description=f"<:upvote:772042657316864040>{upvotes}  💬{in_sub.num_comments}",
                                      url=url,
                                      color=random_color())
                embed.set_image(url=pic_link)
                embed.set_author(name=f"u/{author}", url=f'https://www.reddit.com/user/{author}/',
                                 icon_url='https://i.redd.it/snoovatar/snoovatars/d53ac490-6219-4e83-8115'
                                          '-deee7ec9e325.png')

                embed.set_footer(text=f""" requested by {ctx.author}""", icon_url=ctx.author.avatar_url)

                await ctx.channel.send(embed=embed)

            elif check_domain(in_sub.url, blacklisted) and in_sub.ups >= int(min_ups):
                title = in_sub.title
                author = in_sub.author
                # pic_link = in_sub.url
                url = "https://www.reddit.com/" + str(in_sub.id)

                upvotes = in_sub.ups

                embed = discord.Embed(title=title,
                                      description=f"<:upvote:772042657316864040>{upvotes}  💬{in_sub.num_comments}",
                                      url=url,
                                      color=random_color())
                # emb.set_image(url=pic_link)
                embed.set_author(name=f"u/{author}", url=f'https://www.reddit.com/user/{author}/',
                                 icon_url='https://i.redd.it/snoovatar/snoovatars/d53ac490-6219-4e83-8115'
                                          '-deee7ec9e325.png')
                embed.add_field(name='The Post is hosted on an unsupported Domain',
                                value='**Click on the title to view the post** ')
                embed.set_footer(text=f""" requested by {ctx.author}""", icon_url=ctx.author.avatar_url)

                await ctx.channel.send(embed=embed)
            else:
                await self.memes(ctx=ctx, sub=sub, min_ups=min_ups)

    @commands.command()
    async def camel(self, ctx, *, msg):
        msg = list(msg)
        converted = []
        for x in msg:
            qt = random.randint(0, 1)
            if qt == 1:
                convert = x.upper()
                converted.append(convert)
            elif qt == 0:
                convert = x.lower()
                converted.append(convert)

        final = ''.join(converted)
        await ctx.send(final)

    @commands.command(hidden=True)
    async def timetable(self, ctx, section='10h'):
        global embed
        if section.lower() == '10h':
            url = 'https://cdn.discordapp.com/attachments/757502326586998887/769467305460760576/ce6942ff-9758-4c3d-9cd'\
                  '6-e52f7abdd81b.png '
            embed = discord.Embed(title=f'{section} Timetable ', color=random_color())
            embed.set_image(url=url)

        elif section.lower() == '10g':
            url = 'https://cdn.discordapp.com/attachments/757502326586998887/769467305460760576/ce6942ff-9758-4c3d-9cd'\
                  '6-e52f7abdd81b.png '
            embed = discord.Embed(title=f'{section} Timetable ', color=random_color())
            embed.set_image(url=url)
        print('hello')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
