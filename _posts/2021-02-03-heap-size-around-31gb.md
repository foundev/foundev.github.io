---
layout: post
title: Heap Size Around 32 GB 
tags: [java, cassandra, gc]
---
note: originally written Feb 3 2021

There was a question this morning around a pretty common discussion point around 31 gb versus 32 gb of heap. This [article discusses this in more detail](http://java-performance.info/over-32g-heap-java/), the key point follows:

> Be careful when you increase your application heap size over 32G (from under 32G to over 32G) – JVM switches to 64 bit object references at that moment, which means that your application may end up with less available heap space. A rule of thumb is to jump from 32G right to 37-38G and continue adding memory from that point. The actual area of “grey” territory depends on your application – the bigger an average Java object in your application, the smaller is the overhead.

When this sort of commentary first came out with the CMS garbage collector a lot of us took it as gospel and rarely saw downsides however with the G1GC the conversation around this is more nuanced, [as we must take into account region size on performance](https://plumbr.io/handbook/gc-tuning-in-practice/other-examples/humongous-allocations) key point here:

>  Whenever your application is using the G1 garbage collection algorithm, a phenomenon called humongous allocations can impact your application performance in regards of GC. To recap, humongous allocations are allocations that are larger than 50% of the region size in G1.

[Ok what is region size](https://www.oracle.com/technical-resources/articles/java/g1gc.html)? 

> The G1 GC is a regionalized and generational garbage collector, which means that the Java object heap (heap) is divided into a number of equally sized regions. Upon startup, the Java Virtual Machine (JVM) sets the region size. The region sizes can vary from 1 MB to 32 MB depending on the heap size. The goal is to have no more than 2048 regions. The eden, survivor, and old generations are logical sets of these regions and are not contiguous.

Ok so, region size is this thing we have to worry about [but what are the calculated sizes](https://stackoverflow.com/questions/46786601/how-to-know-region-size-used-of-g1-garbage-collector)? 


```
Region size for each heap size

<4GB -  1MB
<8GB -  2MB
<16GB -  4MB
<32GB -  8MB
<64GB - 16MB
64GB+ - 32MB
```

You'll note in the above table the region size goes from 8mb to 4mb when going from 32GB max heap down to 31GB. In other words, the max object size to avoid a humongous allocation goes from 4mb down to 2mb.
If there are 3mb objects in your process the penalty from the region size change may suddenly cause randomly very long GCs that are worse than the heap utilization you are trying to avoid in

## In Summary

Be more cautious with the 31GB max heap size recommendation it may help as much as it hurts, it is definitely advisable to TRY it but note there are at least with the G1GC some downsides to it.
