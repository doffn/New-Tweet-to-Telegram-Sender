# importing libraries and packages
import __init__
import time
import requests
from KeepAlive import keep_alive
from collections import Counter
from bs4 import BeautifulSoup
import os
import sys
import psutil
import telebot
import logging
import threading



API = os.getenv("Token")
API1 = os.getenv("Token1")
ID = os.getenv("ID")


bot = telebot.TeleBot(API)
username = []
username_rem = []
my_file = open("listfile.txt", "r")
data = my_file.read()
username1 = data.split("\n")
for n in username1:
  if n.startswith('@') == True:
    username.append(n)

my_file1 = open("data.txt", "r")
data1 = my_file1.read()
username2 = data1.split("\n")
for n in username2:
  if n.startswith('@') == True:
    username_rem.append(n)
    
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
        bot.reply_to(message, "Hello! I'm your Telebtot. How can I assist you?")
    
    @bot.channel_post_handler(commands=['help'])
    def handle_channel_help(message):
        bot.reply_to(message, "Here are the available commands:\n"
                              "/start - Start the bot\n"
                              "/help - Get help")
    
    @bot.channel_post_handler(commands=['add'])
    def handle_channel_add(message):
        if message.text.startswith('/add ') and message.text[5:].startswith('@'):
            if message.text[5:] in username:
                bot.reply_to(message, f'{message.text[5:]} User is already included...')
            else:
                username.append(message.text[5:])
                bot.reply_to(message, f'{message.text[5:]} is added to your account list')
                bot.reply_to(message, '-------╔( •̀ з •́)╝╚(•̀ ▪ •́ )╗-------')
                with open('listfile.txt', 'w') as f:
                  for n in username:
                    f.write(n + '\n')
                restart_program()
    
    @bot.channel_post_handler(commands=['rem'])
    def handle_channel_rem(message):
        if message.text.startswith('/rem ') and message.text[5:].startswith('@'):
            if message.text[5:] not in username:
                bot.reply_to(message, f'{message.text[5:]} User is not included...')
            else:
                username.remove(message.text[5:])
                with open('listfile.txt', 'w') as f:
                  for n in username:
                    f.write(n + '\n')
                bot.reply_to(message, f'{message.text[5:]} is removed')
                bot.reply_to(message, '-------〵(•ʘ̥ᴗʘ̥ •〵)-------')
                username_rem.append(message.text[5:])
                with open('data.txt', 'w') as f:
                  for n in username_rem:
                    f.write(n + '\n')
                restart_program()
    
    @bot.channel_post_handler(commands=['ls'])
    def handle_channel_ls(message):
        if message.text.startswith('/ls'):
            bot.reply_to(message, f'{str(username)} Total account is: {len(username)}')
            bot.reply_to(message, '╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮')
    bot.polling()
    


################################ using twstalker #############################:


def get_tweet_by_username(username, counter_max=10, replies=False):
    """Retrieves tweets from a specified Twitter username using the nitter search feature.
  
      Arguments:
          - username (str): The Twitter username of the user whose tweets are to be retrieved.
          - counter: Define the maximum number of tweets to retrive.
          - replies (bool, optional): A boolean value that indicates whether to retrieve all tweets (including replies) or only the tweets posted by the user. Defaults to False.
  """
    if replies == True:
        url = f"https://nitter.salastil.com/{username}/with_replies"
    else:
        url = f"https://nitter.salastil.com/{username}"
    try:
      headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
      response = requests.get(url, headers=headers)
      #print(response.status_code)
      time.sleep(2)
      if response.status_code != 200:
          return 'Request error'
      tweets = response.content
      if tweets:
          soup = BeautifulSoup(tweets, 'html.parser')
          tweets = soup.find_all('div', class_='timeline-item')
          
          counter = 0  # Counter to keep track of number of tweets processed
          tweets_list = []
          users = []
          for i, tweet in enumerate(tweets):
              if len(tweets_list) < counter_max:
                  #print(f"i am here {i}")
                  if 'retweeted' in str(tweet):
                      tweet_text = f"RT: {tweet.find('a', class_='username').text} \n{tweet.find('div', class_='tweet-content').text.strip()}"
                      #print("retweeted text")
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
                  #tweet_stats = [stat.text for stat in tweet.find_all('span', class_='tweet-stat')]
          
                  # Create dictionary to store tweet data
                  tweet_data = (tweet_date,  tweet_id, tweet_text, tweet_pinned, tweet_url)
                
                  #print(i)
                  tweets_list.append(tweet_data)
          return tweets_list
            
      else:
          print("Tweets not found")
            
    except Exception as e:
      print(f" Error: {e}")
      return None




def scheduled_function():
  #report("it has been one hour bro")
  print("it has been one hour")
print('/////////PROGRAM RUNNING////////')


def main_function():
    result2 = []
    rep_remove = []
    item = 0
    while item < 1000000000000000000:

      result = []

      for j in range(0, len(username)):
        user_name = username[j][1:]
        tweet_list1 = ()
        try:
            for trial in range (0, 3):
                try:
                    tweet_result = get_tweet_by_username(user_name)
                    #print(len(tweet_result))
                    if len(tweet_result) != 0:
                        tweet_list1 = tweet_result
                        break
                except Exception as e:
                        print(trial + "trial, We cannot get any data because of the error: "+ e)
            if str(tweet_result) == 'Request error':
                print("EQUEST ERROR")
                result.append(result2[j])
                continue
            if tweet_list1 == ():
                report(f'ATTENTION: we cannot get any data from::{username[j]} so it is REMOVED')
                
                if username[j] not in username_rem:
                  username_rem.append(username[j])
                  with open('data.txt', 'w') as f:
                    for n in username_rem:
                      f.write(n + '\n')
                print(username[j])
                username.remove(username[j])
                with open('listfile.txt', 'w') as f:
                  for n in username:
                    f.write(n + '\n')
                item = -1
                break
              
            result.append(tweet_list1) 
            if item == 0:
                print(f'{j + 1}  ------- this is the first trial of {username[j]}')
                continue
            previous_set = set(result2[j])
            new_set = set(result[j][:6])
            changed_items = list(new_set - previous_set)
            if len(previous_set) == 0:
                pass
            else:
                for po in changed_items:
                    Date, Id, text, Pin, url = po
                    message = f".  \n{username[j]} \n{text}\n {url} at {Date}"
    
                    if "#" in text:
                        text_edit = text.replace("#", "~")
                        mess = f'.\n{username[j]} \n{text_edit} \n{url} at {Date}'
                        report(mess)
                    elif "&" in text:
                        mess = f"{result[j][po]['URL']}"
                        report(url)
                    else:
                        report(message)
    
                # print(result[j][0]['Text'])

        except Exception as e:
            print(e)
      #report (f'$$$$$$$$$$ {e} $$$$$$$$$$$ at account {username[j]} first')
      
      result2 = result
      time.sleep(20)
      print(item)
      item += 1



keep_alive()  
bot.polling


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
    



