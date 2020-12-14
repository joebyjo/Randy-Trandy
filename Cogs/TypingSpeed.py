from discord.ext import commands
import asyncio
import json


# todo typing speed user_input ..... Message has .created_at
# todo text generator
# todo leaderboard


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

        # todo have to find a way to account for client latency


        timetaken = int(user_input.created_at.strftime('%-S')) - int(ctx.message.created_at.strftime('%-S'))  # '%f'


        await ctx.send(timetaken)

    @staticmethod
    def accuracy(text, input_text):
        error = 0

        for i, c in enumerate(text):
            try:
                if input_text[i] == c:
                    continue

                elif input_text[i] != c:
                    error += 1

            except IndexError:
                error += 1

        if len(input_text) > len(text):
            error += (len(input_text) - len(text))

            # if len(input_text) < len(text):
            #     error += len(text) - len(input_text)

        accuracy = (len(input_text) - error) / len(input_text) * 100

        if accuracy < 0:
            accuracy = 0.0

        return accuracy

    @staticmethod
    def gross_wpm(input_text, total_time):
        wpm = len(input_text) * 60 / (5 * total_time)
        return wpm

    @staticmethod
    def net_wpm(input_text, text, total_time):
        errors = 0
        for i, c in enumerate(text):
            if input_text[i] != c:
                errors += 1

        wpm = (len(input_text) - errors) * 60 / (5 * total_time)

        return wpm




def setup(client):
    client.add_cog(Typing(client))
