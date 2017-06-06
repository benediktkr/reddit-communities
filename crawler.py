# -*- coding: utf-8 -*-

import sys
import re
from collections import deque
import argparse

from requests import get

from dbmodel import DBModel

"""Crawl reddit from a starting point, look at the sidebar and spider
to the links there."""

headers = {'user-agent': '/u/benediktkr https://github.com/benediktkr/reddit-communities'}

def fix(s):
    if s[0:2] == "r/":
        s = "/" + s
    if s[-1] != "/":
        s = s + "/"
    return s.lower()

def parse_sidebar(subreddit):
    subreddit = fix(subreddit)
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

def bfs(root, fname, max_depth):
    current_depth = 0
    if not fname:
        fname = fix(root)[3:-1] + ".txt"
    f = open(fname, 'w')
    #db = DBModel.get()
    todo = deque()
    visited = set()
    todo.append(root)
    todo.append(None)
    while len(todo) > 0:
        here = todo.popleft()
        if here is None:
            if max_depth and current_depth >= max_depth:
                print "Exiting at dept", current_depth
                break
            current_depth += 1
            todo.append(None)
            print current_depth
            continue
        if here in visited:
            continue
        visited.add(here)
        this_subreddit = parse_sidebar(here)
        #db.save_subreddit(this_subreddit)
        for subreddit in this_subreddit['links']:
            if subreddit not in visited:
                todo.append(subreddit)
            link = (here, subreddit)
            slink = "{} -> {}".format(here, subreddit)
            f.write(slink + "\n")
            print slink
            # print link
            #db.save_link(link)

    # db.close()
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="reddit-communities")
    parser.add_argument('root', metavar='root', type=str, help="Subreddit to use as root for crawler")
    parser.add_argument('--depth', type=int, default=None, dest="max_depth", help="Depth for BFS search")
    parser.add_argument('--fname', type=str, default=None, dest="fname", help="Filename to write CSV to")

    args = parser.parse_args()

    import pprint
    pprint.pprint(parse_sidebar(args.root))

    bfs(**vars(args))
