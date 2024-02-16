# importing libraries and packages
#import __init__
import time
import requests
from bs4 import BeautifulSoup
import threading
import json
from datetime import datetime
import logging
import psutil
import sys
import telebot
import schedule
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

API = os.environ['Token']
ID = os.environ['ID']
URL = os.environ['API_KEY']
bot = telebot.TeleBot(API)

def get_mongo():
    client = MongoClient(URL, server_api=ServerApi('1'))
    try:
        # Access the database and collection
        db = client['Tweet_tg']
        collection = db['my_first_data']
  
        # Retrieve a single document from the collection based on the query
        document = collection.find_one()
  
        try:
            with open("output.json", 'w') as json_file:
                # Use default JSON encoder
                json.dump(document, json_file, indent=2, default=str) 
            print(f"JSON data has been written to output.json")
            return document
        except Exception as e:
            print(f"Error writing JSON data: {e}")
  
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
        db = client['Tweet_tg']
        collection = db['my_first_data']
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
        bot.send_message(channel_id, message, parse_mode='Markdown')
    except Exception as e:
        print(f"Failed to send message: {e}")
        bot.send_message(channel_id, message)


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
        bot.reply_to(message, "Here are the available commands:\n"
                              "/add <@username> - add a user name to the list\n"
                              "/rem <@username> - remove a username from the list\n"
                              "/del <@username> - permanently delete a username from the list\n"
                              "/reset - add the removed usernames to the working list\n" 
                              "/ls - list all users in the list\n")

    @bot.channel_post_handler(commands=['add'])
    def handle_channel_add(message):
        if message.text.startswith('/add ') and message.text[5:].startswith('@'):
            if message.text[5:] in username:
                bot.reply_to(message, f'{message.text[5:]} User is already included...')
            elif message.text[5:] in data["usernames"]:
                bot.reply_to(message, f'{message.text[5:]} User is Activated...')
                data["usernames"][message.text[5:]]["Active"] = True
                mongo_update(data, remove=False, set_empty=False)
                restart_program()
            else:
                data["usernames"][message.text[5:]] = {
                    "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "recent_tweets": [],
                    "total_tweet" : 0,
                    "day_tweets" :0,
                    "Active" : True
                }
      
                bot.reply_to(message, f'{message.text[5:]} is added to your account list\n-------╔( •̀ з •́)╝╚(•̀ ▪ •́ )╗-------')

                mongo_update(data)
                restart_program()

    @bot.channel_post_handler(commands=['rem'])
    def handle_channel_rem(message):
        if message.text.startswith('/rem ') and message.text[5:].startswith('@'):
            if message.text[5:] not in username:
                bot.reply_to(message, f'{message.text[5:]} User is not included...')
            else:
                data["usernames"][message.text[5:]]["Active"] = False
                bot.reply_to(message, f'{message.text[5:]} is removed\n-------〵(•ʘ̥ᴗʘ̥ •〵)-------')
                mongo_update(data, remove=False, set_empty=False)
                restart_program()

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

                restart_program()


    @bot.channel_post_handler(commands=['ls'])
    def handle_channel_ls(message):
        if message.text.startswith('/ls'):
            bot.reply_to(message, f'{username} Total account is: {len(username)}\n╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮')

    @bot.channel_post_handler(commands=['replies'])
    def handle_channel_replies(message):
        replies = data["replies"]
        if bool(message.text[8:]) == True:
            data["replies"] = not replies
            bot.reply_to(message, f'THE REPLIES HAVE BEEN CHANGED : {data["replies"]}')
            mongo_update(data, remove=False, set_empty=False)
            restart_program()
        else:
            bot.reply_to(message, f'THE REPLIES IS FLAGGED : {replies}')


    bot.polling()



#####################################################################
def get_tweet_by_username(username, counter_max=10, replies=False):
    """Retrieves tweets from a specified Twitter username using the nitter search feature.

    Arguments:
        - username (str): The Twitter username of the user whose tweets are to be retrieved.
        - counter_max (int, optional): Define the maximum number of tweets to retrieve. Defaults to 10.
        - replies (bool, optional): A boolean value that indicates whether to retrieve all tweets (including replies) or only the tweets posted by the user. Defaults to False.
    """
    urls = ["nitter.rawbit.ninja", "nitter.mint.lgbt", "nitter.d420.de"]
    for url in urls:
        if replies:
            full_url = f"https://{url}/{username}/with_replies"
        else:
            full_url = f"https://{url}/{username}"
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            response = requests.get(full_url, headers=headers)
            time.sleep(3)
            if response.status_code == 200:
                tweets = response.content
                if tweets:
                    soup = BeautifulSoup(tweets, 'html.parser')
                    tweets = soup.find_all('div', class_='timeline-item')

                    counter = 0  # Counter to keep track of number of tweets processed
                    tweets_list = []

                    for tweet in tweets:
                        if counter < counter_max:
                            if 'retweeted' in str(tweet):
                                tweet_text = f"RT: {tweet.find('a', class_='username').text} \n{tweet.find('div', class_='tweet-content').text.strip()}"
                            else:
                                try:
                                    tweet_text = f"{tweet.find('div', class_='replying-to').text} \n{tweet.find('div', class_='tweet-content').text.strip()}"
                                except:
                                    tweet_text = tweet.find('div', class_='tweet-content').text.strip()

                            tweet_url = tweet.find('a', class_='tweet-link')['href']
                            tweet_id = tweet_url.split('/')[-1][:19]
                            tweet_date = tweet.find('span', class_='tweet-date').find('a')['title']
                            tweet_url = f"https://vxtwitter.com/{username}/status/{tweet_id}"
                            tweet_pinned = bool(tweet.find('div', class_='pinned'))

                            tweet_data = (tweet_date, tweet_id, tweet_text, tweet_pinned, tweet_url)

                            tweets_list.append(tweet_data)
                            counter += 1
                        else:
                            break

                    return tweets_list
            elif response.status_code == 404:
                return "404 error"
        except Exception as e:
            print(f"Error: {e}")

            return None






