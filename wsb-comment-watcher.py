import praw
import stomp

import config

# Pull these from a configuration file
conn = stomp.Connection([('192.168.1.246', 61613)])
conn.connect('admin', 'admin', wait=True)

def execute_app():
    # Pull these from a configuration file
    reddit = praw.Reddit(user_agent=config.user_agent,
                         client_id=config.client_id, client_secret=config.client_secret,
                         username=config.username, password=config.password)
    subreddit = reddit.subreddit("wallstreetbets")
    for comment in subreddit.stream.comments(skip_existing=True):
        conn.send(body=comment.body, destination='reddit.comment.parser.raw')


def handle_cleanup():
    conn.disconnect()


def main():
    try:
        execute_app()
    finally:
        handle_cleanup()

if __name__=='__main__':
    main()