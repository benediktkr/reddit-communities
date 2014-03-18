#coding: utf-8

import sys
import json
import requests
import re
import sqlite3
from datetime import datetime
from collections import defaultdict, deque

"""OBSOLETE AND NOT USED.

Has some weird DFS implementations. The code is mainly the same as crawler.py,
I think I cretated crawler.py instead of cleaning this file up. """

# pip install pysqlite

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
    url = 'http://www.reddit.com/%s/about.json' % subreddit[1:-1]
    r = client.get(url,  headers=h)
    
    try:
        j = json.loads(r.text)
    except ValueError:
        print subreddit, "not found"
        return {'links': [],
                'subscribers': 0
                }
    if "error" in j or j['data']['description'] == None:
        print subreddit, "not found"
        return {'links': [],
                'subscribers': 0
                }


    regex = re.findall(r'/r/\w+/?', j['data']['description']) #
    subscribers = int(j['data']['subscribers'])
    subreddits = list(set([fix(a) for a in regex]))

    return {
        'links': [s for s in subreddits if s != subreddit],
        'subscribers': subscribers
    }
            
def fix(s):
    if s[0:2] == "r/":
        s = "/" + s
    if s[-1] != "/":
        s = s + "/"
    return s.lower()
    
def recur_dfs(node, lvl=0):
    if node not in found:
        found.add(node)
        l = linked_subreddits(node)['links']
        #print str(lvl).ljust(7), node
    
        for r in l:
            print node, "->", r
            recur_dfs(r, lvl+1)

#known_nodes = defaultdict(str)
#f = open('reddit-dfs-2.txt', 'a')
def recur_dfs2(node, lvl=0):
    if known_nodes[node] == "VISITED":
        return ""
    if known_nodes[node] == "DISCOVERED":
        l = linked_subreddits(node)['links']
        for r in l:
            if known_nodes[r] == "DISCOVERED":
                pass
            else:
                recur_bfs(r, lvl+1)
    if known_nodes[node] == "":
        l = linked_subreddits(node)['links']
        for target in l:
            link = "{0} -> {1}".format(node, target)
            f.write(link + "\n")
            f.flush()
            print str(lvl).ljust(7), link
        known_nodes[node] = "DISCOVERED"
        for r in l:
            recur_bfs(node, lvl+1)
        known_nodes[node] == "VISITED"
    
def bfs(start):
    f = open('bfs.txt', 'a')
    cnxn = sqlite3.connect('data/reddit.db')
    cursor = cnxn.cursor()
    subrsql = "insert into subreddits values(?, ?, ?)"
    todo = deque()
    visited = set()
    todo.append(start)
    while len(todo) > 0:
        node = todo.popleft()
        if node in visited:
            continue  
        visited.add(node)
        l =  linked_subreddits(node)
        cursor.execute(subrsql, (node, l['subscribers'], datetime.now()))

        for child in l['links']:
            edge = (node, child)
            if child not in visited:
                todo.append(child)
        
            link = "{0} -> {1}".format(node, child)
            cursor.execute("insert into mapping values(?, ?)", edge)
            f.write(link)
            print datetime.now().replace(microsecond=0), link

        f.flush()
        cnxn.commit()
    f.close()
    cnxn.close()

    

if __name__ == "__main__":
    sys.setrecursionlimit(10*sys.getrecursionlimit())
    try:
        if len(sys.argv) == 2 or "--bfs" in sys.argv:
            bfs(fix(sys.argv[1]))
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
