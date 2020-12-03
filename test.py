import config
import random
import asyncio

"""class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('$guess'):
            await message.channel.send('Guess a number between 1 and 10.')

            def is_correct(m):
                return m.author == message.author

            answer = random.randint(1, 10)

            try:
                guess = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send('Sorry, you took too long it was {}.'.format(answer))

            if int(guess.content) == answer:
                await message.channel.send('You are right!')
            else:
                await message.channel.send('Oops. It is actually {}.'.format(answer))
"""
def accuracy(sentence, input):
    sent_lst = list(sentence)
    count = 0

    # for letter in sentence:
    #     sent_lst.append(letter)

    for word in input:
        try:
            if word == sent_lst[count]:
                return True
            else:
                return False
        except IndexError:
            return False

        count += 1
    print(sent_lst)
    print(sentence)

accuracy('jok j','joe j')
