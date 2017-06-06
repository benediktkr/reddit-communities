## Ugh.
from datetime import datetime
import sqlite3
import os

"""Removed in favor of .get() @classmethod
def singleton(class_):
    _instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in _instances:
            print "New instnace"
            _instances[class_] = class_(*args, **kwargs)
        return _instances[class_]
    return getinstance"""

#@singleton

# bad name, just python-to-sqlite
class DBModel(object):
    def __init__(self, connection):
        self.cnxn = connection
        #self.cursor = connection.cursor()

    @classmethod
    def get(cls):
        if not os.path.isfile('data/reddit.db'):
            return cls.new()
        conn = sqlite3.connect('data/reddit.db')
        return cls(conn)

    @classmethod
    def new(cls):
        print "Creating new DB..."
        conn = sqlite3.connect('data/reddit.db')
        dbmodel = cls(conn)
        dbmodel.createnew()
        return dbmodel

    def commit(self):
        self.cnxn.commit()

    def save_comment(self, username, subreddit):
        sql = """insert or replace into comments(username, subreddit)
                 values(?, ?)"""
        self.cnxn.execute(sql, (username, subreddit))
        self.cnxn.commit()

    def get_comments_generator(self):
        sql = "select username, subreddit from comments"
        for row in self.cnxn.execute(sql):
            yield row

    def get_comment_links(self, target):
        sql = "select * from comments_mapping where vertex0=? or vertex1=?"
        return self.cnxn.execute(sql, (target, target))

    def save_comment_link(self, link):
        # i can be a dumb programmer too, mismatch between name i sql and python
        self.cnxn.execute("insert or replace into comments_mapping values(?, ?)", link)

    def save_link(self, link):
        sql = "insert or replace into comments_mapping values(?, ?)"
        self.cnxn.execute(sql, link)
        self.cnxn.commit()

    def save_subreddit(self, subreddit, status="good"):
        sql = "insert or replace into subreddits(name, subscribers, date, created, status) values(?, ?, ?, ?, ?)"
        self.cnxn.execute(sql, (subreddit['name'], subreddit['subscribers'], datetime.now(), subreddit['created'], status))
        self.cnxn.commit()

    def update_status(self, name, status):
        sql = "update subreddits set status=? where name=?"
        self.cursor.execute(sql, (status, name))
        self.cnxn.comit()

    def get_subreddits(self):
        sql = "select name, subscribers, created, status from subreddits"
        return list(self.cnxn.execute(sql))

    def get_subreddit(self, name):
        sql = "select name, subscribers, created, status from subreddits where name=?"
        return self.cnxn.execute(sql, (name, )).fetchone()

    def get_all_links(self):
        sql = "select * from mapping"
        return list(self.cnxn.execute(sql))

    def get_links_from(self, source):
        sql = "select * from mapping where source=?"
        return list(self.cnxn.execute(sql, (source, )))

    def close(self):
        self.cnxn.close()

    def createnew(self):
        self.cnxn.execute("""create table mapping (
            source varchar(255),
            target varchar(255),
            primary key(source, target)
            )""")

        self.cnxn.execute("""create table subreddits (
            name varchar(255),
            subscribers int,
            date datetime,
            created int,
            status text,
            primary key (name)
            )""")

        self.cnxn.execute("""create table comments (
            username text,
            subreddit text,
            primary key(username, subreddit)
            )""")

        self.cnxn.execute("""create table comments_mapping (
            vertex0 text,
            vertex1 text
            )""")


        self.cnxn.commit()
