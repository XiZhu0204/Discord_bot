import json

import lib.common.pretty_prints as pprint
import lib.common.time_functions as time_func


with open("data.json") as f:
  DATA = json.load(f)

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
  weekday = time_func.get_weekday()
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
    hours, minutes = time_func.hours_minutes_till_midnight()
    time_till_reset_str = f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}"

    header = "There are"
    footer = "until daily reset."
    response = pprint.code_block_str(time_till_reset_str, header = header, footer = footer)
    await ctx.send(response)
  else:
    header = "Spell correctly xd. The materials list is:"
    footer = "\nor get the time till daily reset with:\nReset"
    response = pprint.code_block_list(material_list, header = header, footer = footer)
    await ctx.send(response)