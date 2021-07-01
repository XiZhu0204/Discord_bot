from discord.ext import commands
import os
from replit import db
import json

# below are to export and load db with JSON when repl causes issues

'''
res = {}
for key in db.keys():
  res[key] = db[key]

with open("res.json", "w") as f:
  f.write(json.dumps(res, indent = 4))
'''

'''
with open("res.json", "r") as f:
  data = json.load(f)

for key in data:
  db[key] = data[key]
'''

from lib.keep_online import keep_online

bot = commands.Bot(command_prefix = "!")

for filename in os.listdir("./cogs"):
  if filename.endswith(".py"):
    bot.load_extension(f"cogs.{filename[:-3]}")

keep_online()
bot.run(os.getenv('TOKEN'))
