#-*- coding: utf-8 -*-
import sqlite3
import igraph
import pickle
import os
from datetime import datetime


"""This file creates igraph layouts and pickes them to file. 
"""

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
    filename = "data/pickejar/{0}.pickle".format(algorithm)
    if not os.path.exists(filename):
        print "Pickling to file"
        glayout = g.layout(algorithm)
        with open(filename, "wb") as f:
            pickle.dump(glayout, f, pickle.HIGHEST_PROTOCOL)
    else:
        print "I had a jar of pickles for this one"
        with open(filename, "rb") as f:
            glayout = pickle.load(f)
    return glayout

def create_layouts():
    algorithms = ["auto",
                  "lgl",  # Large graph
                  "fr",          # Fruchterman-Reingold
                  "gfr",         # Grid-based Fruchterman-Reingold 
                  "graphopt",    # graphopt algorithm
                  "kk",          # Kamada-Kawai
                  "circle",
                  "grid",        # Regular 2D grid
                  "drl"]
                 
    g = graph()
    for a in algorithms:
        print datetime.now(), "-",
        print "algorithm:", a
        l = layout(a)
        #igraph.plot(g, layout=l, vertex_size=2).save("{0}.png".format(a))

def main():
    create_layouts()

if __name__ == "__main__":
    main()
