from discord.ext import commands
import os
import discord
import lib.genshin_data_accessors as genshin_data
import lib.genshin_trackers as genshin_tracker
import lib.MAL_request as MAL_req
import lib.music_bot as music
from lib.keep_online import keep_online

bot = commands.Bot(command_prefix = "!")

@bot.event
async def on_ready():
  genshin_tracker.db_update.start(bot)
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
  await genshin_data.materials_cmd(ctx)


@bot.command()
async def when(ctx, arg):
  await genshin_data.when_cmd(ctx, arg)


@bot.command()
async def resin(ctx):
  await genshin_tracker.resin_cmd(ctx, bot)


@bot.command()
async def transformer(ctx):
  await genshin_tracker.transformer_cmd(ctx)


@bot.command()
async def weeb(ctx):
  await MAL_req.ani_today_cmd(ctx)


@bot.command()
async def join(ctx):
  await music.join_cmd(ctx)


@bot.command()
async def leave(ctx):
  await music.leave_cmd(ctx)


keep_online()
bot.run(os.getenv('TOKEN'))