from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  # this is called every 5 min
  return "Bot still online"


def run():
  app.run(host='0.0.0.0',port=8080)


def keep_online():
  t = Thread(target=run)
  t.start()