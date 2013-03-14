import sqlite3

conn = sqlite3.connect('reddit.db')
cursor = conn.cursor()
cursor.execute("""create table mapping (
  source varchar(255),
  target varchar(255),
  primary key(source, target)
  )""")

cursor.execute("""
  create table subreddits (
   name varchar(255),
   subscribers int,
   date datetime,
   primary key (name)
  );""")
conn.commit()
conn.close()
