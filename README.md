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

1. Use `crawler.py` to crawl from a given start and build the sqlite database in `data/reddit.db`

        $ python crawler.py /r/Iceland/

2. Use `graphtool_analyze.py` to create `data/reddit.gml` to open with gephi. I've also used igraph. The file `igraph_analyze` programmatically calculates some statistics (mean geodesic distance and the top list based on vertex-degree). 

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

