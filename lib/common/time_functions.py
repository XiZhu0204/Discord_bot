import json
from datetime import datetime
import pytz

with open("data.json") as f:
  DATA = json.load(f)

working_tz = pytz.timezone("America/Yakutat")

def get_weekday(tz = working_tz):
  return DATA["weekday"][datetime.now(tz).weekday()]

def hours_minutes_till_midnight(tz = working_tz):
  now = datetime.now(working_tz)
  now_in_min = (now.hour*60) + now.minute
  time_till_reset = (24*60) - now_in_min
  hours = time_till_reset//60
  minutes = time_till_reset % 60

  return hours, minutes
