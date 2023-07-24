# importing libraries and packages
import snscrape.modules.twitter as sntwitter
import pandas as pd
import time
import requests
from KeepAlive import keep_alive
from collections import Counter
from bs4 import BeautifulSoup
from os import system
import threading
import schedule
import warnings
import os
import sys
import psutil
import logging

warnings.simplefilter(action='ignore', category=FutureWarning)

API = os.getenv("Token")
API1 = os.getenv("Token1")
ID = os.getenv("ID")
 
'''def get_id():

    text = 'https://api.telegram.org/bot' + API + '/getupdates'

    response = requests.get(text)
    return response.json()

#print(get_id()['result'])
result1 = str(get_id()['result'][0]['channel_post']['chat']['id'])'''


def telegram_bot_sendtext(bot_message):

  #send_text = 'https://api.telegram.org/bot' + API + '/sendMessage?chat_id=' + ID + '&parse_mode=Markdown&text=' + bot_message

  send_text = f'https://api.telegram.org/bot{API}/sendMessage?chat_id={ID}&parse_mode=Markdown&text={bot_message}'

  response = requests.get(send_text)

  return response.json()





def report(my_message):

  #my_message = "this is dawit neri"

  telegram_bot_sendtext(my_message)


#username = ['@elonmusk', '@berachain', '@shibarium_', '@reda_getachew', '@CryptoUnic', '@0revenue', '@0xUnihax0r', '@milesdeutscher', '@VitalikButerin', '@cryptocross0ver', '@Rekt_Tekashi', '@pepe_linnn']


def telegram_bot_corrector(bot_message):

  send_text = 'https://api.telegram.org/bot' + API1 + '/sendMessage?chat_id=' + ID + '&parse_mode=Markdown&text=' + bot_message

  response = requests.get(send_text)

  return response.json()

# get the word that has "$" in it
def counter(word):
  t = list(filter(lambda word: word[0]=='$', word.split()))
  my_dollar = open("dollar.txt", "r")
  data = my_dollar.read()
  dol_list = []
  tokens = data.split("\n")
  while '' in tokens:
    tokens.remove('')
  for text in t:
      if text.startswith("$"):
          tokens.append(text)
  # lets count the value
  dol_dict = Counter(tokens)
  print(dol_dict)
  # return the counted value into list
  dol_list = list(dol_dict.elements())
  # lets rewrite this back
  with open('dollar.txt', 'w') as f:
      for n in dol_list:
          f.write(n + '\n')

def get_tweet_by_username(username, counter_max=5, replies=False):
    """Retrieves tweets from a specified Twitter username using the nitter search feature.
  
      Arguments:
          - username (str): The Twitter username of the user whose tweets are to be retrieved.
          - counter: Define the maximum number of tweets to retrive.
          - replies (bool, optional): A boolean value that indicates whether to retrieve all tweets (including replies) or only the tweets posted by the user. Defaults to False.
  """
    if replies == True:
        url = f"https://nitter.projectsegfau.lt/search?f=tweets&q=from%3A{username}"
    else:
        url = f"https://nitter.projectsegfau.lt/{username}"
    try:
      response = requests.get(url)
      time.sleep(3)
      tweets = response.content
      if tweets:
          soup = BeautifulSoup(tweets, 'html.parser')
          tweets = soup.find_all('div', class_='timeline-item')
          
          counter = 0  # Counter to keep track of number of tweets processed
          tweets_list = []
          for tweet in tweets:
              if counter <= counter_max:
                  if tweet.find('div', class_='replying-to'):
                      tweet_text = f"Repying to: {tweet.find('div', class_='replying-to').find('a').text.strip()} - " + tweet.find('div', class_='tweet-content').text.strip()
                  else:
                      tweet_text = tweet.find('div', class_='tweet-content').text.strip()
                    
                  tweet_url = tweet.find('a', class_='tweet-link')['href']
                  tweet_id = tweet_url.split('/')[-1][:19]
                  tweet_url = f"https://vxtwitter.com/{username}/status/{tweet_id}"
                  tweet_date = tweet.find('span', class_='tweet-date').find('a')['title']
                  #tweet_stats = [stat.text for stat in tweet.find_all('span', class_='tweet-stat')]
                  tweet_data = [tweet_date,  tweet_id, tweet_text, f"@{username}", tweet_url]
                
                  #print(tweet_data)
                  tweets_list.append(tweet_data)
                  counter += 1
          return tweets_list
            
      else:
          print("Tweets not found")
            
    except Exception as e:
      print(f" Error: {e}")
    #return None

def scheduled_function():
  #report("it has been one hour bro")
  print("it has been one hour")
print('/////////PROGRAM RUNNING////////')


