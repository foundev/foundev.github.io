
# Why Free Software Still Matters to Me

When I was younger I had very little money, this was one part bad decision and one part background that I had to overcome. I got my first computer as an adult on a loan from an aunt who had saved all her money and wanted to make sure her nephew could go back to university (I never finished sorry auntie, but I think I did plenty well due to that loan, it all worked out extremely well.)

Early on I ran Windows like everyone else but wanted to get into IT and after that programming. Eventually, I figured out I was able to run everything I wanted for free (legally no less) and installation was one apt-get install or one YaST install away (the package installer for SuSE Linux), ok often is was ./configure; make; make install. But the docs were free, often the online guides were better than one would find in any book at the store.

I was only limited by my imagination, my ability to read arcane things and the patience that required. I grew in leaps and bounds and eventually as my confidence grew I was able to do more and more things and people started asking me to do “computer work” for money.

I ran Linux, FreeBSD and OpenBSD for various tasks in home and at work. But eventually I headed the demand for Windows and spun up on that stack. At this point, I just wanted to stop being poor and in 2003 in the Midwest being a Unix expert did not really pay the bills. I was sad to be leaving behind free software for all the things, but I had to be pragmatic for a bit, thankfully my wishes and the market finally collided.

## Popularity of Free Software 

Eventually, several startups got very very big and they ran nearly all free software , except of course the main thing that made them money, but this was by all measures an improvement over the world we had with Microsoft and Oracle.

But there had been a bug change in the licenses used. Richard Stallman and the GNU software that I had so admired seemed quaint, the world had begun to prefer the Apache License. Some would call this not free software, but some would.

More and more large companies took from
open source without giving back. Some view this as totally fine, I view it as unhelpful, but permitted. It’s part of the system we signed up for if we were using BSD or Apache software.

## Retrospective

Thinking back though if I am honest the things that made the biggest impact in my career were often not GPL so it’s hard to see how much the license matters for impact.

* Vim has had an outsized impact on my career. Not gpl
* Apache had an large but early impact on my career and later the foundation likewise had a huge impact. Not gpl
* Linux, can’t say enough and it keeps giving. GPL yes we got one!
* Kubernetes not GPL
* Cassandra not GPL
* Go not GPL
* Python not GPL


The sad truth is I don’t need the GPL apparently. I love it on paper and it fits my ideology the closest of any license. However, the reality is more money and more development go into free software that does not require sharing but encourages due to just sheer momentum. Software that everyone uses becomes very important. Companies, developers, etc want the cachet of being a major contributor to something that everyone depends on and hence to be the first ones called when something does not work as expected. This is the big advantage I think of the weak copy left license.

### The case of OpenSSL 

But what do you do with hugely important things like OpenSSL that get no funding or help [until it had a massive security incident](https://www.pcworld.com/article/438906/after-heartbleed-tech-giants-commit-to-supporting-critical-open-source-projects.html)

This being the huge downside of Apache 2 style licenses. The freeloader problem becomes even larger if the economic incentives aren’t there and OpenSSL is boring even if it is hugely important, so no one was pouring billions into it.

## Conclusion

I don’t know what to do. GPLv2 used to seem like the right balance and the non-copyleft or weak-copyleft licenses have taken off. I guess as long as the incentives remain to share changes, and those licenses make it easier to start a business, then this all still works. But it also [leads](https://github.com/rapi3/pfsense-is-closed-source) to [silly](https://visualstudiomagazine.com/articles/2022/06/16/csharp-vs-code-tool.aspx?m=1) [things](https://www.datastax.com/resources/video/thread-core-jake-luciani), that end up working badly for all involved.

TLDR share your code, there is a poor kid somewhere with a lot of talent that needs to be enabled, and you may want to hire them someday. Heck they just may write some software you need.