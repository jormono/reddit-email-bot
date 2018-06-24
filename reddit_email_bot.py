import praw
import time
import smtplib
from credentials import reddit_client_id, reddit_client_secret, reddit_password, reddit_user_agent, reddit_username, email_bot_address, email_bot_password, email_user_address
'''Reddit Bot Portion Based at r/RequestABot authored by /u/John_Yuki.
Modification for sending e-mail and for criteria by dictionary by /u/jormono'''

# The keywords or phrases that the bot looks for.
# changed from 2 lists to one dictionary, this should let you set search value per subreddit
criteria = {
    'news': ['o'],
    'politics': ['i', 'a', 'u'],
    'AskReddit': ['e']}

criteria_keys = '+'.join(criteria.keys())

try:
    reddit = praw.Reddit(username = reddit_username,
        password = reddit_password, client_id = reddit_client_id,
        client_secret = reddit_client_secret, user_agent = reddit_user_agent)
except Exception as e:
    print(e)
    print('Reddit connection issue')
    time.sleep(60)

# Main program:
def send_message(submission, reddit):
    try:
        # e-mail message
        post_title = submission.title
        if len(str(submission.title))>137: # message character limit minus length of url
            post_title = str(post_title)[:130] + '...' # if title exceeds character limit for message this trims it up
        msg = 'From: {}\nTo: {}\n{} \n {}'.format(email_bot_address, email_user_address, post_title, submission.shortlink)
        mail = smtplib.SMTP('smtp.gmail.com', 587) # specific to gmail
        mail.ehlo()
        mail.starttls()
        mail.login(email_bot_address, email_bot_password)
        mail.sendmail(email_bot_address, email_user_address, msg.encode('utf-8')) # added encode uf-8 due to error that kept coming up
        mail.quit()
        print('Sent new message') # This line is for testing purposes.
    except Exception as e:
        print(e)
        print('email issue')
        time.sleep(60)
        
def find_submissions():
    try:
        while True:
            start_time = time.time()
            for submission in reddit.subreddit(criteria_keys).stream.submissions():
                for keyword in criteria[str(reddit.subreddit(str(submission.subreddit)))]:
                    if keyword.lower() in submission.title.lower() and submission.created_utc > start_time:
                        send_message(submission, reddit)
                        break
    except Exception as e:
        print(e)
        print('Reddit search issue')
        time.sleep(60)

if __name__ == '__main__':
    find_submissions()
