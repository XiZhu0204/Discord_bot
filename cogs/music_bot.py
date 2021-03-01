import discord
import youtube_dl
from discord.ext import commands

import lib.pretty_prints as pprint

def setup(bot):
  bot.add_cog(Music(bot))


class Music(commands.Cog):
  # ==================================================================================
  #                          Class Variables and Init
  # ==================================================================================
  def __init__(self, bot):
    self.bot = bot


  # ==================================================================================
  #                                   Static Methods
  # ==================================================================================
  @staticmethod
  def check_same_channel(ctx):
    user_vc = ctx.author.voice.channel
    bot_vc = ctx.voice_client.channel

    return user_vc == bot_vc


  # ==================================================================================
  #                                      Commands
  # ==================================================================================
  @commands.command()
  async def join(self, ctx):
    vc = ctx.author.voice.channel
    try:
      await vc.connect()
    except discord.ClientException:
      response = pprint.embed_str("Bot is already in another voice channel.")
      await ctx.send(embed = response)


  @commands.command()
  async def leave(self, ctx):
    await ctx.voice_client.disconnect()


  @commands.command()
  async def play(self, ctx, url):
    players = {}
    server = ctx.guild
    vc = ctx.voice_client
    player = await vc.create_ytdl_player(url)
    players[server.id] = player
    player.start()