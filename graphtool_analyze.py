from graph_tool.all import *

from dbmodel import DBModel

def main():
    g = Graph()
    g.set_directed(False)
    
    db = DBModel.get()
    g.vertex_properties["subscribers"] = g.new_vertex_property("int")
    g.vertex_properties["name"] = g.new_vertex_property("string")
    vertices = dict()

    # add all vertices to the graph
    for subreddit in db.get_subreddits():
        v = g.add_vertex()
        g.vertex_properties["name"][v] = subreddit[0]
        g.vertex_properties["subscribers"][v] = subreddit[1]
        vertices[subreddit[0]] = v

    # add all the edges
    for link in db.get_all_links():
        v1, v2 = link
        source = vertices[v1]
        target = vertices[v2]
        g.add_edge(source, target)

    db.close()
    g.save("data/reddit.gml")
        

if __name__ == "__main__":
    main()
