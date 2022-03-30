---
layout: post
tags: [astra, go]
---
<h1>Why I Don't Cobra</h1>

So I just implemented this [DataStax Astra CLI](https://github.com/rsds143/astra-cli) interface and it has gotten some attention where I work. One of the developers
who had worked on a similar tool had suggested I use cobra to build a command line interface.

## Code size

I explained to him that I actually had a lot of experience with [Cobra](https://github.com/spf13/cobra) and that I thought it was an
excellent library with lots of great support for nested commands, it also [had lots of transitive dependencies](https://github.com/spf13/cobra/blob/master/go.sum) (313 lines in the go.sum at the time of this post), 
and I've discovered that it actually can bloat the size of the executable quite a bit. Therefore I had elected to 
use the standard library to build my command line flags. Admittedly, I've had to do a lot more work to actually build
my commandline interface, I did kept the executable size to under 4 mb for all platforms.

## Maintenance

With things like typo squatting, abandoned projects and various degrees of coding quality more and more I have felt that grabbing a third-party package for every
single thing you need was just delayed cost due to  more work downe the line. 
Time saved at first is often later lost in maintanence with API changes you didn't want, which are often due to features you do not need. 
Worse still, the extra maintenance when talking about open source projects, this extra maintenance can make it more likely that you will abandon
your project, thereby perpetuating the problem even further, since maybe, other people have come to depend on your library.

Back when I wrote software in the Rails framework or the few projects I've done in Spring Boot I found it very easy to have 200+ dependencies
with most not really adding too many features that I actually used or if I am using them, I am using only using a few functions.

Likewise I've often had to upgrade a library for a security problem that may not actually be affecting any code path I use,
but it does show up on the security scan which does cause a red flag for anybody else checking on it. 

Furthermore, do I really want to examine every single source file in every single dependency to see if I am affected or not?

This puts a lot of cognitive load on the developer sometimes a lot more than it would just implement a simple function themselves.

## The Fix

So I have resolved to never reach for a third-party dependency unless I absolutely need it, and when I do reach for the third-party dependency
that it has a few dependencies as possible. 

If it's something that simple that I can do relevant in myself and I can write test I will go ahead and write it for that project.
If I do it often enough I will go ahead and make a third-party library, but I will strive with that third-party library to not actually depend
on any other projects, so that anyone else depending on that library will only get the one dependency.




So I'm hoping with this change to not help contribute further to the problem of too many dependencies for things that are too trivial and hopefully myself will become a little bit better developer in the process.
