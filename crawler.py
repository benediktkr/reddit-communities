# -*- coding: utf-8 -*-

import sys
import json
import requests
import re
import sqlite3
from datetime import datetime
from collections import deque
import dbmodel

headers = {'user-agent': '/u/benediktkr crawling reddit to graph communities'}
client = requests.session()

def fix(s):
    if s[0:2] == "r/":
        s = "/" + s
    if s[-1] != "/":
        s = s + "/"
    return s.lower()

def parse_sidebar(subreddit):
    url = 'http://www.reddit.com/{0}/about.json'.format(subreddit[1:-1])
    r = client.get(url, headers=headers)
    j = r.json()
    if j == None or "error" in j:
        return {'name': subreddit,
                'links': [],
                'subscribers': 0,
                'created': None,
                'error': "dunno" if j == None else j['error']}
            
    if j['data']['description']:
        regex = re.findall(r'/r/\w+/?', j['data']['description'])
        links = list(set([fix(a) for a in regex if fix(a) != subreddit]))
    else:
        links = []
    subscribers = int(j['data']['subscribers'])
    created = int(j['data']['created'])

    return {'name': subreddit,
            'links': links,
            'subscribers': subscribers,
            'created': created}

def bfs(start_node):
    todo = deque()
    visited = set()
    todo.append(start)
    while len(todo) > 0:
        here = todo.popleft()
        if here in visited:
            continue
        visited.add(here)
        sidebar = parse_sidebar(here)
        # Handle stuff about this node. 
        for subreddit in sidebar['links']:
            if subreddit not in visisted:
                todo.append(subreddit)
            link = (here, subreddit)
            handle(here, subreddit)
            
def dfs():
    found = set()
    old_recursionlimit = sys.get_recursionlimit()
    sys.setrecursionlimit(10*old_recursionlimit)
    def dfs_search(node, lvl=0):
        if node not in found:
            found.add(node)
            sidebar = parse_sidebar(node)['links']
            for r in sidebar:
                handle(node, r)
                dfs_search(r, lvl+1)
    return dfs_search

