from discord.ext import commands
from replit import db

import lib.pretty_prints as pprint


def setup(bot):
  bot.add_cog(Owner(bot))

class Owner(commands.Cog):
  # ==================================================================================
  #                          Class Variables and Init
  # ==================================================================================
  def __init__(self, bot):
    self.bot = bot


  # ==================================================================================
  #                                       Events
  # ==================================================================================
  @commands.Cog.listener()
  async def on_ready(self):
    print(f"Logged on as {self.bot.user}!")


  # ==================================================================================
  #                                      Commands
  # ==================================================================================
  @commands.command(hidden = True)
  @commands.is_owner()
  async def load(self, ctx, cog_to_load):
    try:
      self.bot.load_extension(f"cogs.{cog_to_load}")
    except Exception as e:
      response = pprint.embed_str(f"ERROR: {type(e).__name__} - {e}")
      await ctx.send(embed = response)
    else:
      response = pprint.embed_str(f"Successfully loaded {cog_to_load}")
      await ctx.send(embed = response)


  @commands.command(hidden = True)
  @commands.is_owner()
  async def unload(self, ctx, cog_to_unload):
    try:
      self.bot.unload_extension(f"cogs.{cog_to_unload}")
    except Exception as e:
      response = pprint.embed_str(f"ERROR: {type(e).__name__} - {e}")
      await ctx.send(embed = response)
    else:
      response = pprint.embed_str(f"Successfully unloaded {cog_to_unload}")
      await ctx.send(embed = response)


  @commands.command(hidden = True)
  @commands.is_owner()
  async def reload(self, ctx, cog_to_reload):
    try:
      self.bot.reload_extension(f"cogs.{cog_to_reload}")
    except Exception as e:
      response = pprint.embed_str(f"ERROR: {type(e).__name__} - {e}")
      await ctx.send(embed = response)
    else:
      response = pprint.embed_str(f"Successfully reloaded {cog_to_reload}")
      await ctx.send(embed = response)

  @commands.command(hidden = True)
  @commands.is_owner()
  async def show_db(self, ctx):
    output = []
    for key in db.keys():
      msg = f"{key}: {db[key]}"
      output.append(msg)
    
    response = pprint.code_block_list(output)
    await ctx.send(response)
