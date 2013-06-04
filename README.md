reddit-communities
==============

This is my humble try at crawling and graphic reddit, with the purpose
of analysing it as a social network.

How?
--------------

Subreddits commonly link to other subreddits in their "sidebar". This is available with the Reddit API. I then interpret each subreddit as a vertex in the graph and the links as edges. 

Novel findings
---------------

So far I have crawled about 17,000 subreddits (vertices) and just above 100,000 links (edges) between them. There are much more according to metareddit. 

I have found that some communities are topologically disconnected from the rest of reddit. But since we have a directed graph, they are not nessecarily topologically disconnected from reddit. A prime exaple of this are the communities formed around /r/clojure/. 

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

In case you are wondering, the Top 100 list shows the same behavoir. Wtf, Reddit?

Author
-----------------
Benedikt Kristinsson 
benedikt.k@gmail.com