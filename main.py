from discord.ext import commands, tasks
import os
import asyncio
import time

import lib.data_accessors as d_access
import lib.resin_tracker as resin_track
import lib.pretty_prints as pprint
from lib.keep_online import keep_online

bot = commands.Bot(command_prefix = "!")

SPAM_PREVENTION = set()
@tasks.loop(seconds = 60.0, count = 1)
async def add_user_to_process(user):
  SPAM_PREVENTION.add(user)

@add_user_to_process.after_loop
async def remove_user(user):
  SPAM_PREVENTION.remove(user)

@bot.event
async def on_ready():
  resin_track.increment_resin.start()
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
async def materials(ctx):
  weekday = d_access.get_weekday()
  if weekday == "Sunday":
    response = pprint.code_block_str("It's Sunday you cringe kid.")
    await ctx.send(response)
  else:
    list_of_mats = d_access.get_farmable_mats(weekday)
    header = "You can waste your time today farming:"
    response = pprint.code_block_list(list_of_mats, header = header)
    await ctx.send(response)


@bot.command()
async def when(ctx, arg):
  mat = arg.capitalize()
  list_of_days = d_access.find_farmable_day(mat)
  if list_of_days:
    # non empty array, indicating that retrieval was successful
    header = f"Greetings you gacha cringe, {mat} can be farmed on:"
    response = pprint.code_block_list(list_of_days, header = header, footer = "Sunday")
    await ctx.send(response)
  else:
    material_list = d_access.get_material_list()
    header = "Spell correctly xd. The materials list is:"
    response = pprint.code_block_list(material_list, header = header)
    await ctx.send(response)


##### Work in Progress
@bot.command()
async def resin(ctx):
  user = ctx.author.name
  if user in SPAM_PREVENTION:
    await ctx.send("You have an active process, use that one instead.")
    return
  add_user_to_process.start(user)
  amount = resin_track.get_resin(user)

  def check_for_resin_amount(m):
        try:
          n = int(m.content)
        except ValueError:
          raise Exception(pprint.block_quote_str("Must be an integer"))
          return False
        else:
          if n < 0 or n > 160:
            raise Exception(pprint.block_quote_str("Must be valid resin amount"))
            return False
          return m.author == ctx.author and m.channel == ctx.channel

  async def handle_set(msg):
    await msg.add_reaction("⬆️")
    
    def check_for_set(reaction, author):
      return author == ctx.author and str(reaction.emoji) == "⬆️"

    try:
      reaction, author = await bot.wait_for("reaction_add", timeout = 60.0, check = check_for_set)
    except asyncio.TimeoutError:
      await msg.remove_reaction("⬆️", bot.user)
      await msg.remove_reaction("<:peepoping:809565752768069632>", bot.user)
    else:
      await ctx.send(pprint.block_quote_str("Enter resin amount"))

      try:
        in_val = await bot.wait_for("message", timeout = 60.0, check = check_for_resin_amount)
      except asyncio.TimeoutError:
        await ctx.send("Too slow, timed out. Try again")
      except Exception as e:
        await ctx.send(e.args[0])
      else:
        in_amount = int(in_val.content)
        resin_track.set_resin(user, in_amount)

        header = "Resin set at"
        footer = f"for {user}"
        resp = pprint.block_quote_str(in_amount, header = header, footer = footer)
        await ctx.send(resp)
      finally:
        # stop user from calling set again since wait_for is no longer active
        await msg.remove_reaction("⬆️", bot.user)


  async def handle_notif(msg):
    await msg.add_reaction("<:peepoping:809565752768069632>")
    
    def check_for_noti(reaction, author):
      return author == ctx.author and str(reaction.emoji) == "<:peepoping:809565752768069632>"

    try:
      reaction, author = await bot.wait_for("reaction_add", timeout = 60.0, check = check_for_noti)
    except asyncio.TimeoutError:
      await msg.remove_reaction("⬆️", bot.user)
      await msg.remove_reaction("<:peepoping:809565752768069632>", bot.user)
    else:
      await ctx.send(pprint.block_quote_str("Enter amount to notify. Default is 150 after 10s timeout."))

      try:
        in_val = await bot.wait_for("message", timeout = 10.0, check = check_for_resin_amount)
      except asyncio.TimeoutError:
        resin_track.set_noti_value(user, 150)
        await ctx.send(pprint.block_quote_str(f"{user} will be notified at 150 resin"))
      except Exception as e:
        await ctx.send(e.args[0])
      else:
        in_amount = int(in_val.content)
        resin_track.set_noti_value(user, in_amount)
        await ctx.send(pprint.block_quote_str(f"{user} will be notified at {in_amount} resin"))
      finally:
        # stop user from calling noti again since wait_for is no longer active
        await msg.remove_reaction("<:peepoping:809565752768069632>", bot.user)

      
  
  if amount is not None:
    header = f"{user} has about"
    footer = "resin"
    footer += "\nReact with ⬆️ to set your resin amount."
    footer += "\nReact with <:peepoping:809565752768069632> if you want to be notified at a certain amount."
    response = pprint.block_quote_str(str(amount), header = header, footer = footer)
    message = await ctx.send(response)
    await asyncio.gather(
      handle_set(message),
      handle_notif(message)
    )
  else:
    main_str = f"{user} is not in the database"
    footer = "React with ⬆️ to add your resin amount."
    response = pprint.block_quote_str(main_str, footer = footer)
    message = await ctx.send(response)
    await handle_set(message)

keep_online()
bot.run(os.getenv('TOKEN'))