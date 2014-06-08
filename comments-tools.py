import dbmodel
from collections import defaultdict
from itertools import combinations

def convert():
    """Convert the data in the table "comments" to links
    between subreddits and save in "comments_mapping", the
    same format as the "mapping" table. The result is an
    undirected graph"""
    
    model = dbmodel.DBModel.get()
    mapping = defaultdict(list)
    print "preprocessing"
    for comment in model.get_comments_generator():
        mapping[comment[0]].append(comment[1])
    print "creating subreddit pairs (links)"
    links = []
    for username in mapping:
        pairs = combinations(mapping[username], 2)
        # extend seems to be the way to go
        #https://stackoverflow.com/questions/17044508
        links.extend(pairs)
    print "found {0} pairs".format(len(links))
    print "saving to database"
    for pair in links:
        model.save_comment_link(pair)
    model.commit()
    model.close()
            

def check(s0, s1):
    model = dbmodel.DBModel.get()
    first = set(model.get_comment_links(s0))
    second = set(model.get_comment_links(s1))
    return len(first.intersection(second)) > 0
    
        
if __name__ == "__main__":
    import sys
    if sys.argv[1] == "--convert":
        print convert()
    elif sys.argv[1] == "--check":
        subr0, subr1 = sys.argv[2], sys.argv[3]
        print check(subr0, subr1)
