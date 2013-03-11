#coding: utf-8

import sys
import json
import requests
import re
from collections import defaultdict

h = {'user-agent': '/u/benediktkr crawling reddit to graph communities'}
client = requests.session()

#logindata = {'user': 'benediktkr',
#             'passwd': password,
#             'api_type': 'json'}
#l = client.post(r'https://www.reddit.com/api/login', data=logindata, verify=False)
#j = json.loads(l.text)
#client.modhash = j['json']['data']['modhash']

found = set()

def linked_subreddits(subreddit):
    try:
        url = 'http://www.reddit.com/%s/about.json' % subreddit[1:-1]
        r = client.get(url,  headers=h)
    except requests.exceptions.ConnectionError as ce:
        print datetime.now(), ce

    try:
        j = json.loads(r.text)
        regex = re.findall(r'/r/\w+/?', j['data']['description']) #
    except Exception as ex:
        print subreddit, "not found"
        return ""

    subreddits = list(set([fix(a) for a in regex]))
    return [s for s in subreddits if s != subreddit]
            
def fix(s):
    if s[0:2] == "r/":
        s = "/" + s
    if s[-1] != "/":
        s = s + "/"
    return s.lower()
    
def links(subr):
    subr = fix(subr)
    print subr, "-", ', '.join(linked_subreddits(subr.lower()))


def recur_dfs(node, lvl=0):
    if node not in found:
        found.add(node)
        l = linked_subreddits(node)
        #print str(lvl).ljust(7), node
    
        for r in l:
            print node, "->", r
            recur_dfs(r, lvl+1)

known_nodes = defaultdict(str)
f = open('reddit-bfs-2.txt', 'a')
def recur_bfs(node, lvl=0):
    if known_nodes[node] == "VISITED":
        return ""
    if known_nodes[node] == "DISCOVERED":
        l = linked_subreddits(node)
        for r in l:
            if known_nodes[r] == "DISCOVERED":
                pass
            else:
                recur_bfs(r, lvl+1)
    if known_nodes[node] == "":
        l = linked_subreddits(node)
        for target in l:
            link = "{0} -> {1}".format(node, target)
            f.write(link + "\n")
            f.flush()
            print str(lvl).ljust(7), link
        known_nodes[node] = "DISCOVERED"
        for r in l:
            recur_bfs(node, lvl+1)
        known_nodes[node] == "VISITED"
    
    

if __name__ == "__main__":
    sys.setrecursionlimit(10*sys.getrecursionlimit())
    try:
        if len(sys.argv) == 2 or "--bfs" in sys.argv:
            recur_bfs(fix(sys.argv[1]))
        if "--dfs" in sys.argv:
            recur_dfs(fix(sys.argv[1]))

    except KeyboardInterrupt:
        print "User exit"
        f.flush()
        f.close()
    except RuntimeError:
        print "Max recursion reached"
        f.flush()
        f.close()
