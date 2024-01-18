# importing libraries and packages
import __init__
import time
import requests
from KeepAlive import keep_alive
from bs4 import BeautifulSoup
import threading
import json
from datetime import datetime
import logging
import psutil
import sys
import telebot
import time
import os



API = os.getenv("Token")
ID = os.getenv("ID")
bot = telebot.TeleBot(API)



def report(message, channel_id=ID):
    
    try:
        bot.send_message(channel_id, message)
    except Exception as e:
        print(f"Failed to send message: {e}")
        time.sleep(1)


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
            else:
                data["usernames"][message.text[5:]] = {
                    "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "recent_tweets": {},
                    "total_tweet" : 0
                }
                bot.reply_to(message, f'{message.text[5:]} is added to your account list\n-------╔( •̀ з •́)╝╚(•̀ ▪ •́ )╗-------')
                
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
                restart_program()
    
    @bot.channel_post_handler(commands=['rem'])
    def handle_channel_rem(message):
        if message.text.startswith('/rem ') and message.text[5:].startswith('@'):
            if message.text[5:] not in username:
                bot.reply_to(message, f'{message.text[5:]} User is not included...')
            else:
                data["removed_usernames"][message.text[5:]] = {
                    "removed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                del data["usernames"][message.text[5:]]
                bot.reply_to(message, f'{message.text[5:]} is removed\n-------〵(•ʘ̥ᴗʘ̥ •〵)-------')
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
                restart_program()
              
    @bot.channel_post_handler(commands=['del'])
    def handle_channel_rem(message):
        if message.text.startswith('/del ') and message.text[5:].startswith('@'):
            if message.text[5:] not in username:
                bot.reply_to(message, f'{message.text[5:]} User is not included...')
            else:
                del data["usernames"][message.text[5:]]
                bot.reply_to(message, f'{message.text[5:]} is permanently deleted\n-------〵(•ʘ̥ᴗʘ̥ •〵)-------')
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
                restart_program()

    @bot.channel_post_handler(commands=['reset'])
    def handle_channel_rem(message):
        if message.text.startswith('/reset'):
                if len(username_rem) == 0:
                    bot.reply_to(message, "Nothing to Reset...")
                for user in username_rem:
                    if user not in username:
                        data["usernames"][user] = {
                          "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          "recent_tweets": {},
                          "total_tweet" : 0
                      }
                        del data["removed_usernames"][user]
                        bot.reply_to(message, f'{user} is returned back to ur list\n-------〵(•ʘ̥ᴗʘ̥ •〵)-------')  
                        with open('data.json', 'w') as file:
                            json.dump(data, file, indent=4)
                        restart_program()
    
    @bot.channel_post_handler(commands=['ls'])
    def handle_channel_ls(message):
        if message.text.startswith('/ls'):
            bot.reply_to(message, f'{username} Total account is: {len(username)}\n╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮')
    bot.polling()



#####################################################################
def get_tweet_by_username(username, counter_max=10, replies=False):
    """Retrieves tweets from a specified Twitter username using the nitter search feature.
  
    Arguments:
        - username (str): The Twitter username of the user whose tweets are to be retrieved.
        - counter_max (int, optional): Define the maximum number of tweets to retrieve. Defaults to 10.
        - replies (bool, optional): A boolean value that indicates whether to retrieve all tweets (including replies) or only the tweets posted by the user. Defaults to False.
    """
    urls = ["nitter.salastil.com", "nitter.projectsegfau.lt",]
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

try:
    with open('data.json', 'r+') as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            print("There is a JSON error")
            restart_program()
        
        # Check if keys are present and create them if not
        if 'usernames' not in data:
            data['usernames'] = {}
        if 'removed_usernames' not in data:
            data['removed_usernames'] = {}
        if 'sent_ids' not in data:
            data['sent_ids'] = []
        
        # Move the file pointer to the beginning of the file
        file.seek(0)
        
        # Write the updated data back to the file
        json.dump(data, file, indent=4)
        
        # Truncate any remaining content after the updated data
        file.truncate()
        
except FileNotFoundError:
    print("File not found")


username= username = list(data["usernames"])
username_rem = list(data["removed_usernames"])


def main_function():
    result2 = []
    item = 0
    while True:

      result = []
      ids_list = list(data["sent_ids"])
      for j in range(0, len(username)):
        user_name = username[j][1:]
        try:
            for trial in range(0, 3):
                try:
                    try:
                        tweet_result = get_tweet_by_username(user_name)
                        #print(len(tweet_result))
                    except Exception as e:
                        if tweet_result  == "404 error":
                            report(f'ATTENTION::{username[j]} is REMOVED because {e}')      
                            if username[j] not in username_rem:
                                username_rem[username[j]] = {"removed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                            del username[username[j]]
                            with open('data.json', 'w') as file:
                                json.dump(data, file, indent=4)
                            restart_program()
                    if len(tweet_result) >= 6:
                        tweets_list = []
                        for _ in tweet_result:
                            Date, Id, text, Pin, url = _
                            new_tweet = {
                                "Pinned": Pin,
                                "Tweet_Id": Id,
                                "Text": f"{text[:25]} ... ",
                                "Tweet_URL": url
                            }
                            tweets_list.append(new_tweet)
                            data["usernames"][username[j]]["recent_tweets"] = tweets_list
                        break
                except Exception as e:
                        print(f"{trial} trial, We cannot get any data because of the error: {e}")

              
            result.append(tweet_result)
            if item == 0:
                print(f'{j + 1}  ------- this is the first trial of {username[j]}')
                for u in result[j]:
                  if u[1] not in ids_list:
                      ids_list.insert(0, u[1])
                continue
  
            if result[j][4] not in  result2[j]:
                restart_program()
            else:
                
                previous_set = set(result2[j])
                new_set = set(result[j][:4])
                changed_items = list(new_set - previous_set)
                for po in changed_items:
                    Date, Id, text, Pin, url = po
                    message = f".  \n{username[j]} \n{text}\n {url} at {Date}"
                    if Id not in ids_list:
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
                        ids_list.insert(0, Id)
                        data["usernames"][username[j]]["total_tweet"] += 1

        except Exception as e:
            print(e)
      #report (f'$$$$$$$$$$ {e} $$$$$$$$$$$ at account {username[j]} first')
      
      result2 = result
      
      
      data["sent_ids"] = ids_list
      with open('data.json', 'w') as file:
          json.dump(data, file, indent=4)
        
      time.sleep(20)
      print(item)
      item += 1



keep_alive()  


# Create the first thread object
thread1 = threading.Thread(target=main_function)

# Create the second thread object
thread2 = threading.Thread(target=commands)



try:
    # Start both threads
    thread1.start()
    thread2.start()
except Exception as e:
    print(e)
    restart_program()
    



