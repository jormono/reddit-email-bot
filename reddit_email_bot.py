#! python3
import praw
import time
import smtplib
import logging
from credentials import reddit_client_id, reddit_client_secret, reddit_password, reddit_user_agent, reddit_username, email_bot_address, email_bot_password, email_user_address
'''Reddit Bot Portion Based at r/RequestABot authored by /u/John_Yuki.
Modification for sending e-mail by /u/jormono'''

logging.basicConfig(filename='reddit_message_bot_error_log.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def initialize():
    try:
        # e-mail message
        msg = 'From: {}\nTo: {}\n***BEEP BOOP*** Initializing Stream'.format(email_bot_address, email_user_address)
        mail = smtplib.SMTP('smtp.gmail.com', 587) # specific to gmail
        mail.ehlo()
        mail.starttls()
        mail.login(email_bot_address, email_bot_password)
        mail.sendmail(email_bot_address, email_user_address, msg.encode('utf-8'))
        mail.quit()
        logging.info('Sent initializing message') # This line is for testing purposes.
    except Exception as e:
        logging.warning(e)
        logging.debug('email issue')
        time.sleep(60)
        
initialize()

# The keywords or phrases that the bot looks for.
criteria = {
    'AskReddit': ['e'],
    'politics': ['i','o'],
    'news': ['u', 'a']
    }

criteria_keys = '+'.join(criteria.keys())

try:
    reddit = praw.Reddit(username = reddit_username,
        password = reddit_password, client_id = reddit_client_id,
        client_secret = reddit_client_secret, user_agent = reddit_user_agent)
except Exception as e:
    logging.warning(e)
    logging.debug('Reddit connection issue')
    time.sleep(60)

# Main program:
def send_message(submission, reddit):
    try:
        # e-mail message
        post_title = submission.title
        if len(str(submission.title))>137:
            post_title = str(post_title)[:130] + '...'
        msg = 'From: {}\nTo: {}\n{} \n {}'.format(email_bot_address, email_user_address, post_title, submission.shortlink)
        mail = smtplib.SMTP('smtp.gmail.com', 587) # specific to gmail
        mail.ehlo()
        mail.starttls()
        mail.login(email_bot_address, email_bot_password)
        mail.sendmail(email_bot_address, email_user_address, msg.encode('utf-8'))
        mail.quit()
        logging.info('Sent new message')
    except Exception as e:
        logging.warning(e)
        lgging.debug('email issue')
        time.sleep(60)
        
def find_submissions():
    try:
        while True:
            start_time = time.time()
            for submission in reddit.subreddit(criteria_keys).stream.submissions():
                for keyword in criteria[str(reddit.subreddit(str(submission.subreddit)))]:
                    if keyword.lower() in submission.title.lower() and submission.created_utc > start_time:
                        send_message(submission, reddit)
                        continue
    except Exception as e:
        logging.warning(e)
        logging.debug('Reddit search issue')
        time.sleep(60)
        
if __name__ == '__main__':
    find_submissions()
