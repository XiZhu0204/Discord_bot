from replit import db
from discord.ext import tasks

def set_resin(user, amount):
  if user not in db.keys():
    db[user] = {
      "resin": 0
    }
  
  user_data = db[user]
  user_data["resin"] = amount
  db[user] = user_data

def get_resin(user):
  if user not in db.keys():
    return None

  return db[user]["resin"]

@tasks.loop(minutes = 8.0)
async def increment_resin():
  for user in db.keys():
    user_data = db[user]
    if user_data["resin"] < 160:
      user_data["resin"] += 1
      db[user] = user_data
  