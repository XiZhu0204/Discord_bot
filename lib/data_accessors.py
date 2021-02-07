import json
from datetime import datetime
import pytz

DATE = datetime.now()
working_tz = pytz.timezone("America/Yakutat")

with open("data.json") as f:
  DATA = json.load(f)

def get_weekday():
  return DATA["weekday"][DATE.now(working_tz).weekday()]

def get_farmable_mats(day):
  return DATA["mats_by_weekday"][day]

def find_farmable_day(mat):
  farmable_days = []

  for day in DATA["mats_by_weekday"]:
    if mat in DATA["mats_by_weekday"][day]:
      farmable_days.append(day)

  return farmable_days  