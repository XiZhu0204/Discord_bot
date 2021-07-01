import json
import pytz
from discord.ext import commands

import lib.pretty_prints as pprint
import lib.time_functions as time_func


def setup(bot):
  bot.add_cog(Genshin_Data(bot))

class Genshin_Data(commands.Cog):
  # ==================================================================================
  #                          Class Variables and Init
  # ==================================================================================
  working_tz = pytz.timezone("Etc/GMT+8")
  with open("data.json") as f:
    data = json.load(f)

  def __init__(self, bot):
    self.bot = bot
  

  # ==================================================================================
  #                                  Class Methods
  # ==================================================================================
  def get_material_list(self):
    return self.data["mats_names"]

  def get_farmable_mats(self, day):
    return self.data["mats_by_weekday"][day]

  def find_farmable_day(self, mat):
    farmable_days = []

    for day in self.data["mats_by_weekday"]:
      if mat in self.data["mats_by_weekday"][day]:
        farmable_days.append(day)

    return farmable_days


  # ==================================================================================
  #                                      Commands
  # ==================================================================================
  @commands.command()
  async def mats(self, ctx):
    weekday = time_func.get_weekday(self.working_tz)
    if weekday == "Sunday":
      response = pprint.embed_str("It's Sunday.")
      await ctx.send(embed = response)
    else:
      list_of_mats = self.get_farmable_mats(weekday)
      header = "You can farm today:"
      response = pprint.embed_list(list_of_mats, header = header)
      await ctx.send(embed = response)


  @commands.command()
  async def when(self, ctx, arg):
    arg = arg.capitalize()
    material_list = self.get_material_list()
    if arg in material_list:
      list_of_days = self.find_farmable_day(arg)
      if list_of_days:
        list_of_days.append("Sunday")
        # non empty array, indicating that retrieval was successful
        header = f"{arg} can be farmed on:"
        response = pprint.embed_list(list_of_days, header = header)
        await ctx.send(embed = response)
      else:
        response = pprint.embed_str("Unexpected error. Try again.")
        await ctx.send(embed = response)
    elif arg == "Reset":
      hours, minutes = time_func.hours_minutes_till_midnight(self.working_tz)
      time_till_reset_str = f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}\nuntil daily reset"

      header = "There are"
      response = pprint.embed_str(time_till_reset_str, header = header)
      await ctx.send(embed = response)
    else:
      header = "Unknown material. The materials list is:"
      footer = "\nor get the time till daily reset with:\nReset"
      response = pprint.embed_list(material_list, header = header, footer = footer)
      await ctx.send(embed = response)
