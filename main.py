from discord.ext import commands
import os

from lib.keep_online import keep_online

bot = commands.Bot(command_prefix = "!")

for filename in os.listdir("./cogs"):
  if filename.endswith(".py"):
    bot.load_extension(f"cogs.{filename[:-3]}")

keep_online()
bot.run(os.getenv('TOKEN'))
