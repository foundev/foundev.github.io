---
date: 2022-03-24T02:00:00+00:00
author: Ryan Svihla
layout: post
tags: [ dse, search, solr ]
---
<h1>Getting Index Size in DSE Search</h1>

Applies to DSE Search versions 3.2 to 6.8 

For some reason finding this information is dreadfully stupidly hard and I finally decided to write it down myself since I own it and someone may benefit from it some day.
There are three ways that I know of (I am sure there is a JMX way I just do not happen to know it atm)

1. via curl (and using jq but grep will suffice)  `curl "http://localhost:8983/solr/admin/cores?action=STATUS&wt=json&indent=true"  | jq '.status."mykeyspace.mytable".index.size'`
2. via ls and awk (assuming no du is available as is the case in the dse docker image) `ls -A -R -g -o "$@" /var/lib/cassandra/data/solr.data/mykeyspace.mytable/index | awk '{n1 += $3} END {print n1}' | awk '{ byte =$1 /1024/1024; print byte " MB" }'` 
3. via the solradmin and just eyeballing the per segment sizes http://localhost:8983/solr/#/mykeyspace.mytable/segments


I have had a deep dive to find this so many times I wish I had just posted this years ago
