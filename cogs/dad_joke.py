from discord.ext import commands


def setup(bot):
  bot.add_cog(Dad(bot))


class Dad(commands.Cog):
  # ==================================================================================
  #                          Class Variables and Init
  # ==================================================================================
  def __init__(self, bot):
    self.bot = bot

  
  # ==================================================================================
  #                                       Events
  # ==================================================================================
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author == self.bot.user:
      return

    if message.content.lower().startswith("i am ") or " i am " in message.content.lower():
      end_piece = message.content.lower().split('i am')[-1]
      await message.channel.send(f'Hello{end_piece}! I am dad!')

    elif message.content.lower().startswith("im ") or " im " in message.content.lower():
      end_piece = message.content.lower().split('im')[-1]
      await message.channel.send(f'Hello{end_piece}! I am dad!')

    elif message.content.lower().startswith("i'm ") or " i'm " in message.content.lower():
      end_piece = message.content.lower().split("i'm")[-1]
      await message.channel.send(f'Hello{end_piece}! I am dad!')