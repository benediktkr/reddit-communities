import sqlite3, igraph
conn = sqlite3.connect('data/reddit.db')
cursor = conn.cursor()
g = igraph.Graph()
g.add_vertices([a[0] for a in cursor.execute("select name from subreddits").fetchall()])
g.add_edges(cursor.execute("select * from mapping").fetchall())
# glayout = g.layout("fr")

