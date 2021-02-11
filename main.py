from discord.ext import commands
import os
import asyncio

import lib.data_accessors as d_access
import lib.resin_tracker as resin_track
import lib.pretty_prints as pprint
from lib.keep_online import keep_online


bot = commands.Bot(command_prefix = "!")

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
  amount = resin_track.get_resin(user)

  # event handling func
  async def send_msg_and_handle_events(msg):
    msg = await ctx.send(msg)
    await msg.add_reaction("⬆️")
    
    def check_for_set(reaction, author):
      return author == ctx.author and str(reaction.emoji) == "⬆️"

    try:
      reaction, author = await bot.wait_for("reaction_add", timeout = 60.0, check = check_for_set)
    except asyncio.TimeoutError:
      await msg.remove("⬆️")
    else:
      await ctx.send(pprint.block_quote_str("Enter resin amount"))

      def check_for_resin_amount(m):
        try:
          n = int(m.content)
        except ValueError:
          ctx.send(pprint.block_quote_str("Must be an integer"))
          return False
        else:
          if n < 0 or n > 160:
            ctx.send(pprint.block_quote_str("Must be valid amount Darien."))
          return m.author == ctx.author and m.channel == ctx.channel

      try:
        in_val = await bot.wait_for("message", timeout = 60.0, check = check_for_resin_amount)
      except asyncio.TimeoutError:
        await ctx.send("Soo slow, timed out. Try again")
      else:
        in_amount = int(in_val.content)
        resin_track.set_resin(user, in_amount)

      header = "Resin set at"
      footer = f"for {user}"
      resp = pprint.block_quote_str(in_amount, header = header, footer = footer)
      await ctx.send(resp)
    # end event handlng func
  
  if amount is not None:
    header = f"{user} has about"
    footer = "resin"
    footer += "\nReact with ⬆️ to set your resin amount."
    response = pprint.block_quote_str(str(amount), header = header, footer = footer)
    await send_msg_and_handle_events(response)
  else:
    main_str = f"{user} is not in the database"
    footer = "React with ⬆️ to add your resin amount."
    response = pprint.block_quote_str(main_str, footer = footer)
    await send_msg_and_handle_events(response)

''''
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