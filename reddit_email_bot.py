import praw
import time
import smtplib
from credentials import reddit_client_id, reddit_client_secret, reddit_password, reddit_user_agent, reddit_username, email_bot_address, email_bot_password, email_user_address

'''Reddit bot portion from r/RequestABot authored by /u/John_Yuki.
Modification for sending e-mail by /u/jormono'''

# The keywords or phrases that the bot looks for.
# Keywords and phrases are NOT case sensitive. However it will match them literally, so make sure you spell them correctly.
keywords = ['test', 'example', 'another example']

# You can have 1 subreddit or multiple. If you have multiple, separate them with + symbols like I have done in the example.
# Also, you do not need to include the "/r/" part, just the name of the subreddit as shown in the example.
# The subreddit can also just be "all" if you want it to search through every subreddit in existence. (Might get spammy if you have a common or a lot of keywords).
subreddits = 'news+askreddit'

try:
    reddit = praw.Reddit(username = reddit_username,
        password = reddit_password, client_id = reddit_client_id,
        client_secret = reddit_client_secret, user_agent = reddit_user_agent)
except Exception as e:
    print(e)
    time.sleep(60)

# Main program:
def send_message(submission, reddit):
    try:
        # e-mail message
        msg = 'From: {}\nTo: {}\n{} \n {}'.format(email_bot_address, email_user_address, submission.title, submission.shortlink)
        mail = smtplib.SMTP('smtp.gmail.com', 587) # setup for gmail, if not using gmail will need to change this
        mail.ehlo()
        mail.starttls()
        mail.login(email_bot_address, email_bot_password)
        mail.sendmail(email_bot_address, email_user_address, msg)
        mail.quit()
        print('Sent new message') # This line is for testing purposes.
    except Exception as e:
        print(e)
        time.sleep(60)
        
        
def find_submissions():
    try:
        while True:
            start_time = time.time()
            for submission in reddit.subreddit(subreddits).stream.submissions():
                for keyword in keywords:
                    if keyword.lower() in submission.title.lower() and submission.created_utc > start_time:
                        send_message(submission, reddit)
                        break
    except Exception as e:
        print(e)
        time.sleep(60)

if __name__ == '__main__':
    find_submissions()
