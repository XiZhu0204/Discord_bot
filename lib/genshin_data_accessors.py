import json
from datetime import datetime, timedelta
import pytz
import time

import lib.pretty_prints as pprint

DATE = datetime.now()
working_tz = pytz.timezone("America/Yakutat")

with open("data.json") as f:
  DATA = json.load(f)

def get_weekday():
  return DATA["weekday"][DATE.now(working_tz).weekday()]

def get_material_list():
  return DATA["mats_names"]

def get_farmable_mats(day):
  return DATA["mats_by_weekday"][day]

def find_farmable_day(mat):
  farmable_days = []

  for day in DATA["mats_by_weekday"]:
    if mat in DATA["mats_by_weekday"][day]:
      farmable_days.append(day)

  return farmable_days

async def materials_cmd(ctx):
  weekday = get_weekday()
  if weekday == "Sunday":
    response = pprint.code_block_str("It's Sunday you cringe kid.")
    await ctx.send(response)
  else:
    list_of_mats = get_farmable_mats(weekday)
    header = "You can waste your time today farming:"
    response = pprint.code_block_list(list_of_mats, header = header)
    await ctx.send(response)

async def when_cmd(ctx, arg):
  arg = arg.capitalize()
  material_list = get_material_list()
  if arg in material_list:
    list_of_days = find_farmable_day(arg)
    if list_of_days:
      # non empty array, indicating that retrieval was successful
      header = f"Greetings you gacha cringe, {arg} can be farmed on:"
      response = pprint.code_block_list(list_of_days, header = header, footer = "Sunday")
      await ctx.send(response)
    else:
      response = pprint.code_block_str("Unexpected error. Try again.")
      await ctx.send(response)
  elif arg == "Reset":
    tomorrow = datetime.now(working_tz) + timedelta(days = 1)
    reset = datetime(year = tomorrow.year, month = tomorrow.month, day = tomorrow.day,
                      hour = 0, minute = 0, second = 0, tzinfo = working_tz)
    time_till_reset = reset - datetime.now(working_tz)
    formattable_time_till_reset = time.gmtime(time_till_reset.total_seconds())
    time_till_reset_str = time.strftime('%H:%M', formattable_time_till_reset)

    header = "There are"
    footer = "until daily reset."
    response = pprint.code_block_str(time_till_reset_str, header = header, footer = footer)
    await ctx.send(response)
  else:
    header = "Spell correctly xd. The materials list is:"
    footer = "\nor get the time till daily reset with:\nReset"
    response = pprint.code_block_list(material_list, header = header, footer = footer)
    await ctx.send(response)