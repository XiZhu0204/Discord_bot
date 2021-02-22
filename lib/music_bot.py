import discord

import lib.common.pretty_prints as pprint

def check_same_channel(ctx):
  user_vc = ctx.author.voice.channel
  bot_vc = ctx.voice_client.channel

  return user_vc == bot_vc

async def join_cmd(ctx):
  vc = ctx.author.voice.channel
  try:
    await vc.connect()
  except discord.ClientException:
    await ctx.send(pprint.code_block_str("Bot is already in another voice channel."))

async def leave_cmd(ctx):
  await ctx.voice_client.disconnect()
