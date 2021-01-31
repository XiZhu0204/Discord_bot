import discord
import os


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == client.user:
            return

        if "I am" in message.content:
            end_piece = message.content.split('I am')[-1]
            await message.channel.send(f'Hello{end_piece}! I am dad!')


def main():
    client = MyClient()
    client.run(os.getenv('TOKEN'))


if __name__ == "__main__":
    main()
