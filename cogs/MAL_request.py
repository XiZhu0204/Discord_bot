import pytz

from discord.ext import commands
from jikanpy import AioJikan

import lib.pretty_prints as pprint
from lib.time_functions import get_weekday


def setup(bot):
  bot.add_cog(MAL(bot))

class MAL(commands.Cog):
  # ==================================================================================
  #                          Class Variables and Init
  # ==================================================================================
  working_tz = pytz.timezone("Asia/Tokyo")

  def __init__(self, bot):
    self.bot = bot

  # ==================================================================================
  #                                      Commands
  # ==================================================================================
  @commands.command()
  async def weeb(self, ctx):
    weekday = get_weekday(self.working_tz).lower()
    async with AioJikan() as requester:
      ani_tdy = await requester.schedule(weekday)
    animes = []
    for entry in ani_tdy[weekday]:
      title = entry["title"]
      url = entry["url"]
      info = f"{title}\n{url}\n"
      animes.append(info)
    
    header = "The animes that come out today are:\n"
    response = pprint.code_block_list(animes, header = header)
    await ctx.send(response)