## Ugh.
from datetime import datetime

def singleton(class_):
    _instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in _instances:
            print "New instnace"
            _instances[class_] = class_(*args, **kwargs)
        return _instances[class_]
    return getinstance
        
@singleton
class DBModel(object):
    def __init__(self, connection):
        self.cnxn = connection
        self.cursor = connection.cursor()
        
    def commit(self):
        self.cnxn.commit()
        
    def add_mapping(self, source, target):
        self.cursor.execute("insert into mapping values(?, ?)", (source, target))

    def add_subreddit(self, name, subscribers, created, status="good"):
        sql = "insert into subreddit(name, subscribers, date, created, status)"
        self.cursor.execute(sql, (name,
                                  subscribers,
                                  datetime.now(),
                                  created,
                                  status))
        
    def update_subreddit(self, name, subscribers, created, status="good"):
        sql = """update subreddits
        set subscribers=?, date=?, created=?, status=?
        where name=?"""
        self.cursor.execute(sql, (subscribers,
                                  datetime.now(),
                                  created,
                                  status,
                                  name))
        
    def update_status(self, name, status):
        sql = "update subreddits set status=? where name=?"
        self.cursor.execute(sql, (status, name))

    def get_subreddits(self):
        sql = "select name from subreddits"
        return set([a[0] for a in self.cursor.execute(sql)])
