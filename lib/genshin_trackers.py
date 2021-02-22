import asyncio
import time

from replit import db
from discord.ext import tasks

import lib.common.pretty_prints as pprint
import lib.common.time_functions as time_func

SPAM_PREVENTION = {}
WEEK_IN_SECONDS = 604800

def set_resin(user, amount, user_id):
  if user not in db.keys():
    db[user] = {
      "resin": 0,
      "id": user_id
    }
  
  user_data = db[user]
  user_data["resin"] = amount
  user_data["id"] = user_id
  if "noti" in user_data:
    user_data["noti"]["notified"] = False
  db[user] = user_data


def get_resin(user):
  if user not in db.keys():
    return None

  return db[user]["resin"]


def get_time_to_noti(user):
  user_data = db[user]

  if "noti" not in user_data or user_data["noti"]["notified"]:
    return (None, None, None)
  else:
    # user opted for notifications and a notification has not been sent
    # this implies that current resin < notification value
    noti_amount = user_data["noti"]["amount"]
    current_resin = user_data["resin"]

    min_till_noti = (noti_amount - current_resin)*8
    hours = min_till_noti//60
    minutes = min_till_noti % 60
    return hours, minutes, noti_amount


def generate_time_to_noti_msg(user):
  noti_hours, noti_minutes, noti_amount = get_time_to_noti(user)
  if noti_hours is not None:
    noti_str = f"{user} will reach {noti_amount} resin in {str(noti_hours).zfill(2)}:{str(noti_minutes).zfill(2)} and be notified."
    return noti_str
  else:
    return None


def set_noti_value(user, amount):
  user_data = db[user]
  user_data["noti"] = {"amount": amount, "notified": False}
  db[user] = user_data


def noti_off(user):
  user_data = db[user]
  user_data.pop("noti", None)
  db[user] = user_data


def set_transformer_used(user, user_id):
  if user not in db.keys():
    db[user] = {
      "transformer_used": None,
      "id": user_id
    }
  
  current_time = time_func.get_current_time_for_db()
  user_data = db[user]
  user_data["transformer_used"] = current_time
  user_data["id"] = user_id
  db[user] = user_data
  

@tasks.loop(minutes = 8.0)
async def db_update(bot):
  await increment_resin(bot)
  await check_transformers(bot)


async def check_transformers(bot):
  current_time = time_func.get_current_time()
  for user in db.keys():
    user_data = db[user]

    if "transformer_used" in user_data:
      time_used = time_func.convert_db_time_storage_to_datetime(user_data["transformer_used"])

      seconds_passed = time_func.get_difference_in_seconds(current_time, time_used)
      if seconds_passed > WEEK_IN_SECONDS:
        channel = bot.get_channel(805552076763562005)
        user_id = user_data["id"]
        user_ping = f"<@!{user_id}>"
        message = f"{user_ping}, your transformer has come off CD."

        response = pprint.block_quote_str(message)
        await channel.send(response)
        user_data.pop("transformer_used", None)
        db[user] = user_data


async def increment_resin(bot):
  for user in db.keys():
    user_data = db[user]

    if user_data["resin"] < 160:
      user_data["resin"] += 1
    
    if "noti" in user_data:
      noti_amount = user_data["noti"]["amount"]
      res_amount = user_data["resin"]
      if res_amount >= noti_amount:
        if not user_data["noti"]["notified"]:
          user_data["noti"]["notified"] = True
          db[user] = user_data
          channel = bot.get_channel(805552076763562005)
          user_id = user_data["id"]
          user_ping = f"<@!{user_id}>"
          message = f"{user_ping}, you have {res_amount} resin."

          response = pprint.block_quote_str(message)
          await channel.send(response)
    
    db[user] = user_data