print('/////////PROGRAM RUNNING////////')



def main_function():
    try:
      data = get_mongo()
      if data is None:
          raise ValueError("The function returned None")
    except ValueError as ve:
      print(f"There is an error: {ve}")
      restart_program()
    except Exception as e:
      print(f"There is an error: {e}")
      restart_program()

    username = [i for i in data["usernames"] if data["usernames"][i]["Active"]]
    result2 = []
    item = 0
    while True:
      if len(username) == 0:
          continue
      result = []

      for j in range(0, len(username)):
        user_name = username[j][1:]
        tweet_list = []
        recent_tweets = data["usernames"][username[j]]["recent_tweets"]
        for tweet in recent_tweets:
            tweet_url = tweet["Tweet_URL"]
            tweet_list.append(tweet_url)

        try:
            for trial in range(0, 3):
                try:
                    try:
                        tweet_result = get_tweet_by_username(user_name, replies=data["replies"])
                        #print(len(tweet_result))
                    except Exception as e:
                        if tweet_result  == "404 error":
                            report(f'ATTENTION::{username[j]} is removed cause {e}') 
                            del data["usernames"][username[j]]
                            mongo_update(data, remove=False, set_empty=False)
                            restart_program()
                    if len(tweet_result) >= 6:
                        tweets_list = []
                        for _ in tweet_result:
                            Date, Id, text, Pin, url = _
                            new_tweet = {
                                "Pinned": Pin,
                                "Tweet_Id": Id,
                                "Text": text,
                                "Tweet_date": Date,
                                "Tweet_URL": url
                            }
                            tweets_list.append(new_tweet)

                        previous_res = data["usernames"][username[j]]["recent_tweets"]
                        for new_tweet in tweets_list:
                            if new_tweet not in previous_res:
                                if new_tweet["Pinned"] is True:
                                    previous_res.insert(0, new_tweet)
                                else:
                                    previous_res.insert(tweets_list.index(new_tweet), new_tweet)
                        data["usernames"][username[j]]["recent_tweets"] = previous_res
                        break
                except Exception as e:
                        print(f"{trial} trial, We cannot get any data because of the error: {e}")


            result.append(tweet_result)


            if item > 0 and result[j][4] not in  result2[j]:
                restart_program()
            else:
                if item == 0:
                    new_tweets = []
                    tweets_list = (data["usernames"][username[j]]["recent_tweets"])[:10]
                    for tweet in tweets_list:
                        new_tweet = tuple(tweet.values())
                        new_tweets.append(new_tweet)

                    print(f'{j + 1}  ------- this is the first trial of {username[j]}')

                    result2.append(new_tweets)

                previous_set = set(result2[j])
                new_set = set(result[j])
                changed_items = list(new_set - previous_set)[::-1]
                for po in changed_items:
                    Date, Id, text, Pin, url = po
                    message = f".  \n{username[j]} \n{text}\n {url} at {Date}"
                    if url not in tweet_list:
                        if "#" in text:
                            text_edit = text.replace("#", "~")
                            mess = f'.\n{username[j]} \n{text_edit} \n{url} at {Date}'
                            print(mess)

                            report(mess)
                        elif "&" in text:
                            mess = f"{result[j][po]['URL']}"
                            print(url)
                            report(url)
                        else:
                            report(message)
                            print(message)
                        data["usernames"][username[j]]["total_tweet"] += 1
                        data["usernames"][username[j]]["day_tweets"] += 1
                        mongo_update(data)

        except Exception as e:
            print(f"last error ::  {e}")
      #report (f'$$$$$$$$$$ {e} $$$$$$$$$$$ at account {username[j]} first')

      result2 = result


      mongo_update(data)

      time.sleep(10)
      print(item)
      item += 1


def users_data():
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

        mongo_update(data, remove=False, set_empty=False)

        report(text)
        restart_program()
    except Exception as e:
        print(e)


def review():
    # Schedule the function to run at 12 PM
    schedule.every().day.at("12:00",).do(users_data)



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
    # Start both threads
    thread1.start()
    thread2.start()
    thread3.start()
except Exception as e:
    print(e)
    restart_program()




