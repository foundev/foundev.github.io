---
layout: post
tags: []
categories: []
#date: 2019-06-25 13:14:15
#excerpt: ''
#image: 'BASEURL/assets/blog/img/.png'
#description:
#permalink:
title: 'fallen into rust'
---

# fallen into rust

I have just fallen into my first days of the Rust programming language. It wasn't as difficult as I feared and I wrote a high performance log reporter and analyzer. It took longer than normal to write and I did waste 2 days trying to understand how variable life times worked and this "borrow checker" thing but I managed to write a fast and seemingly major bug free prototype that is getting some heavy usage.

  
## The good 

- performance is crazy good
- cargo is very nice so far, very complete, 
- not directly owned by a single big tech company, so less prone to major disaster (in theory).

## The not so good

- very small standard library, leaving sometimes not well documented libraries as your only valid option (date time I am looking at you)
- I cannot imagine handing this off to someone else as it will be way too complicated to train a non coder or a new coder on. The borrow checker often makes sense to me, but I have more than a decade of multi threaded coding and dealing with the edges of object lifetimes. I've also read it gets much more complicated at the edges, so I may not have yet grown to hate it.
- cross-platform and cross compile support is not super easy as you need to install linkers for all the platforms you want to cross compile for. This looks bad compared to Go for example.

## overall

I like it a lot, it is all I personally want to code in now. The warts that exist will have me reach for Go when performance is not the primary concern but I look forward to this and regret I held off learning it for so long despite the efforts of good friends to tell me the good news about Rust.
