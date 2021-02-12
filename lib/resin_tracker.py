from replit import db
from discord.ext import tasks

import lib.pretty_prints as pprint

def set_resin(user, amount):
  if user not in db.keys():
    db[user] = {
      "resin": 0
    }
  
  user_data = db[user]
  user_data["resin"] = amount
  if "noti" in user_data:
    user_data["noti"]["notified"] = False
  db[user] = user_data

def get_resin(user):
  if user not in db.keys():
    return None

  return db[user]["resin"]

def set_noti_value(user, amount, user_id):
  user_data = db[user]
  user_data["noti"] = {"amount": amount, "id": user_id, "notified": False}
  db[user] = user_data

def noti_off(user):
  user_data = db[user]
  user_data.pop("noti", None)
  db[user] = user_data

@tasks.loop(minutes = 8.0)
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
          user = user_data["noti"]["id"]
          user_ping = f"<@!{user}>"
          message = f"{user_ping}, you have {res_amount} resin."
          await channel.send(pprint.block_quote_str(message))
    
    db[user] = user_data
