import discord
from datetime import datetime
import pytz
import os
import requests
import json

from lib.keep_online import keep_online

DATE = datetime.now()
working_tz = pytz.timezone("America/Yakutat")

DAYS_OF_WEEK = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
FARMABLE_MATS_BY_WEEKDAY = {
    "Monday": ("Freedom", "Prosperity", "Decarabian", "Guyun"),
    "Tuesday": ("Diligence", "Resistance", "Elixir", "Tooth"),
    "Wednesday": ("Ballad", "Gold", "Aerosiderite", "Gladiator"),
    "Thursday": ("Freedom", "Prosperity", "Decarabian", "Guyun"),
    "Friday": ("Diligence", "Resistance", "Elixir", "Tooth"),
    "Saturday": ("Ballad", "Gold", "Aerosiderite", "Gladiator")
}


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == client.user:
            return

        if "I am" in message.content:
            end_piece = message.content.split('I am')[-1]
            await message.channel.send(f'Hello{end_piece}! I am dad!')
        elif message.content.startswith("!materials"):
            weekday = DAYS_OF_WEEK[DATE.now(working_tz).weekday()]
            if weekday == "Sunday":
                await message.channel.send("It's Sunday you cringe kid.")
            else:
                list_of_mats = get_farmable_mats(weekday)
                response = "You can waste your time today farming:\n"
                for entry in list_of_mats:
                    response += entry + "\n"
                await message.channel.send(response)
        elif message.content.startswith("!when "):
            mat = message.content.split('!when ')[-1]
            mat = mat.capitalize()
            list_of_days = find_farmable_day(mat)
            if list_of_days:
                # non empty array, indicating that retrieval was successful
                response = f"Greetings you gacha cringe, {mat} can be farmed on:\n"
                for entry in list_of_days:
                    response += entry + "\n"
                response += "Sunday"
                await message.channel.send(response)
            else:
                await message.channel.send("Spell correctly xd")


def get_farmable_mats(day):
    return FARMABLE_MATS_BY_WEEKDAY[day]


def find_farmable_day(mat):
    farmable_days = []

    for day in FARMABLE_MATS_BY_WEEKDAY:
        if mat in FARMABLE_MATS_BY_WEEKDAY[day]:
            farmable_days.append(day)

    return farmable_days


client = MyClient()
keep_online()
client.run(os.getenv('TOKEN'))


