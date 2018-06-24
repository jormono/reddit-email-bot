# reddit-email-bot
bot that emails the user when a new post is made in specified subreddits matching specified keywords

To use, you will need to enter your information on the credentials.py file

For my own personal use, the e-mail address I send the notifications to is the address for my verizon cell phone, meaning these messages appear as text messages.
Will of course work with a regular e-mail account, just food for thought.

The reddit_email_bot.py file needs to be supplied keywords to search for, and subreddits to search in, in its current state it will yield a lot of junk responses (works great for testing though) These keywords and subreddits are setup in a dictionary now, dictionary key is subreddit, search term/phrase is the value. Values should be a list of strings, keys should be just strings.


When both files have been set up, you simmply need to run the reddit_email_bot.py file on your computer!
