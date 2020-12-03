import discord
from discord.ext import commands
import praw
import random
from config import *
from Messages_bot import *

r = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                client_secret=REDDIT_CLIENT_SECRET,
                user_agent=REDDIT_USER_AGENT)


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, msg, min_upvotes: int = 2000):

        if msg.content.startswith('r/') and not msg.author.bot:
            await msg.add_reaction("\N{THUMBS UP SIGN}")
            x = msg.content.split(" ")
            subreddit = x[0]
            subreddit = subreddit[2:]
            if len(x) > 1:
                min_upvotes = int(x[1])
            await self.memes(msg, sub=subreddit, min_ups=min_upvotes)
        # await client.process_commands(msg)

    @commands.command()
    async def gayrate(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        gayrate = random.randint(0, 100)
        color = random_color()
        embed = discord.Embed(title=f"How Gay are you?", description=f"{member.display_name} is {gayrate}% gay 🌈",
                              color=color)  # ,colour='green'
        await ctx.send(embed=embed)

    @commands.command(name='pp', aliases=['penis', 'pprate'])
    async def ppsize(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        size = random.randint(0, 25)
        color = random_color()
        embed = discord.Embed(title=f"{member.display_name}'s pp size", description=f'''8{'=' * size}D''',
                              color=color)  # ,colour='green'
        await ctx.send(embed=embed)

    @commands.command()
    async def simprate(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        simprate = random.randint(0, 100)
        color = random_color()
        embed = discord.Embed(title=f"How much of a Simp are you?",
                              description=f"{member.display_name} is {simprate}% simp",
                              color=color)  # ,colour='green'
        await ctx.send(embed=embed)

    @ppsize.error
    async def ppsize_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Don't forget to mentions someone")

    @commands.command()
    async def memes(self, ctx, sub='memes', min_ups: int = 2000):
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
        global emb
        if section.lower() == '10h':
            url = 'https://cdn.discordapp.com/attachments/757502326586998887/769467305460760576/ce6942ff-9758-4c3d-9cd'\
                  '6-e52f7abdd81b.png '
            emb = discord.Embed(title=f'{section} Timetable ', color=random_color())
            emb.set_image(url=url)

        elif section.lower() == '10g':
            url = 'https://cdn.discordapp.com/attachments/757502326586998887/769467305460760576/ce6942ff-9758-4c3d-9cd'\
                  '6-e52f7abdd81b.png '
            emb = discord.Embed(title=f'{section} Timetable ', color=random_color())
            emb.set_image(url=url)
        print('hello')
        await ctx.send(embed=emb)

    @commands.command(name='dm')  # allows the user to send a dm to the mentioned user
    async def direct_message(self, ctx, member: discord.Member, *, message):
        await member.send(message)
        await ctx.message.delete()


def setup(client):
    client.add_cog(Fun(client))
