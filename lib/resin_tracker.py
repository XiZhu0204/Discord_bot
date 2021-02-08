from replit import db
from discord.ext import tasks

def set_resin(user, amount):
  db[user]["resin"] = amount
  print(db[user])

def get_resin(user):
  if user not in db.keys():
    return None

  return db[user]["resin"]

@tasks.loop(seconds = 8.0)
async def increment_resin():
  for user in db.keys():
    db[user]["resin"] += 1