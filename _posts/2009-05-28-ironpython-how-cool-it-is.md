---
date: 2009-05-28T05:08:00+00:00
author: Ryan Svihla
layout: post
tags: [python, csharp]
---
<h1>IronPython how cool it is</h1>
*EDIT: this is an old post copied over from my [old blog on Los Techies](https://lostechies.com/ryansvihla/2009/05/28/ironpython-how-cool-it-is/), I have kept it here for archival reasons.*

Briefly, [IronPython](http://www.codeplex.com/IronPython) is an implementation of Python in the .Net runtime. This allows you access to .Net framework goodness while programming in a dynamic language. The current stable version 2.0.1 maps to CPython 2.5.This allows me to do fun fun things like use my python project to access a c# project. follows is a python script using Pinsor and accessing a .net dll.

C# code:

```csharp

public class Command
{

	private readonly DoingStuff _stuff;

	public Command (DoingStuff stuff)
	{
		 _stuff = stuff;
        }

	public void Execute()
	{
		Console.WriteLine(_stuff.Message);
        }
}

public class DoingStuff
{
        public string Message
        {
		get { return "From the Doing Stuff Class, I'm doing stuff"; }
	}
}
```

python code:

```python
from pinsor import *
import clr
clr.AddReference('csharpdemo')
from csharpdemo import *


kernel = PinsorContainer()
kernel.register( Component.oftype(DoingStuff),Component.oftype(Command).depends([DoingStuff])  )

cmd = kernel.resolve(Command)
cmd.Execute()
```

ouput is like:

```shell
C:\ipyexmaple>c:\Program Files\IronPython 2.0.1\ipy.exe ipydemo.py
From the Doing Stuff Class, I'm doing stuff
```

I'm sure this causes a "what the heck" so let me summarize:

  1. created c# dll
  2. placed a python script next to it named ipydemo.py
  3. in that script I imported the c# dll
  4. then I called my custom python IoC container Pinsor which is written in pure python
  5. added .Net objects to my python IoC container
  6. resolved a .Net object from my python IoC container
  7. then executed it with the expected results and dependencies.

When I did this test I stared at the screen completely stunned for a bit.Pinsor was very easy to implement, and it has some decent abilities considering its short life and my limited time.

I doubt I could make the same thing in C# in twice as much time, and I'm more experienced in C#.
This opens up some worlds for me.

With all this in mind has anyone had a chance to play with ironpython support in VS 2010?

Finally, I would like to thank [Micheal Foord](http://www.voidspace.org.uk/cv.shtml with his blog and book [IronPython In Action](http://www.manning.com/foord/). I highly recommend reading both if you are interested in quality programming, but especially if any of this intrigues you.
