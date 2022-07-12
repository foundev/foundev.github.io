---
layout: post
tags: []
categories: []
#date: 2019-06-25 13:14:15
#excerpt: ''
#image: 'BASEURL/assets/blog/img/.png'
#description:
#permalink:
title: 'Coding in Lieu of Scripting'
---

<h1>Coding in Lieu of Scripting</h1>

<p>
Since I "mostly" moved to support about 8 years ago now I have parsed a LOT of logs, and I enjoy it.
  I like to search for unknown problems before they become known at 3am, or figure out what happened exactly at
a given point in time, especially when no one else seems to know. The discovery is fun and I get to tell a
  story with the data. At first I used the shell at lot and I rediscovered lost skills from my early days
  in ISP land. However, I found it very difficult to share that knowledge. Scripts were never quite portable
  enough, and the Windows users would just stare at me in bewilderment when I handed them a bash script 
  Note this is before WSL was really a thing, and while I enjoy powershell support is unix centric.
</p>

<p>
  I tried a few different strategies to knowledge share: central script repos, documents teaching all the 
  commands I used (complete with copy pastable examples use cases) and none of it really took off. Worse,
  as my scripts needed to get more advanced they got harder to grasp, I mean for myself let alone for
  others. So I began to write a lot of Go and Python code instead. Go was easy to teach,
  Python even easier and a lot of people knew it, and for things where performance or deployment
  ease wasn't the primary driver Python worked out super well for knowledge sharing.
</p>

<p>
  The best example of this was [sperf](https://github.com/datastax-labs/sperf) which had a lot more than the 
  93 commits listed as it started as a close source product. In sperf, I found my
  way to solve tickets with readable reports that found an answer to a delicate problem, and then I could 
  immediately deploy and share it with everyone, if it had any bugs or had issues, and I was too busy,
  someone else could fix it right then and there. This may not have happened exactly as often I would like,
  but I appreciated every bug fix I got as one less thing I had to do in 
  the middle of an escalation, and the unit tests gave me a log more confidence in the result. I do something
  like this everywhere I go, I take whatever code I used to solve an issue, and then put it into a central tool
  for everyone else to use, this has been hugely popular and uplifted my career in a large number of ways, plus the
  customers have really appreciated the reports.
</p> 

<p>
  For those of you less into CLI I have also done several python notebooks that were hugely useful and for a time I did
  all my reports this way, but the coworkers by and large trended towards cli/unix tools. In another organization though I would
  happily write [python notebooks like this](https://github.com/foundev/notebooks), but the principle is the same, make your problem solving reusable
  and easily shareable, and write tests.
 </p>
