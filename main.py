from discord.ext import commands
import os

from lib.genshin_data_accessors import materials_cmd, when_cmd
from lib.resin_tracker import increment_resin, resin_cmd
from lib.MAL_request import ani_today_cmd
from lib.keep_online import keep_online

bot = commands.Bot(command_prefix = "!")

@bot.event
async def on_ready():
  increment_resin.start(bot)
  print(f"Logged on as {bot.user}!")


@bot.event
async def on_message(message):
  if message.author == bot.user:
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

  await bot.process_commands(message)


@bot.command()
async def mats(ctx):
  await materials_cmd(ctx)


@bot.command()
async def when(ctx, arg):
  await when_cmd(ctx, arg)


@bot.command()
async def resin(ctx):
  await resin_cmd(ctx, bot)

@bot.command()
async def weeb(ctx):
  await ani_today_cmd(ctx)

keep_online()
bot.run(os.getenv('TOKEN'))