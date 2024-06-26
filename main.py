# importing libraries and packages
from bs4 import BeautifulSoup
from datetime import datetime
import telebot
import time
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import twitter
import requests
import os
from twitter.scraper import Scraper
import shutil
import json



API = os.environ['API']
ID = "" # channel ID
bot = telebot.TeleBot(API)
URL = os.environ['URL']



cookies = [{"ct0": os.environ["CT0"], "auth_token": os.environ["AUTH0"]},
 {"ct0": os.environ["CT1"], "auth_token": os.environ["AUTH1"]},]

def get_values(values):
  index = 0
  while True:
      yield values[index]
      index = (index + 1) % len(values)


values_generator = get_values(cookies)

def get_mongo():
    client = MongoClient(URL, server_api=ServerApi('1'))
    try:
        # Access the database and collection
        db = client['name']
        collection = db['collection']

        # Retrieve a single document from the collection based on the query
        document = collection.find_one()
        return document

    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

    finally:
        # Close the connection in a finally block to ensure it is always closed
        client.close()



def mongo_update(files, remove=False, set_empty=False):
    """
    files: dict, Json ; defines the json or dictionary to be updated
    remove: str ; defines the keys to be removed. If you want to remove a key inside a key, separate the keys with a dot.
    set_empty: bool ; will remove all data in the collection
    """
    try:
        client = MongoClient(URL, server_api=ServerApi('1'))
        db = client['name']
        collection = db['collection']
        document = collection.find_one()

        # Exclude '_id' field from the update query
        files_without_id = files.copy()
        files_without_id.pop('_id', None)

        if remove:
            keys = remove.split('.')
            nested_dict = data
            for key in keys[:-1]:
                nested_dict = nested_dict[key]
            del nested_dict[keys[-1]]
        if set_empty:
            for key in files_without_id:
                collection.update_one({"_id": document["_id"]}, {"$unset": {key: ""}})
        else:
            update_query = {"$set": files_without_id}
            collection.update_one({"_id": document["_id"]}, update_query)

        # Return the modified files dictionary
        return files_without_id
    except Exception as e:
        print(f"Error updating document: {e}")
    finally:
        client.close()


def report(message, channel_id=ID):

    try:
      bot.send_message(chat_id=channel_id, text=message, parse_mode='MarkdownV2')
    except Exception as e:
        print(f"Failed to send message: {e}")




def commands():    
    try:
      data = get_mongo()
      username = [i for i in data["usernames"] if data["usernames"][i]["Active"]]

    except Exception as e:
      print(f"Error reading JSON file: {e}")
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.reply_to(message, "Hello! I'm your Telebtot. How can I assist you?")

    @bot.message_handler(commands=['help'])
    def handle_help(message):
        bot.reply_to(message, "Here are the available commands:\n"
                              "/start - Start the bot\n"
                              "/help - Get help")

    @bot.message_handler(func=lambda message: True)
    def handle_all_other_messages(message):
        bot.reply_to(message, "I'm sorry, I don't understand that command. "
                              "Type /help to see the available commands.")

    @bot.channel_post_handler(commands=['start'])
    def handle_channel_start(message):
        bot.reply_to(message, "Hello! I'm Doff bot . I will send new tweet from a useraccount to a telegram.")

    @bot.channel_post_handler(commands=['help'])
    def handle_channel_help(message):
        bot.reply_to(message, f"""    Here are the available commands:
/add <@username> - add a username to the list
/rem <@username> - remove a username from the list
/del <@username> - permanently delete a username from the list
/reset - add the removed usernames back to the working list
/ls - list all users in the list
/replies {data['replies']} - include Replies?""")


    @bot.channel_post_handler(commands=['add'])
    def handle_channel_add(message):
        if message.text.startswith('/add ') and message.text[5:].startswith('@'):
            if message.text[5:] in username:
                bot.reply_to(message, f'{message.text[5:]} User is already included...')
            elif message.text[5:] in data["usernames"]:
                bot.reply_to(message, f'{message.text[5:]} User is Activated...')
                data["usernames"][message.text[5:]]["Active"] = True
                mongo_update(data, remove=False, set_empty=False)

            else:
                try:
                    user_name = message.text[6:]
                    print(user_name)
                    scraper = Scraper(cookies=cookies[0])
                    user = scraper.users([user_name])
                    #print(user)
                    user_id = user[0]["data"]["user"]["result"]["rest_id"]
                    #report(user_id)
                    data["usernames"][message.text[5:]] = {
                        "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "recent_tweets": [],
                        "total_tweet" : 0,
                        "day_tweets" :0,
                        "Active" : True,
                        "User_ID" : user_id
                    }
    
                    bot.reply_to(message, f'{message.text[5:]} is added to your account list\n-------╔( •̀ з •́)╝╚(•̀ ▪ •́ )╗-------')
    
                    #mongo_update(data)
                except Exception as e:
                    bot.reply_to(message, f'{message.text[5:]} is not added please try again')
                    print(e)

    @bot.channel_post_handler(commands=['rem'])
    def handle_channel_rem(message):
        if message.text.startswith('/rem ') and message.text[5:].startswith('@'):
            if message.text[5:] not in username:
                bot.reply_to(message, f'{message.text[5:]} User is not included...')
            else:
                data["usernames"][message.text[5:]]["Active"] = False
                bot.reply_to(message, f'{message.text[5:]} is removed\n-------〵(•ʘ̥ᴗʘ̥ •〵)-------')
                mongo_update(data, remove=False, set_empty=False)


    @bot.channel_post_handler(commands=['del'])
    def handle_channel_rem(message):
        data = get_mongo()
        if message.text.startswith('/del ') and message.text[5:].startswith('@'):
            if message.text[5:] not in username:
                bot.reply_to(message, f'{message.text[5:]} User is not included...')
            else:
                del data["usernames"][message.text[5:]]
                bot.reply_to(message, f'{message.text[5:]} is Deleteded\n-------〵(•ʘ̥ᴗʘ̥ •〵)-------')
                mongo_update(data)

                #restart_program()


    @bot.channel_post_handler(commands=['ls'])
    def handle_channel_ls(message):
        if message.text.startswith('/ls'):
            bot.reply_to(message, f'{username} Total account is: {len(username)}\n╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮')

    @bot.channel_post_handler(commands=['replies'])
    def handle_channel_replies(message):
        replies = data["replies"]
        data["replies"] = not replies
        bot.reply_to(message, f'THE REPLIES HAVE BEEN CHANGED : {data["replies"]}')
        mongo_update(data, remove=False, set_empty=False)


    bot.polling()




