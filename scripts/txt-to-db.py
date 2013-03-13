import sqlite3
import sys

conn = sqlite3.connect('reddit.db')
cursor = conn.cursor()
data = []

with open(sys.argv[1]) as f:
    for line in f.readlines():
        source, target = line.split(" -> ")
        data.append((source, target.rstrip("\n")))

print "Doing sql"
sql = "insert into mapping(target, source) values(?, ?)"
cursor.executemany(sql, data)
        
conn.commit()
conn.close()
