from replit import db
from discord.ext import tasks

def set_resin(user, amount):
  db[user] = amount

def get_resin(user):
  if user not in db.keys():
    return None

  return db[user]

@tasks.loop(minutes = 8.0)
async def increment_resin():
  for user in db.keys():
    if db[user] < 160:
      db[user] += 1