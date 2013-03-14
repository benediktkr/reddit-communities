import sqlite3
import crawler
from datetime import datetime

cnxn = sqlite3.connect('data/reddit.db')
cursor = cnxn.cursor()

for s in cursor.execute("select name from subreddits").fetchall():
    if type(s) == type(int):
        print "!!!!!", s
    subreddit = s[0]
    subscribers = crawler.linked_subreddits(subreddit)['subscribers']
    print subreddit, subscribers
    cursor.execute("update subreddits set subscribers=?, date=? where name=?",
                   (subscribers, subreddit, datetime.now()))

    cnxn.commit()
cnxn.close()
