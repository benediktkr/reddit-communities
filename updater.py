import dbmodel
import sqlite3
import crawler

def update():
    conn = sqlite3.connect("data/reddit.db")
    db = dbmodel.DBModel(conn)
    subreddits = db.get_subreddits()
    for s in subreddits:
        print s,
        l = crawler2.parse_sidebar(s)
        if "error" in l:
            print l['error'], "!!"
            db.update_status(s, l['error'])
        else:
            print l['subscribers'], l['created']
            db.update_subreddit(s, l['subscribers'], l['created'])
        
    db.commit()
    conn.close()

if __name__ == "__main__":
    update()
