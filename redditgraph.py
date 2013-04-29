#-*- coding: utf-8 -*-
import sqlite3
import igraph
import pickle
import os
from datetime import datetime

# Helpers
first = lambda l: l[0]

def graph():
    conn = sqlite3.connect('data/reddit.db')
    cursor = conn.cursor()
    # Mögulega hafa list en ekki set, treysta á uniqueness. 
    V = set(first(a) for a in cursor.execute("select name from subreddits"))
    E = set((a, b) for a, b in cursor.execute("select * from mapping")
            if (a in V) and (b in V))

    graph = igraph.Graph(directed=True)
    graph.add_vertices(list(V))
    graph.add_edges(list(E))
    return graph

def layout(algorithm):
    g = graph()
    if not os.path.exists("{0}.pickle".format(algorithm)):
        print "Pickling to file"
        glayout = g.layout(algorithm)
        with open("{0}.pickle".format(algorithm), "wb") as f:
            pickle.dump(glayout, f, pickle.HIGHEST_PROTOCOL)
    else:
        print "I had a jar of pickles for this one"
        with open("{0}.pickle".format(algorithm), "rb") as f:
            glayout = pickle.load(f)
    return glayout

def main():
    algorithms = ["auto",
                  "lgl",  # Large graph
                  "fr",          # Fruchterman-Reingold
                  "gfr",         # Grid-based Fruchterman-Reingold 
                  "graphopt",    # graphopt algorithm
                  "kk",          # Kamada-Kawai
                  "rt",          # Reingold-Tilford tree layout
                  "sugiyama",    # Sugiyama layout
                  "rt_circular", # circular Reingold-Tilford tree layout
                  "circle",
                  "grid",        # Regular 2D grid
                  "kk_3d",       # 3D Kamada-Kawai
                  "fr_3d",       # 3D Fruchterman- Reingold layout
                  "drl",
                  "drl_3d"]

    g = graph()
    for a in algorithms:
        print datetime.now(), "-",
        print a, "start"
        l = layout(a)
        #igraph.plot(g, layout=l, vertex_size=2).save("{0}.png".format(a))
    

if __name__ == "__main__":
    main()
