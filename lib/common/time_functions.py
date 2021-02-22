import json
from datetime import datetime
import pytz

working_tz = pytz.timezone("UTC")

with open("data.json") as f:
  DATA = json.load(f)

def get_weekday(tz = working_tz):
  return DATA["weekday"][datetime.now(tz).weekday()]

def get_current_time(tz = working_tz):
  return datetime.now(tz)

def get_current_time_for_db(tz = working_tz):
  now = datetime.now(tz)
  storage = {
    "year": now.year,
    "month": now.month,
    "day": now.day,
    "hour": now.hour,
    "minute": now.minute,
    "second": now.second
  }
  return storage

def convert_db_time_storage_to_datetime(time_stored, tz = working_tz):
  resp = datetime(time_stored["year"], time_stored["month"], time_stored["day"], 
                  time_stored["hour"], time_stored["minute"], time_stored["second"],tzinfo=tz)
  return resp

def get_difference_in_seconds(time_1, time_2):
  diff = time_1 - time_2
  return diff.total_seconds()

def hours_minutes_till_midnight(tz = working_tz):
  now = datetime.now(tz)
  now_in_min = (now.hour*60) + now.minute
  time_till_reset = (24*60) - now_in_min
  hours = time_till_reset//60
  minutes = time_till_reset % 60

  return hours, minutes
