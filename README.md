reddit-communities
==============

Crawling and graphig reddit, with the purpose of analysing it as a social network.

![Yifan-Hu](/data/yifan-hu-4.png)

How?
--------------

Subreddits commonly link to other subreddits in their "sidebar". This is available with the Reddit API. We then interpret each subreddit as a vertex in the graph and the links between subreddits as edges. 

I first wrote a crawler that saves the info in a sqlite database. Then it's easy to convert that data into whatever analytic tools I want to use. 

Usage 
-------------

Sidebar data 
====

1. Use `crawler.py` to crawl from a given start and build the sqlite database in `data/reddit.db`

        $ python crawler.py /r/Iceland/

2. Use `graphtool_analyze.py` to create `data/reddit.gml` to open with gephi. I've also used igraph. The file `igraph_analyze` programmatically calculates some statistics (mean geodesic distance and the top list based on vertex-degree). 

Comments data
======

1. To crawl comments, run `comments.py` and leave it running. 

        $ python comments.py

2. Convert this data to the same format as from `crawler.py` with `comments-tools.py`. 

        $ python comments-tools.py --convert

  The data then gets stored in the table `comments_mapping` as an undirected graph. This otherwise mirrors the format of the data in `mapping` and now `graphtool_analyze.py` (i need to get better at naming things) should work on this dataset as well.

3. You can use `comments-tools.py` to check if a link exists between subreddits:

        $ python comments-tools.py --check /r/askreddit/ /r/programming/
        True



Methodology
-----

I realized that there are two sources of data that connect subreddits together. 

1. The links in the sidebar
2. If a user comments in two or more subreddits, these subreddits are connected by the user. This might reveal intersting data about what people are interested in. 

Ideas and improvements
-----

At first i decided to ignore edge weight, but I have realized this might be useful data. My idea is to change the comments method to use the number of users that have commmented in the same pairs of subreddits as weight. 

Novel findings
---------------

So far I have crawled about 24,000 subreddits (vertices) and just above 160,000 links (edges) between them. There are much more according to metareddit. 

The starting point has been `/r/Iceland/`, with no special reason except I've frequented it the longest. 

I have found that some communities are topologically disconnected from the rest of reddit. But since this is a directed graph, they are not nessecarily topologically disconnected from reddit. A prime exaple of this are the communities formed around /r/clojure/. 

If we order subreddits with respect to their in-degree (number of subreddits linking to them) and without regard of the number of subscribers, we reveal one interesting statistic abour reddit. 

This is the top 10:

     $ python graph.py
     0. /r/music/
     1. /r/kateupton/
     2. /r/emmawatson/
     3. /r/starlets/
     4. /r/mileycyrus/
     5. /r/jenniferlawrence/
     6. /r/vanessahudgens/
     7. /r/emmastone/
     8. /r/emiliaclarke/
     9. /r/arianagrande/

In case you are wondering, the Top 100 list shows the same behavoir. wtf, Reddit?

Notes
========

Layout algorithms not used (igraph)
------
 For layouts actually used, see the code.

 - The Sugiyama layout algorithm repeatedly segfaulted.
   "sugiyama":    Sugiyama layout. Segmentation fault.

 - Reingold-Tilford tree layouts. Reddit is not a tree
   "rt":          Reingold-Tilford tree layout
   "rt_circular": circular Reingold-Tilford tree layout
   
 - Various 3D layouts
   "kk_3d":   3D Kamada-Kawai
   "fr_3d":   3D Fruchterman- Reingold layout
   "drl_3d"

Author
==========

Benedikt Kristinsson 

benedikt@inventati.org

