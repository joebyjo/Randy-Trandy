import discord
from discord.ext import commands
import praw
import random
from json import loads
from asyncio import TimeoutError
from urllib3 import exceptions, disable_warnings
from config import *
from discord.colour import Colour
from html import unescape

r = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                client_secret=REDDIT_CLIENT_SECRET,
                user_agent=REDDIT_USER_AGENT)


# todo https://some-random-api.ml/
# todo Snipe command
# todo See how dank you are, 100% official dank score
# todo Hack your friends! Or your enemies...
# todo Answer some trivia for a chance to win some coins.


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

        disable_warnings(exceptions.InsecureRequestWarning)

    @commands.command(aliases=['emoji', 'ep'])
    async def emojipictionary(self, ctx, topic):

        async def question_converter(word):
            new_word = ""
            for i in word:
                if i.isalnum():
                    new_word += "⸺ "
                elif i.isspace():
                    new_word += "   "
                else:
                    new_word += "⸺ "
            return new_word

        async def answer():
            user_input = await self.client.wait_for('message', check=lambda ms: ms.channel == ctx.channel, timeout=time)
            users_answer = user_input.content.lower()
            await user_input.delete()
            if users_answer == word:
                await ctx.send(f"**{user_input.author.mention} Got it correct!!**\nThe correct answer was `{word}`")
            else:
                await answer()

        topics = {'countries': {"Wales": " 🐳", "Oman": "⭕👨", "Iceland": "❄️🏝️", "Chile": "🌶️", "Turkey": "🦃",
                                "Taiwan": "👔 🚐", "Cuba": "🎲 🅰️"},
                  "movies": {"Dumbo": "🐘 🎪", "Up": "🎈🏠", "Finding Nemo": " 🔎🐠", "Lion King": "🦁 👑",
                             "Snakes on a plane": "🐍 ✈️", "American Pie": "🇺🇸 🥧"}
                  }

        time = 20
        word, emoji = random.choice(list(topics[topic].items()))
        word = word.lower()

        em_title = discord.Embed(title="Emoji Pictionary", colour=Colour.random())
        em_title.add_field(name=f"Topic: ", value=f'```\n{topic} \n```')
        em_title.add_field(name=f"Time: ", value=f'```\n{time}sec \n```')
        em_blanks = discord.Embed(description=f'```\n{await question_converter(word)} \n```', colour=Colour(0x2f3136))
        await ctx.send(embed=em_title)
        await ctx.send(f"{emoji}")
        await ctx.send(embed=em_blanks)

        await answer()

    @commands.command()
    async def gayrate(self, ctx, member: discord.Member):
        # member = member or ctx.author
        gayrate = random.randint(0, 100)
        color = Colour.random()
        embed = discord.Embed(title=f"How Gay are you?", description=f"{member.display_name} is {gayrate}% gay 🌈",
                              color=color)  # ,colour='green'
        await ctx.send(embed=embed)

    @commands.command(name='pp', aliases=['penis', 'pprate'])
    async def ppsize(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        size = random.randint(0, 25)
        color = Colour.random()
        embed = discord.Embed(title=f"{member.display_name}'s pp size", description=f'''8{'=' * size}D''',
                              color=color)  # ,colour='green'
        await ctx.send(embed=embed)

    @commands.command()
    async def simprate(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        simprate = random.randint(0, 100)
        color = Colour.random()
        embed = discord.Embed(title=f"Simp Rate",
                              description=f"{member.display_name} is {simprate}% simp",
                              color=color)  # ,colour='green'
        await ctx.send(embed=embed)

    @commands.command()
    async def lenny(self, ctx):
        """Displays a random lenny face."""

        async with self.client.session.get('https://api.lenny.today/v1/random', verify_ssl=False) as req:
            req = loads(await req.read())
            lenny = req[0]['face']
            await ctx.send(lenny)

    @commands.command()
    @commands.cooldown(rate=1, per=15.0)
    async def trivia(self, ctx):
        """trivia"""

        async with self.client.session.get('https://opentdb.com/api.php?amount=1&type=multiple',
                                           verify_ssl=False) as req:
            req = loads(await req.read())
            category = req['results'][0]['category']
            difficulty = req['results'][0]['difficulty']
            correct_answer = unescape(req['results'][0]['correct_answer'])
            incorrect_answers = req['results'][0]['incorrect_answers']
            question = unescape(req['results'][0]['question'])

        incorrect_answers.append(correct_answer)
        random.shuffle(incorrect_answers)

        options = {'a': unescape(incorrect_answers[0]),
                   'b': unescape(incorrect_answers[1]),
                   'c': unescape(incorrect_answers[2]),
                   'd': unescape(incorrect_answers[3])}

        em = discord.Embed(title=f'{question}', color=Colour.random())
        em.set_author(name=f"{ctx.author}\'s question", icon_url=ctx.author.avatar_url)
        em.add_field(name='\u200b',
                     value=f"a){options['a']}\n b){options['b']}\n c){options['c']}\n d){options['d']}\n\u200b",
                     inline=False)
        em.add_field(name='Difficulty', value=f"`{difficulty}`")
        em.add_field(name="Category", value=f"`{category}`")
        em.set_footer(text='you have 10 seconds. use the letter of the correct answer')
        await ctx.send(embed=em)

        user_input = await self.client.wait_for('message', check=lambda msg: msg.author == ctx.author
                                                                             and msg.channel == ctx.channel, timeout=12)
        user_input = (user_input.content).lower()
        try:
            if options[user_input] == correct_answer:
                await ctx.send("Correct")
            elif options[user_input] != correct_answer:
                await ctx.send(f"Incorrect,the correct answer was **{correct_answer}**")
        except KeyError:
            await ctx.send(f"Invalid input,the correct answer was **{correct_answer}**")

    @commands.command(aliases=['ytcomment', 'yt', 'comment'])
    async def youtubecomment(self, ctx, *, comment: str):
        avatar = str(ctx.author.avatar_url).replace('webp', 'png')
        pay = {'avatar': avatar, 'username': str(ctx.author.display_name), 'comment': comment}
        async with self.client.session.get('https://some-random-api.ml/canvas/youtube-comment', params=pay) as req:
            emb = discord.Embed(color=Colour.random())
            emb.set_image(url=req.url)
            await ctx.send(embed=emb)

    @commands.command()
    async def doot(self, ctx, *, msg: str):
        msg = "\💀\🎺".join(msg.split(" "))
        await ctx.send(msg)

    @commands.command()
    async def clap(self, ctx, *, msg: str):
        if " " in msg:
            msg = "\👏".join(msg.split(" "))
        else:
            msg = list(msg)
            msg = "\👏".join(msg)

        await ctx.send(msg)

    @commands.command()
    async def uselessweb(self, ctx):
        async with self.client.session.get('https://pastebin.com/raw/guqjQtqn') as req:
            req = loads(await req.read())
            website = random.choice(req['uselessweb'])
        await ctx.send(website)

    @commands.command(name='8ball', aliases=['8b'])
    async def eightball(self, ctx, *, msg=None):

        async with self.client.session.get('https://pastebin.com/raw/guqjQtqn') as req:
            req = loads(await req.read())
            answer = random.choice(req['8ball'])
        await ctx.send(answer)

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

    @commands.command(hidden=True)
    @commands.is_owner()
    async def counterstrike(self, ctx, member: discord.Member):
        x = True
        count = 0
        while x:
            try:
                msg = await ctx.send(member.mention)
                await msg.delete()
                count += 1
            except Exception:
                x = False
                await ctx.send("you're welcome")
                print(count)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def test(self, ctx):
        await ctx.send("""```ansi\n\u001b[0;40m\u001b[1;32mThat's some cool formatted text right?```""")

    @commands.command()
    @commands.cooldown(rate=1, per=10.0)
    @commands.max_concurrency(2)
    async def memes(self, ctx, sub='memes', min_ups: int = 2000):
        ''' Gets a meme from r/memes'''

        def check_domain(url, blacklisted):
            for words in blacklisted:
                if words in url:
                    return True

        post = r.subreddit(sub).random()
        blacklisted = ['v.redd.it', 'youtube', 'redgifs']
        async with ctx.channel.typing():
            if post.ups >= int(min_ups) and not check_domain(post.url, blacklisted):
                title = post.title
                author = post.author
                pic_link = post.url
                url = "https://www.reddit.com/" + str(post.id)

                upvotes = post.ups

                embed = discord.Embed(title=title,
                                      description=f"<:upvote:772042657316864040>{upvotes}  💬{post.num_comments}",
                                      url=url,
                                      color=Colour.random())
                embed.set_image(url=pic_link)
                embed.set_author(name=f"u/{author}", url=f'https://www.reddit.com/user/{author}/',
                                 icon_url='https://i.redd.it/snoovatar/snoovatars/d53ac490-6219-4e83-8115'
                                          '-deee7ec9e325.png')

                embed.set_footer(text=f""" requested by {ctx.author}""", icon_url=ctx.author.avatar_url)

                await ctx.channel.send(embed=embed)

            elif check_domain(post.url, blacklisted) and post.ups >= int(min_ups):
                title = post.title
                author = post.author
                # pic_link = post.url
                url = "https://www.reddit.com/" + str(post.id)

                upvotes = post.ups

                embed = discord.Embed(title=title,
                                      description=f"<:upvote:772042657316864040>{upvotes}  💬{post.num_comments}",
                                      url=url,
                                      color=Colour.random())
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

    @commands.command(aliases=['xno'])
    async def tictactoe(self, ctx, player2: discord.Member):
        board = ['<:white_large_1:809754969182961694>',
                 '<:white_large_2:809754991291006986>',
                 '<:white_large_3:809755010527264768>',
                 '<:white_large_4:809755035708686336>',
                 '<:white_large_5:809755054336507915>',
                 '<:white_large_6:809755072387874836>',
                 '<:white_large_7:809755091409043456>',
                 '<:white_large_8:809755130043301958>',
                 '<:white_large_9:809755162847477801>']

        winningConditions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        X = [':regional_indicator_x:', ctx.author]
        O = [':o2:', player2]
        game_over = False
        current_player = O

        async def send_board():
            return await ctx.send(
                f'{board[0] + board[1] + board[2]}\n{board[3] + board[4] + board[5]}\n{board[6] + board[7] + board[8]}')

        async def make_move(position, player):
            position -= 1
            if board[position].startswith('<:white_large'):
                if player[0] == X[0]:
                    board[position] = X[0]
                elif player[0] == O[0]:
                    board[position] = O[0]
            else:
                try:
                    await ctx.send('That place is taken. Try again using numbers ranging from 1-9', delete_after=6)
                    user_input = await self.client.wait_for('message', check=lambda msg: msg.author == current_player[
                        1] and msg.channel == ctx.channel, timeout=20)
                    await make_move(int(user_input.content), player)
                except TimeoutError:
                    await ctx.send("The game ended cuz you took too long to make a move")

        async def check_win(mark):
            for condition in winningConditions:
                if board[condition[0]] == mark[0] and board[condition[1]] == mark[0] and board[condition[2]] == mark[0]:
                    await ctx.send(f"{mark[1].mention}({mark[0]}) has won")
                    return True

        async def check_tie():
            count = 0
            for cell in board:
                if cell.startswith("<:white_large"):
                    return False
                elif not cell.startswith("<:white_large"):
                    count += 1

            if count == len(board):
                await ctx.send("The game has ended in a draw")
                return True

        async def switch_player(current_player):
            if current_player[0] == X[0]:
                current_player = O
                return current_player
            elif current_player[0] == O[0]:
                current_player = X
                return current_player

        async def choice():
            user_input = await self.client.wait_for('message', check=lambda msg: msg.author == current_player[
                1] and msg.channel == ctx.channel, timeout=20)
            try:
                await user_input.delete()  #
                user_input = int(user_input.content)
                return user_input
            except ValueError:
                await ctx.send("Only numbers from 1-9")
                return await choice()

        sent_board = await send_board()
        turn = await ctx.send(f"{X[1].mention}'s turn")
        while not game_over and not await check_tie():
            current_player = await switch_player(current_player)
            await turn.edit(content=f"{current_player[1].mention}'s turn")
            user_input = await choice()
            await make_move(user_input, current_player)
            await sent_board.edit(
                content=f"{board[0] + board[1] + board[2]}\n{board[3] + board[4] + board[5]}\n{board[6] + board[7] + board[8]}\n")
            game_over = bool(await check_win(current_player))

    @tictactoe.error
    async def tictactoe_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        if isinstance(error, TimeoutError):
            await ctx.send("The game ended cuz you took too long to make a move")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Mention a player to play against** \n*ps you can mention yourself too*",
                           delete_after=5)

        elif isinstance(error, commands.BadArgument):
            await ctx.send("You have to mention a User to play against", delete_after=10)

        else:
            await ctx.send(f"`Error: {error}`")

    @emojipictionary.error
    async def emojipictionary_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Choose one of the following topics",
                           delete_after=9)


# ------------------------------------------ Load Cog ------------------------------------------ #

def setup(client):
    client.add_cog(Fun(client))
