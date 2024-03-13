# 🤖 **Twitter to Telegram Bot: Stayin' Informed with the Tweet Avalanche!** ➡️

This README is your one-stop guide to understanding and using the super cool Python code for a bot that acts like a tweet-retrieving superhero 🦸‍♀️, bringing the latest tweets from your favorite accounts straight to your Telegram channel! 

## What it Does:
🔎 Scans Twitter Accounts: Like a tireless detective 🕵️‍♂️, the bot keeps a watchful eye on a list of Twitter usernames you provide.
📥 Grabs New Tweets (Optional Replies Too!): It swoops in and snatches up any new tweets (including replies, if you want them ✉️) from those accounts.
📩 Sends Them to Your Telegram Channel: Faster than a speeding tweet ⚡️, the bot delivers those fresh tweets directly to your designated Telegram channel, keeping you in the loop 🪢.
👤 Manages Usernames with Ease: Feeling overwhelmed by all the tweets? No worries! The bot provides special Telegram channel commands 📜 that let you add, remove, or even delete usernames from the monitored list.
📆 Daily Reports Keep You Informed: Every day at noon (like a clockwork owl 🦉!), the bot sends you a report summarizing the number of tweets retrieved for each user.


## What You'll Need:
✔️ Python 3 (the coding language that makes the magic happen 🪄)
✔️ These awesome libraries (pip install them to join the party):
   - telebot (talks to Telegram for you 📲)
   - tweepy (chats with Twitter like a pro 🐦)
   - pymongo (keeps track of things in a fancy database 💾)
   - schedule (makes sure things happen on time ⏰)
   - and a few other helpful ones
✔️ Your own unique Telegram bot token (find it in the BotFather settings 🤖)
✔️ A MongoDB connection string (where the bot stores its info 🗃️)

## Why Authentication is Needed:
⚠️ **Important Update:** Twitter has recently discontinued unauthorized scraping, which means users must now authorize their access to Twitter. Previously, the bot was programmed to directly scrape from Nitter, an alternative front end for Twitter that provided guest tokens for scraping. However, with this recent update, authentication is now required to access Twitter's data.

To authorize and obtain the session for the bot, please refer to the [Signing In — Tweety 1.0.9.6 documentation](https://mahrtayyab.github.io/tweety_docs/basic/singing-in.html). This documentation provides step-by-step instructions on how to sign in to Twitter using Tweety. Once you have obtained the authenticated session file, named 'session.tw_session', you can load the session using the `connect` method.

To obtain the session information of a webpage, you can navigate to the website and open the Developer Tools by right-clicking on the page and selecting "Inspect." In the "Network" tab of the Developer Tools, you can locate the initial request sent to the server, and the session information can be found there.

⚠️ **Note on Rate Limiting:**
Please be aware that the authentication method used in this bot is subject to rate limiting imposed by Twitter. To avoid hitting the rate limit, it is recommended to introduce longer gaps between each scan or consider using multiple Twitter accounts. You can use sessions from different accounts one after the other to distribute the load and avoid exceeding the rate limit.

## Getting Started (It's Easy Peasy!):
1. Install the libraries (mentioned above) using pip.
2. Grab the code and replace these placeholders with your info:
   - API : Your Telegram bot token (don't share this with anyone! 🔒)
   - ID : The ID of your Telegram channel (where the tweets will land 📢)
   - URL : Your MongoDB connection string (keep your data safe 🔐)
3. Generate the session file ('session.tw_session') by following the link i provided.
4. Run the script from the command line:
5. 
   ```bash
   python twitter_to_telegram.py
   ```

🚨 **Use code with caution.**

## Telegram Channel Commands (Be the Boss!):
- /start: Gets things going (use this initially, but not required afterwards).
- /help: Confused? This command shows you all the available commands (like a helpful genie 🧞‍♀️).
- /add <@username>: Want to add a new Twitter account to the monitored list? Use this command!
- /rem <@username>: Feeling overwhelmed? This command removes a username from the list (but don't worry, you can bring it back later!).
- /del <@username>: Need to permanently delete a username? This command does the trick (bye-bye birdie 🐦).
- /ls: Curious to see all the usernames currently monitored? This command shows you the list.
- /replies {true/false}: Want to include replies in the monitoring? Set it to true or exclude them with false (the choice is yours! ✔️/❌).

## Additional Notes:
- The script uses a fancy multi-threading approach (like having multiple superheroes working together 🦸‍♂️) to handle tweet monitoring and Telegram communication at the same time.
- It uses MongoDB as its memory palace to store information about monitored users and retrieved tweets.
- The script schedules reports and data checks to keep things running smoothly (like a well-oiled machine ⚙️).

⚠️ **Disclaimer:**
If the account is rate limited you can not access twitter using that account. So use an account that you are not going to use for day to day activity. You can finetune the code as you will.

Please let me know if there's anything else I can help you with! 🎉

## Credits 🙌

This project was created by **Dawit Neri**

## Support 💬

If you encounter any issues or have any questions, feel free to reach out to dawitneri888@gmail.com or open an issue in the GitHub repository.
