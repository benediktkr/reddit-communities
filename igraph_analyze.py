import sqlite3
import igraph

"""Work with the graph from DB."""

def reddit():
    """Return an igraph instance of Reddit from data/reddit.db"""
    conn = sqlite3.connect('data/reddit.db')
    cursor = conn.cursor()
    # TODO: Use the dbmodel. 
    vertices = set([a[0] for a in cursor.execute("select name, subscribers from subreddits")])
    edges = set([(a, b) for a, b in cursor.execute("select * from mapping") if (a in vertices) and (b in vertices)])
    
    
    g = igraph.Graph(directed=True)
    g.add_vertices(list(vertices))
    g.add_edges(list(edges))
    return g

def get_shortest_paths(graph, node, to):
    l = [[graph.vs(a)['name'] for a in path]
         for path in graph.get_all_shortest_paths(node, to=to)]
    return l

def print_shortest_paths(graph, node, to):
    for path in graph.get_all_shortest_paths(node, to=to):
        for node in path:
            print graph.vs[node]['name'], 
        print

def top(n, g):
    """Return the list of top N subreddits, by in-degree, where g is the
    graph over Reddit. In some sense, these can be viewed as the most
    popular subreddits.

    This revealed some (mildly) interesting facts about Reddit.

    The default for this function is to take all subreddits into
    consideration. If we start filtering based on number of
    subscribers, we see different results.

    """
    degrees = [(i['name'], g.degree(i, type="in")) for i in g.vs]
    top = sorted(degrees, key=lambda a: a[1], reverse=True)[0:n]
    return top

if __name__ == "__main__":
    g = reddit()
    for i, subreddit in enumerate(top(100, g)):
        print i, ":", subreddit[0]
    #glayout = g.layout("fr")

# Top 10
#  >>> sorted([(i['name'], g.degree(i, type="in")) for i in g.vs], key=lambda a: a[1], reverse=True)[0:10]
