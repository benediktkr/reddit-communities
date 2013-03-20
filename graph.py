import sqlite3, igraph

def get_shortest_paths(graph, node, to):
    l = [[graph.vs(a)['name'] for a in path]
         for path in graph.get_all_shortest_paths(node, to=to)]
    return l

def print_shortest_paths(graph, node, to):
    for path in graph.get_all_shortest_paths(node, to=to):
        for node in path:
            print graph.vs[node]['name'], 
        print

conn = sqlite3.connect('data/reddit.db')
cursor = conn.cursor()
g = igraph.Graph(directed=True)
g.add_vertices([a[0] for a in cursor.execute("select name from subreddits").fetchall()])
g.add_edges(cursor.execute("select * from mapping").fetchall())
#glayout = g.layout("fr")

