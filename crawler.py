# -*- coding: utf-8 -*-

import sys
import json
import re
from datetime import datetime
from collections import deque

from requests import get
import sqlite3

from dbmodel import DBModel

"""Crawl reddit from a starting point, look at the sidebar and spider
to the links there."""

headers = {'user-agent': '/u/benediktkr crawling reddit to graph communities'}

def fix(s):
    if s[0:2] == "r/":
        s = "/" + s
    if s[-1] != "/":
        s = s + "/"
    return s.lower()

def parse_sidebar(subreddit):
    url = 'http://www.reddit.com/{0}/about.json'.format(subreddit[1:-1])
    try:
        json = get(url, headers=headers).json()
        error = False
    except ValueError as ve:
        print subreddit + ": " + str(ve)
        f = open('errors.txt', 'a')
        f.write(get(url).text.encode("utf-8"))
        f.close()
        error = True

    if error or "error" in json:
        return {'name': subreddit,
                'links': [],
                'subscribers': 0,
                'created': None,
                'error': "dunno" if error else json['error']}
            
    if json['data']['description']:
        regex = re.findall(r'/r/\w+/?', json['data']['description'])
        links = list(set([fix(a) for a in regex if fix(a) != subreddit]))
    else:
        links = []
    subscribers = int(json['data']['subscribers'])
    created = int(json['data']['created'])

    return {'name': subreddit,
            'links': links,
            'subscribers': subscribers,
            'created': created}

def bfs(start_node):
    f = open('data/reddit.txt', 'w')
    db = DBModel.get()
    todo = deque()
    visited = set()
    todo.append(start)
    while len(todo) > 0:
        here = todo.popleft()
        if here in visited:
            continue
        visited.add(here)
        this_subreddit = parse_sidebar(here)
        db.save_subreddit(this_subreddit)
        # Handle stuff about this node. 
        for subreddit in this_subreddit['links']:
            if subreddit not in visited:
                todo.append(subreddit)
            link = (here, subreddit)
            print link
            db.save_link(link)
    db.close()
    f.close()
            
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

if __name__ == "__main__":
    try:
        start = fix(sys.argv[1])
    except IndexError:
        start = "/r/iceland/"
    bfs(start)
