---
layout: post
---
<h1>Trying to Get Away From Jekyll</h1>

<p>
This morning I tried to switch to pure HTML from Jekyll on GitHub pages and it was not trivial, I finally punted and gave up but I wanted
to share the brick wall I ran into so I can try again later.
</p>
<h2>why?</h2>

<h3>Access</h3>

<p>
Simple, I am trying to use my computer less. When I have a thought I would like to share
and say I have my phone on me, I would just like to rip out a blog post, without setting
up git, getting a decent text editor, etc it's just too much work to do well.
</p>
<h3>Security</h3>

<p>
My Jekyll version was apparently out of date and needed a security fix.
Dependabot deemed it too hard to fix itself so I had to get the computer out to upgrade it.
I realized this is not what I want to be doing. This is too much work for glorified HTML that would
never have this problem.
</p>
<h3>what did I try?</h3>

<p>I wrote a simple python script that attempted to convert the markdown to HTML.
This also took a few attempts and I saved off the home page with all the links I figured I don't blog 
enough to warrant dynamic post linking from the home page.
However the result was unusable
</p>

<h3>why did it fail?</h3>
<p>
The code marked down with back tics did not parse correctly and
All of the posts with code (most of them) were a disaster. As
a result I converted stripped out my theme and configuration
to get at least auto updating Jekyll versions and I'm 
keeping the home page as is, i.e. mostly static. During the conversion I also found 
several blogs with a bad title that Jekyll was burying as a result.
</p>

<h3>Next steps</h3>

<p>I will be slowly converting all of this to pure HTML and will remove 
the posts directory once that's complete.I 
also need a better text editor or GitHub app
that will let me edit blog posts, doing this in 
the browser while accessible is not fun.
</p>

<p>I'm sure someone will say use WordPress, Medium or whatever but I've used several 
blog platforms and a lot of my worst formatted posts are bad conversions from those.
Either that platform started charging, or changed their own versions that broke my formatting.
If years ago I had written this all in HTML and accepted a simple layout,
I would still have posts formatted as they were a decade ago (granted in those days
browser rendering changed frequently, but this is no longer the case and the web is
relatively well-versioned).
</p>
