
def commands():
    """
  Defines Telegram bot commands for managing monitored users and bot settings.

  This function creates Telegram bot command handlers for various actions:
      - `/start`: Provides a greeting message.
      - `/help`: Lists available commands.
      - `/add <@username>`: Adds a Twitter username to the monitored list.
      - `/rem <@username>`: Removes a Twitter username from the monitored list (but keeps it for reactivation).
      - `/del <@username>`: Permanently deletes a Twitter username from the monitored list.
      - `/ls`: Lists all usernames currently monitored.
      - `/replies {true/false}`: Enables/disables including replies in the monitoring.
      - Handles all other messages, prompting the user with available commands.
  """
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
                mongo_update(data)

            else:
                try:
                    user_name = message.text[6:]
                    print(user_name)
                    app = Twitter("session")
                    app.connect()
                    id = app.get_user_id(user_name)
                    data["usernames"][message.text[5:]] = {
                        "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "recent_tweets": [],
                        "total_tweet" : 0,
                        "day_tweets" :0,
                        "Active" : True,
                        "User_ID" : id
                    }

                    bot.reply_to(message, f'{message.text[5:]} is added to your account list\n-------╔( •̀ з •́)╝╚(•̀ ▪ •́ )╗-------')

                    mongo_update(data)
                    restart_program()
                except Exception as e:
                    bot.reply_to(message, f'{message.text[5:]} is not a twitter user. Please try again')
                    print(e)

    @bot.channel_post_handler(commands=['rem'])
    def handle_channel_rem(message):
        if message.text.startswith('/rem ') and message.text[5:].startswith('@'):
            if message.text[5:] not in username:
                bot.reply_to(message, f'{message.text[5:]} User is not included...')
            else:
                data["usernames"][message.text[5:]]["Active"] = False
                bot.reply_to(message, f'{message.text[5:]} is removed\n-------〵(•ʘ̥ᴗʘ̥ •〵)-------')
                mongo_update(data)
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
        data["replies"] = not replies
        bot.reply_to(message, f'THE REPLIES HAVE BEEN CHANGED : {data["replies"]}')
        mongo_update(data)


    bot.polling()