async def resin_cmd(ctx, bot):
  user = ctx.author.name

  if user in SPAM_PREVENTION:
    if time.time() - SPAM_PREVENTION[user] < 30.0:
      response = pprint.embed_str("You already have an active process, use that instead.")
      await ctx.send(embed = response)
      return
  else:
    SPAM_PREVENTION[user] = time.time()

  def check_for_resin_amount(m):
      if m.author == ctx.author and m.channel == ctx.channel:
        try:
          n = int(m.content)
        except ValueError:
          raise Exception(pprint.embed_str("Must be an integer"))
        else:
          if n < 0 or n > 160:
            raise Exception(pprint.embed_str("Must be valid resin amount"))
          return True
  
  async def remove_reactions(msg):
    await msg.remove_reaction("⬆️", bot.user)
    await msg.remove_reaction("<:peepoping:809565752768069632>", bot.user)
    await msg.remove_reaction("<:PepeREE:368523735843733516>", bot.user)

  async def handle_set(msg):
    await msg.add_reaction("⬆️")
    
    def check_for_set(reaction, author):
      return author.name == user and str(reaction.emoji) == "⬆️"

    try:
      reaction, author = await bot.wait_for("reaction_add", timeout = 30.0, check = check_for_set)
    except asyncio.TimeoutError:
      await remove_reactions(msg)
    else:
      response = pprint.embed_str("Enter resin amount")
      await ctx.send(embed = response)

      try:
        in_val = await bot.wait_for("message", timeout = 30.0, check = check_for_resin_amount)
      except asyncio.TimeoutError:
        response = pprint.embed_str("Too slow, timed out. Try again")
        await ctx.send(embed = response)
      except Exception as e:
        await ctx.send(embed = e.args[0])
      else:
        in_amount = int(in_val.content)
        set_resin(user, in_amount, ctx.author.id)

        header = "Resin set at"
        footer = f"for {user}"
        noti_str = generate_time_to_noti_msg(user)
        if noti_str:
          footer += f"\n{noti_str}"
        response = pprint.embed_str(in_amount, header = header, footer = footer)
        await ctx.send(embed = response)
      finally:
        # stop user from calling set again since wait_for is no longer active
        await msg.remove_reaction("⬆️", bot.user)


  async def handle_notif(msg):
    await msg.add_reaction("<:peepoping:809565752768069632>")
    
    def check_for_noti(reaction, author):
      return author.name == user and str(reaction.emoji) == "<:peepoping:809565752768069632>"

    try:
      reaction, author = await bot.wait_for("reaction_add", timeout = 30.0, check = check_for_noti)
    except asyncio.TimeoutError:
      await remove_reactions(msg)
    else:
      response = pprint.embed_str("Enter amount to notify. Default is 150 after 10s timeout.")
      await ctx.send(embed = response)

      try:
        in_val = await bot.wait_for("message", timeout = 30.0, check = check_for_resin_amount)
      except asyncio.TimeoutError:
        set_noti_value(user, 150)
        response = pprint.embed_str(f"{user} will be notified at 150 resin")
        await ctx.send(embed = response)
      except Exception as e:
        await ctx.send(embed = e.args[0])
      else:
        in_amount = int(in_val.content)
        set_noti_value(user, in_amount)
        response = pprint.embed_str(f"{user} will be notified at {in_amount} resin")
        await ctx.send(embed = response)
      finally:
        # stop user from calling noti again since wait_for is no longer active
        await msg.remove_reaction("<:peepoping:809565752768069632>", bot.user)

  async def notif_off(msg):
    await msg.add_reaction("<:PepeREE:368523735843733516>")

    def check_for_off(reaction, author):
      return author.name == user and str(reaction.emoji) == "<:PepeREE:368523735843733516>"

    try:
      reaction, author = await bot.wait_for("reaction_add", timeout = 30.0, check = check_for_off)
    except asyncio.TimeoutError:
      await remove_reactions(msg)
    else:
      noti_off(user)
      response = pprint.embed_str(f"Notifications off for {user}")
      await ctx.send(embed = response)
    finally:
      # stop user from calling noti off again since wait_for is no longer active
      await msg.remove_reaction("<:PepeREE:368523735843733516>", bot.user)
  
  amount = get_resin(user)

  if amount is not None:
    msg_list = [
      amount,
      "resin"
    ]
    noti_str = generate_time_to_noti_msg(user)
    if noti_str:
      msg_list.append(noti_str)
    
    header = f"{user} has about"
    footer = "\nReact with ⬆️ to set your resin amount.\nReact with <:peepoping:809565752768069632> if you want to be notified when resin reaches a certain amount.\nReact with <:PepeREE:368523735843733516> to turn off notifications."
    response = pprint.embed_list(msg_list, header = header, footer = footer)
    message = await ctx.send(embed = response)
    await asyncio.gather(
      handle_set(message),
      handle_notif(message),
      notif_off(message)
    )
  else:
    main_str = f"{user} is not in the database"
    footer = "React with ⬆️ to add your resin amount."
    response = pprint.embed_str(main_str, footer = footer)
    message = await ctx.send(embed = response)
    await handle_set(message)
    SPAM_PREVENTION.pop(user)


async def transformer_cmd(ctx):
  user = ctx.author.name
  user_id = ctx.author.id

  set_transformer_used(user, user_id)
  response = pprint.embed_str(f"{user} will be notified in 7 days when the transformer is off CD.")
  await ctx.send(embed = response)