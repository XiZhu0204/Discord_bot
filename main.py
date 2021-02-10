from discord.ext import commands
import os

import lib.data_accessors as d_access
import lib.resin_tracker as resin
from lib.keep_online import keep_online

bot = commands.Bot(command_prefix = "!")

@bot.event
async def on_ready():
  resin.increment_resin.start()
  print('Logged on as {0}!'.format(bot.user))


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
async def materials(ctx):
  weekday = d_access.get_weekday()
  if weekday == "Sunday":
    await ctx.send("```\nIt's Sunday you cringe kid.\n```")
  else:
    list_of_mats = d_access.get_farmable_mats(weekday)
    response = "```\nYou can waste your time today farming:\n"
    for entry in list_of_mats:
      response += entry + "\n"
    response += "\n```"
    await ctx.send(response)


@bot.command()
async def when(ctx, arg):
  mat = arg.capitalize()
  list_of_days = d_access.find_farmable_day(mat)
  if list_of_days:
    # non empty array, indicating that retrieval was successful
    response = f"```\nGreetings you gacha cringe, {mat} can be farmed on:\n"
    for entry in list_of_days:
      response += entry + "\n"
    response += "Sunday\n```"
    await ctx.send(response)
  else:
    await ctx.send("Spell correctly xd. The materials list is \n{}".format(d_access.get_material_list()))


##### Work in Progress
'''
@bot.command()
async def resin(ctx):
  user = ctx.author.name

  elif message.content.startswith("!resin set "):
    user = message.author.name
    try:
      amount = int(message.content.split("!resin set ")[-1])
    except ValueError:
      await message.channel.send("Resin amount must be an integer.")
        
    resin.set_resin(user, amount)
    await message.channel.send("Resin set at {} for {}".format(amount, user))

  elif message.content.startswith("!resin get"):
    user = message.author.name
    amount = resin.get_resin(user)

    if amount is not None:
      await message.channel.send("{} has about {} resin".format(user, amount))
    else:
      await message.channel.send("{} is not in the database".format(user))
'''

keep_online()
bot.run(os.getenv('TOKEN'))
