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
import logging



API = os.getenv("Token")
API1 = os.getenv("Token1")
ID = os.getenv("ID")


def report(message, token):
    send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={ID}&text={message}'
    try:
        response = requests.get(send_text)
        if response.status_code == 200 and response.json()['ok']:
            print(message)
            return response.json()
        else:
                # If there was an error, log the error and wait for a short period before retrying
            print(f"Failed to send message: {response.json()['description']}")
            time.sleep(1)
    except Exception as e:
            # If there was an exception, log the exception and wait for a short period before retrying
        print(f"Failed to send message: {e}")
        time.sleep(1)


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
                  #tweet_stats = [stat.text for stat in tweet.find_all('span', class_='tweet-stat')]
          
                  # Create dictionary to store tweet data
                  tweet_data = [tweet_date,  tweet_id, tweet_text, username, tweet_url]
                
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
      if username == []:
          break
      try:
        base_url = f'https://api.telegram.org/bot{API}/getUpdates'
        resp = requests.get(base_url)
        data = resp.json()
        item1 = data["result"]
        # new1 = item1[len(item1)-1]['channel_post']['text']
        new1 = item1[len(item1) - 1]['channel_post']['text']
        #print(new1)
        if new1.startswith(
            '/add ') and new1[5:].startswith('@'):
          if new1[5:] in username:
              report(f'{new1[5:]} User is  already included...', API1)
          else:
              username.append(new1[5:])
              report(f'{new1[5:]} is added to your account list', API)
              item = 0
              report('-------╔( •̀ з •́)╝╚(•̀ ▪ •́ )╗-------', API1)
        if new1.startswith(
            '/rem ')  and new1[5:].startswith('@'):
          if new1[5:] not in username:
              report(f'{new1[5:]} User is not included...', API1)
          else:
              username.remove(new1[5:])
              report(f'{new1[5:]} is removed', API)
              item = 0
              report('-------〵(•ʘ̥ᴗʘ̥ •〵)-------', API1)
      
        if new1.startswith('/ls'):
          report(f'{str(username)} Total account is: {len(username)}', API)
          #print(f'{str(username)} Total account is: {len(username)}')
          report('╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮', API1)
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
    
          report(try_mess_1, API)
          report('╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮    ╭∩╮(︶0︶)╭∩╮', API1)
    
      except Exception as e:
        
        print(f'$$$$$$$$$$ {e}, at {n} $$$$$$$$$$$ ')
    
        report('乁(҂◡̀﹏◡́)ㄏ fixed it 乁(҂◡̀﹏◡́)ㄏ', API1)
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
            for trial in range (0, 3):
                try:
                    tweet_result = get_tweet_by_username(user_name)
                    #print(len(tweet_result))
                    if len(tweet_result) != 0:
                        tweet_list1.append(tweet_result)
                        break
                except Exception as e:
                        print(trial + "trial, We cannot get any data because of the error: "+ e)
                
            if tweet_list1 == []:
                report(f'ATTENTION: we cannot get any data from::{username[j]} so it is REMOVED', API)
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
                username.remove(username[j])
                with open('listfile.txt', 'w') as f:
                  for n in username:
                    f.write(n + '\n')
                item = -1
                break
            else:
               # create a list of dictionaries with keys as column names
              res = [{'Datetime': tweet[0], 'Tweet Id': tweet[1], 'Text': tweet[2], 'username': tweet[3], 'URL': tweet[4]} for tweet in tweet_list1[0]]
              result.append(res)
              
              po = 0
              while po <= 6:
                  if item == 0:
                      print(f'{j + 1}  ------- this is the first trial of {username[j]}')
                      break

                  tweet_ids = [tweet['Tweet Id'] for tweet in result[j]]
                  tweet_ids_2 = [tweet['Tweet Id'] for tweet in result2[j]]

              
                  if result2[j][0]['Tweet Id'] == result[j][po]['Tweet Id'] or tweet_ids.index(result2[j][6]['Tweet Id']) < tweet_ids_2.index(result2[j][6]['Tweet Id']):
                      if tweet_ids.index(result2[j][6]['Tweet Id']) < tweet_ids_2.index(result2[j][6]['Tweet Id']):
                          print("There is a deleted tweet")
                      break
              
                  if result2[j][0]['Text'] != result[j][po]['Text'] and result2[j][1]['Text'] != result[j][0]['Text']:
                      t1 = str(result[j][po]['Datetime'])
                      # print(t1[:18])
                      text = result[j][po]['Text']
                      url = result[j][po]['URL']
                      message = f".  \n{username[j]} \n{text}\n {url} at {t1}"
                      my_ids = open("ids.txt", "r")
                      ids_list = (my_ids.read()).split("\n")
                      id = result[j][po]['Tweet Id']
                      if id not in rep_remove:
                          if "#" in text:
                              text_edit = text.replace("#", "~")
                              mess = f'.\n{username[j]} \n{text_edit} \n{url} at {t1}'
                              report(mess, API)
                          elif "&" in text:
                              mess = f"{result[j][po]['URL']}"
                              report(url, API)
                          else:
                              report(message, API)
                          ids_list.insert(0, str(id))
                          ids_list = ids_list[:50]
                          with open('ids.txt', 'w') as f:
                                for i in ids_list:
                                      f.write(i + '\n')
                      # print(result[j][0]['Text'])
                  po += 1
        except Exception as e:
            print(e)
      #report (f'$$$$$$$$$$ {e} $$$$$$$$$$$ at account {username[j]} first')
      
      result2 = result
      print(item)
      item += 1

    
    report("MASTER i have stopped working: PLEASE fix me ;", API)




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
    restart_program()
    print(e)


restart_program()
