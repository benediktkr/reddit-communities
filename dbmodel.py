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
        
    def save_link(self, link):
        self.cnxn.execute("insert or replace into mapping values(?, ?)", link)
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
        sql = "select name from subreddits"
        return set([a[0] for a in self.cursor.execute(sql)])

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
        self.cnxn.commit()

