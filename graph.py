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


if __name__ == "__main__":
    conn = sqlite3.connect('data/reddit.db')
    cursor = conn.cursor()
    vertices = set([a[0] for a in cursor.execute("select name from subreddits where subscribers >= 100000;")])
    edges = set([(a, b) for a, b in cursor.execute("select * from mapping") if (a in vertices) and (b in vertices)])
    
    
    g = igraph.Graph(directed=True)
    g.add_vertices(list(vertices))
    g.add_edges(list(edges))
#glayout = g.layout("fr")

# Top 10
#  >>> sorted([(i['name'], g.degree(i, type="in")) for i in g.vs], key=lambda a: a[1], reverse=True)[0:10]