def main_function():
    result2 = []
    rep_remove = []
    item = 0
    while item < 1000000000000000000:
      #print('/////////item////////  ', item)
      if item == 0:
        my_file = open("listfile.txt", "r")
        username = []
        data = my_file.read()
        username1 = data.split("\n")
        for n in username1:
          if n.startswith('@') == True:
            username.append(n)
        #print(username, len(username))
      try:
        base_url = f'https://api.telegram.org/bot{API}/getUpdates'
        resp = requests.get(base_url)
        data = resp.json()
        item1 = data["result"]
        # new1 = item1[len(item1)-1]['channel_post']['text']
        new1 = item1[len(item1) - 1]['channel_post']['text']
        if new1.startswith(
            '/add ') and new1[5:] not in username and new1[5:].startswith('@'):
          username.append(new1[5:])
          report(f'{new1[5:]} is added to your account list')
          item = 0
          telegram_bot_corrector('-------╔( •̀ з •́)╝╚(•̀ ▪ •́ )╗-------')
    
        if new1.startswith(
            '/rem ') and new1[5:] in username and new1[5:].startswith('@'):
          username.remove(new1[5:])
          report(f'{new1[5:]} is removed')
          item = 0
          telegram_bot_corrector('-------〵(•ʘ̥ᴗʘ̥ •〵)-------')
    
        if new1.startswith('/ls'):
          report(f'{str(username)} Total account is: {len(username)}')
          #print(f'{str(username)} Total account is: {len(username)}')
          telegram_bot_corrector('╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮')
        if new1.startswith('/try'):
          username_try = []
          try_mess_1 = f''
          my1 = open("data.txt", "r")
          d1 = my1.read()
          un3 = d1.split("\n")
          for n in un3:
            if n.startswith('@') == True:
              username_try.append(n)
          for i in range(0, len(username_try)):
            try_mess_0 = f'{i+1}, {username_try[i]}'
            try_mess_1 = try_mess_1 + try_mess_0 + '\n'
          #print(new1)
    
          report(try_mess_1)
          telegram_bot_corrector('╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮')
    
      except Exception as e:
        
        print(f'$$$$$$$$$$ {e}, at {n} $$$$$$$$$$$ ')
    
        telegram_bot_corrector('乁(҂◡̀﹏◡́)ㄏ fixed it 乁(҂◡̀﹏◡́)ㄏ')
        #username.remove(n)
        
      finally:
        
        with open('listfile.txt', 'w') as f:
          for n in username:
            f.write(n + '\n')
        
      result = []
      for j in range(0, len(username)):
        user_name = username[j][1:]
        tweet_list1 = []
        res = []
        try:
            while True:
                tweet_result = get_tweet_by_username(user_name)
                if len(tweet_result) > 1:
                    #print(tweet_result)
                    tweet_list1.append(tweet_result)
                    break
                time.sleep(1)
        except Exception as e:
            print(e)
            item = -1
            print(item)
        res = pd.DataFrame(tweet_list1[0],columns=['Datetime', 'Tweet Id', 'Text','username', 'URL'])
        #print(res)
        result.append(res)
  

        try:
          po = 0
          while po <= 6:
            if item == 0:
              print(f'{j + 1}  ------- this is the first trial of {username[j]}')
              break
    
            if result2[j].iat[0, 2] == result[j].iat[po, 2]:
              #print(f'breaked here at item {item}')
              break
    
            if result2[j].iat[0, 2] != result[j].iat[po, 2] and result2[j].iat[
                1, 2] != result[j].iat[0, 2]:
    
              t1 = str(result[j].iat[po, 0])
              #print(t1[:18])
              rv = result[j].iat[po, 2]
              yv = rv[:16]
              url = result[j].iat[po, 4]
              message = f".  {username[j]} \n{rv}\n {url} at {t1[:19]}"
          
              if rv.startswith('@') == False and yv not in rep_remove:
                if "#" in rv:
                  tv = rv.replace("#", "~")
                  mess = f'.  {username[j]} \n{tv} \n{url} at {t1[:19]}'
                  report(mess)
                  print(mess)
                elif "&" in rv:
                  mess = f'{result[j].iat[po, 4]}'
                  report(url)
                  print(mess)
                else:
                  report(message)
                  print(message)
                rep_remove.append(yv)
              #print(result[j].iat[0, 2])
            po += 1
    
        except Exception as e:
          print(f'this is {e}')
      
          report(f'ATTENTION: {username[j]} is removed because of {e}')
          my_file1 = open("data.txt", "r")
          username_rem = []
          data1 = my_file1.read()
          username2 = data1.split("\n")
          for n in username2:
            if n.startswith('@') == True:
              username_rem.append(n)
          if username[j] not in username_rem:
            username_rem.append(username[j])
            with open('data.txt', 'w') as f:
              for n in username_rem:
                f.write(n + '\n')
          print(username[j])
          #username1.remove(username1[j])
          with open('listfile.txt', 'w') as f:
            for n in username1:
              f.write(n + '\n')
          item = -1
    #report (f'$$$$$$$$$$ {e} $$$$$$$$$$$ at account {username[j]} first')
    
      result2 = result
    
      #print(result[0].iat[6, 0])
      #print(item)
      print(item)
      # print(rep_remove)
    
      item += 1

    
    report("MASTER i have stopped working: PLEASE fix me ;")




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


keep_alive()  


try:
    main_function()
except Exception as e:
    print(e)
    report(e)

#restart_program()

