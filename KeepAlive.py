from flask import Flask
from threading import Thread
import random
n = random.randint(1,9)
app = Flask('app')
@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0',port='5050')

def keep_alive():
    t = Thread(target=run)
    t.start()