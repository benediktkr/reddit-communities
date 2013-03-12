import sqlite3

conn = sqlite3.connect('reddit.db')
cursor = conn.cursor()
cursor.execute("""create table mapping (
  source varchar(255),
  target varchar(255),
  primary key(source, target))""")
conn.commit()
conn.close()
