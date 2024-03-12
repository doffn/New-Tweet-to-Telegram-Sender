# importing libraries and packages
from datetime import datetime
import telebot
import threading
import schedule
import logging
import psutil
import time
import os
import sys
from tweety import Twitter

import shutil
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

## importing local functions

from bot import *
from db import *

API = '''Telegram BOT Token'''
ID = '''Channal ID'''
URL = '''Mongodb url'''
bot = telebot.TeleBot(API)



def report(message, channel_id=ID):
    """
      Sends a message to the specified Telegram channel.
    
      Args:
          message (str): The message content to send.
          channel_id (str, optional): The Telegram channel ID to send the message to.
                                       Defaults to the ID stored in the `ID` variable.
      """
    try:
        bot.send_message(channel_id, message)
    except Exception as e:
        print(f"Failed to send message: {e}")


def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """
    try:
        p = psutil.Process(os.getpid())
        for handler in p.open_files() + p.connections():
            os.close(handler.fd)
    except Exception as e:
        logging.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)



session = ["session", "session1"]   # define multiple account session to avoid rate limitation


def get_values(values):
  index = 0
  while True:
      yield values[index]
      index = (index + 1) % len(values)


values_generator = get_values(session)



#####################################################################
def get_tweet_by_username(usernames, replies=False):
    """
    Retrieves tweets from the specified usernames.

    usernames: list of usernames
    replies: whether to include replies (default: False)

    Returns: a list of scraped tweets
    """
    session = next(values_generator)
    app = Twitter(session)
    app.connect()
    print(app.me)

    all_tweets = []
    try:

        for p, user in enumerate(usernames):
            try:
                tweets_list = []
                tweets = app.get_tweets(user[1:],  replies=True)
                for tweet in tweets:
                    if "all_tweets_id" in tweet.keys():
                        #print("got a reply")
                        tweet = tweet["tweets"][-1]
                    tweet_new = (
                      False,
                      tweet["id"],
                      tweet["text"],
                      tweet["date"],
                      f"https://vxtwitter.com/{user[1:]}/status/{tweet['id']}"
                    )
                    tweets_list.append(tweet_new)

                all_tweets.append(tweets_list)
                print(f"Tring to scrape from {user} and got {len(tweets_list)} tweets")
            except Exception as e:
                print(e)
                all_tweets.append([])
            time.sleep(1)



    except Exception as e:
        report(f" It can not scrape cause {e}")

    return all_tweets




print('/////////PROGRAM RUNNING////////')

def main_function():
  while True:
      #start_time_main = time.time

      current_time = datetime.now().time()
      print(current_time)
      start_time = datetime.strptime("07:00:00", "%H:%M:%S").time()
      end_time = datetime.strptime("23:00:00", "%H:%M:%S").time()
      if start_time <= current_time <= end_time:
          try:
              data = get_mongo()
              usernames = [i for i in data["usernames"] if data["usernames"][i]["Active"]]
              all_data = get_tweet_by_username(usernames, replies=data["replies"])


              try:
                  for u, data_new in enumerate(all_data):

                      user_name = usernames[u]
                      tweet_ids = []
                      for j in range(0, len(data["usernames"][user_name]["recent_tweets"])):
                          tweet_ids.append(data["usernames"][user_name]["recent_tweets"][j]["Tweet_Id"])

                      new_ids = [id[1] for id in data_new]
                      #print(len(new_ids))
                      diff_ids = list(set(new_ids) - set(tweet_ids))
                      #print(len(tweet_ids))
                      data_new = data_new[::-1]
                      #report(f"{user_name} ----- retrieve {len(data_new)} data and got {len(diff_ids)} data")
                      if len(diff_ids) > 0:
                          for j, new_tweet in enumerate(data_new):
                              Pin, Id, text, Date, url = new_tweet
                              if Id in diff_ids:
                                  #print(Date)
                                  Date = str(datetime.fromisoformat(str(Date)).strftime("%b %d, %Y · %I:%M %p UTC"))
                                  message = f"""\n.\n{user_name}\n{text}\n{url} at {Date}"""
                                  new_tweet = {
                                      "Pinned": Pin,
                                      "Tweet_Id": Id,
                                      "Text": text,
                                      "Tweet_date": Date,
                                      "Tweet_URL": url
                                  }
                                  if Pin is True:
                                      data["usernames"][user_name]["recent_tweets"].insert(0, new_tweet)
                                  else:
                                      data["usernames"][user_name]["recent_tweets"].insert(j, new_tweet)
                                  data["usernames"][user_name]["total_tweet"] += 1
                                  data["usernames"][user_name]["day_tweets"] += 1
                                  mongo_update(data)
                                  print("message sent")
                                  report(message)
              except Exception as e:
                  print(f"There is an error at the message sender of {user_name} ::  {e}")

          except Exception as e:
              print(f"There is an error in main function ::  {e}")
      else:
          print("You are sleeping")
      print("FINISHED")
      time.sleep(5*60)   # it will sleep for 5 minute



def reviewer():
    try:
        data = get_mongo()
        text = f"Hello User, this is the 24 HRS Report:\n"
        username = [i for i in data["usernames"] if data["usernames"][i]["Active"]]
        for user in username:
            #data["usernames"][user]["total_tweet"] = 0
            tweets = data["usernames"][user]["total_tweet"]
            previous_tweet = data["usernames"][user].get("day_tweets", 0)
            data["usernames"][user]["day_tweets"] = 0
            if  len(data['usernames'][user]['recent_tweets']) == 0:
                time = None
            else:
                if data['usernames'][user]['recent_tweets'][0]['Pinned'] == 'false':
                    time = data["usernames"][user]["recent_tweets"][0]["Tweet_date"]
                else:
                    time = data["usernames"][user]["recent_tweets"][1]["Tweet_date"]

            text += f"👨🏾‍🦲 : {user} \n  24 hr number of tweets 📜: { previous_tweet if previous_tweet > 0 else '⚪️'} \n  last tweet time ⌛️: {time}\n"

        mongo_update(data)

        report(text)
    except Exception as e:
        print(e)

def review():
    """ Schedule the function to run at 12 PM"""
    schedule.every().day.at("12:00",).do(reviewer)

    # Keep the schedule running continuously
    while True:
        schedule.run_pending()
        time.sleep(1)

def fixer():
    # Schedule the function to run at 12 PM
    schedule.every(10).minutes.do(fix_json)

    # Keep the schedule running continuously
    while True:
        schedule.run_pending()
        time.sleep(1)


#fix_json()
# Create the first thread object
thread1 = threading.Thread(target=main_function)

# Create the second thread object
thread2 = threading.Thread(target=commands)
thread3 = threading.Thread(target=review)

try:
    # Start the main function
    thread1.start()
except Exception as e:
    print(e)

try:
    # Start the TG bot
    thread2.start()
except Exception as e:
    print(e)

try:
    # Start Reporter function
    thread3.start()
except Exception as e:
    print(e)





