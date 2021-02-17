import json
from datetime import datetime


with open("data.json") as f:
  DATA = json.load(f)

def get_weekday(tz):
  return DATA["weekday"][datetime.now(tz).weekday()]

def get_date(tz):
  pass

def hours_minutes_till_midnight(tz):
  now = datetime.now(tz)
  now_in_min = (now.hour*60) + now.minute
  time_till_reset = (24*60) - now_in_min
  hours = time_till_reset//60
  minutes = time_till_reset % 60

  return hours, minutes
