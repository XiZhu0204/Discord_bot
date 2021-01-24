

import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))


client = MyClient()
client.run("ODAzMDI3NDM1MzM0Nzk1MzE1.YA3zlA.QASxewJ5wU0quaVA16qflxMZcFA")