#####################################################################
def get_tweet_by_userid(usernames_id, usernames, replies=True):
    """
    Retrieves tweets from the specified usernames.

    usernames_id: list of usernames
    replies: whether to include replies (default: True)

    Returns: a list of scraped tweets
    """
    all_tweets = []
    try:
        cookies = next(values_generator)
        scraper = Scraper(cookies=cookies)
        if replies is True:
            scraped_tweets = scraper.tweets_and_replies(usernames_id, limit=10, pbar=True)
        else:
            scraped_tweets = scraper.tweets(usernames_id, limit=10)
        if len(scraped_tweets) < len(usernames_id):
            return([[]]*len(scraped_tweets))
        piner = 0
        for p, tweets_new in enumerate(scraped_tweets):
            tweets_list = []
            try:
                pin_check = tweets_new["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]
                if "Pin" in pin_check[1]["type"] and piner == 0:
                    tweet_new = pin_check[1]["entry"]["content"]["itemContent"]["tweet_results"]["result"]["legacy"]

                    tweet_new = (
                        True,
                        tweet_new["id_str"],
                        tweet_new["full_text"],
                        tweet_new["created_at"],
                        f"https://vxtwitter.com/{usernames[p]}/status/{tweet_new['id_str']}"
                    )
                    tweets_list.append(tweet_new)
                    piner = 1

                tweets = tweets_new["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"][-1]["entries"]

                for j, tweet in enumerate(tweets):
                    try:
                        if "promoted" in tweet["entryId"]:
                            continue
                        if "conversation" in tweet["entryId"]:
                            tweet_new = tweet["content"]["items"][-1]["item"]["itemContent"]["tweet_results"]["result"]["legacy"]
                        elif "tweet" in tweet["entryId"]:
                            #return tweet["content"]
                            tweet_new = tweet["content"]["itemContent"]["tweet_results"]["result"]["legacy"]
                        else:
                            continue

                        tweet_new = (
                            False,
                            tweet_new["id_str"],
                            tweet_new["full_text"],
                            tweet_new["created_at"],
                            f"https://vxtwitter.com/{usernames[p][1:]}/status/{tweet_new['id_str']}"
                        )
                        tweets_list.append(tweet_new)
                    except:
                        pass
            except Exception as e:
                print(f"There is an error : {e}")
            all_tweets.append(tweets_list)

    except Exception as e:
        print("There is an error on the main loop ===============================")
    print(all_tweets)
    return all_tweets







print('/////////PROGRAM RUNNING////////')

def main_function():
  #start_time_main = time.time()
  try:
      iter = 0
      data = get_mongo()
      usernames = [i for i in data["usernames"] if data["usernames"][i]["Active"]]
      USER_ID = []
      for username in usernames:
          if data["usernames"][username]["Active"]:
            USER_ID.append(data["usernames"][username]["User_ID"])


      all_data = get_tweet_by_userid(USER_ID, usernames)

      #print(all_data)
      
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
                          Date = datetime.strptime(Date, "%a %b %d %H:%M:%S %z %Y").strftime("%b %d, %Y · %I:%M %p UTC")
                          message = f"""[{user_name}]({url})\n{text}\n\n{Date}"""
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
                          print(iter)
                          print(message)
                          iter += 1
                          #report(message)
      except Exception as e:
          print(f"There is an error at the message sender of {user_name} ::  {e}")

  except Exception as e:
      print(f"There is an error in main function ::  {e}")

  print("Function Finished!!!!!")


