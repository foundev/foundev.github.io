---
title: Detecting and dealing with backpressure in DSE 6.x
date: 2021-07-28T08:11:00+00:00
author: Ryan Svihla
layout: post
tags: [ dse, backpressure, DataStax ]
---

Several years ago DataStax change DataStax Enterprise from a version of Cassandra with some closed source plugins and a handful of fixes most of which were backports of
fixes in very old versions, to [a fundamentally different architecture](https://www.datastax.com/blog/dse-advanced-performance-apache-cassandratm-goes-turbo). This new architecure we will
refer to as TPC, however, there were also several internals that were changed that may have relied or depended on TPC but were not actually themselves part of TPC.

Today I want to review one of those features TPC Backpressure. TPC Backpressure in theory stops the node from running out of memory or becoming unresponsive and being somewhat down (in Cassandra this is often worse than being down). TPC Backpressure
has a complex implementation and can be difficult to explain, but for the sake of brevity I am going to focus on two primary thresholds that when passed the node will
pause new requests allowing the existing requests to complete.

## log messages

backpressure active regex, tells you when it is engaged

```shell
"DEBUG\s+\[(?P<thread>.*)\] (?P<date>.{10} .{12}) *(?P<source_file>[^:]*):(?P<source_line>[0-9]*) - TPC backpressure is active on core (?P<core_num>\d+) with global local/remote pending tasks at (?P<global_pending>\d+)/(?P<remote_pending>\d+)"
```

You can also just use [ripgrep](https://github.com/BurntSushi/ripgrep#installation) for `TPC backpressure is active` and see how often that is enabled. If I want to be extra fancy I can take the regex above, combine it with regrep and output the remoting and global pending values:

for global:

`rg "DEBUG\s+\[(?P<thread>.*)\] (?P<date>.{10} .{12}) *(?P<source_file>[^:]*):(?P<source_line>[0-9]*) - TPC backpressure is active on core (?P<core_num>\d+) with global local/remote pending tasks at (?P<global_pending>\d+)/(?P<remote_pending>\d+)" -or  '$global_pending'`

for remote:

`rg "DEBUG\s+\[(?P<thread>.*)\] (?P<date>.{10} .{12}) *(?P<source_file>[^:]*):(?P<source_line>[0-9]*) - TPC backpressure is active on core (?P<core_num>\d+) with global local/remote pending tasks at (?P<global_pending>\d+)/(?P<remote_pending>\d+)" -or  '$remote_pending'`

The higher it is the longer it will take to clear out, this can be used to measure severity, once you have the total you can try and find the time it occured at. You can find the 5 worse totals with the following

```sh
rg "DEBUG\s+\[(?P<thread>.*)\] (?P<date>.{10} .{12}) *(?P<source_file>[^:]*):(?P<source_line>[0-9]*) - TPC backpressure is active on core (?P<core_num>\d+) with global local/remote pending tasks at (?P<global_pending>\d+)/(?P<remote_pending>\d+)"  -or  '$global_pending' --no-filename | sort -n | tail -n 5
134
813
1111
1831
1911
```

do your grep again but filter out for the worst value

```sh
rg "DEBUG\s+\[(?P<thread>.*)\] (?P<date>.{10} .{12}) *(?P<source_file>[^:]*):(?P<source_line>[0-9]*) - TPC backpressure is active on core (?P<core_num>\d+) with global local/remote pending tasks at (?P<global_pending>\d+)/(?P<remote_pending>\d+)" | rg 1911
debug.log:DEBUG [CoreThread-1] 2020-01-01 01:01:01,000  NoSpamLogger.java:92 - TPC backpressure is active on core 1 with global local/remote pending tasks at 1911/120
```

Now you can compare that to node latencies at that time and see if that matches the problems you are trying to find with latency and timesouts.

## what to do

There is some art to the next step, one needs to evaluate if raising backpressure will actually help or hurt the situation. But let us say you see the GC is low, the CPU usage is low
and the latencies are bad, it just could be a workload that the defaults are too low.

### checking existing state

To know the next steps we need to take state of the system

#### Check GC

`sperf core gc` is a good tool for this, and can quickly tell you how severe gc is. For example in this report:

```sh
gcinspector version 0.6.4

. <300ms + 301-500ms ! >500ms
------------------------------
2020-01-10 16:28:37 236 ...............+++........++.....+.+...+++.++.+.+......+.....+.!!+!.!++!+..++.+.!..+.!++++.!.++++.+.+++..+!!.......!..+.+....+.....++.+...+.+.++.+.+!!++.+.+.!++.+.+...+.+..+.+.+.+..+++....++..+++....+..++.+++.+!+..+.+.+.+!......+++....+

busiest period: 2020-01-10 16:28:37 (75041ms)


GC pauses  max        p99        p75        p50        p25        min        
           ---        ---        ---        ---        ---        ---        
ms         800        729        358        282        243        201        

Worst pauses in ms:
[800, 735, 729]

Collections by type
--------------------
* G1 Young: 236
```

The GC is extremely heavy and the target gc rate was 500ms, this is not a cluster you wan to raise backpressure on. Now let us look at a cluster that has good GC and would be at least
safe to raise backpressure limits on:

```sh
gcinspector version 0.6.4

. <300ms + 301-500ms ! >500ms
------------------------------
2020-01-10 16:28:37 10 .........

busiest period: 2020-01-10 16:28:37 (75041ms)


GC pauses  max        p99        p75        p50        p25        min        
           ---        ---        ---        ---        ---        ---        
ms         300        289        250        225        210        201        

Worst pauses in ms:
[300, 289, 250]

Collections by type
--------------------
* G1 Young: 10
```

In this case the system is not very busy with GC activity and if there are high pending writes and reads, and we find backpressure is being enabled, raising those limits may help system performance.

#### Check Pending

`sperf core statuslogger` can generate some very useful reports to track the number of pending operations in your cluster. Below I've shared an artificial example:

```
sperf core statuslogger version: 0.6.13

Summary (111,111 lines)
Summary (0 skipped lines)

dse versions: {'6.x'}
cassandra versions: unknown
first log time: 2021-01-01 01:11:01.111000+00:00
last log time: 2021-01-01 01:01:01.111000+00:00
duration: 10.00 minutes
total stages analyzed: 111
total nodes analyzed: 1

GC pauses  max        p99        p75        p50        p25        min
           ---        ---        ---        ---        ---        ---
ms         500       500         400        350        250        250
total GC events: 11

busiest tables by ops across all nodes
------------------------------
* debug.log: test.tester: 1,000,000 ops / 11.11 mb data

busiest table by data across all nodes
------------------------------
* debug.log: test.tester: 111,111 ops / 11.11 mb data

busiest stages across all nodes
------------------------------
* TPC/9 local backpressure:                         11115  (debug.log)
* TPC/4 local backpressure:                         6791   (debug.log)
* TPC/all/BACKPRESSURED_MESSAGE_DECODE active:      6618   (debug.log)
* TPC/4/BACKPRESSURED_MESSAGE_DECODE active:        5743   (debug.log)
* TPC/1 local backpressure:                         5414   (debug.log)
* TPC/2 local backpressure:                        5111   (debug.log)
* TPC/all/WRITE_REMOTE pending:                     4967   (debug.log)
* TPC/all/WRITE_RESPONSE active:                    4771   (debug.log)
* TPC/3/WRITE_RESPONSE active:                      4460   (debug.log)

busiest stages in PENDING
------------------------------
debug.log:
       TPC/all/WRITE_REMOTE:             4967
       TPC/all/READ_LOCAL:               4599
       TPC/3/WRITE_REMOTE:               1455
       TPC/1/WRITE_REMOTE:               1442
       TPC/2/READ_LOCAL:                 1441
       TPC/3/READ_LOCAL:                 1034
       TPC/9/READ_LOCAL:                 935
       TPC/9/WRITE_REMOTE:               988


busiest LOCAL BACKPRESSURE
------------------------------
debug.log:
       avg backpressure                  1332.06
       max backpressure                  11111
```

Here we can see there is a lot of backpressure and realitively little GC happening in this case this would suggest to me we can raise the backpressure limits to see if latency improves and more of the system is utilized.


### raising backpressure limits

The two main paramters I like to focus on are (both in the cassandra.yaml):

`tpc_concurrent_requests_limit` -  the number of concurrently executed read/write requests per core, to be increased only if the CPU is under utilized, or decreased only in case of excessive memory pressure (i.e. long GCs/OOM).
`tpc_pending_requests_limit` - the number of pending read/write requests per core, to be increased only if getting too many timeouts. 

Try raising this and repeat your tests, continue to monitor GC and CPU utilization.

### upgrading version!

DSE 6.8 adds work stealing, and badly balanced data models, or apps with anti-patterns have a less significant impact on the cluster health. The downside to this is
writes will still go to a particular Core and this means data models 

### raising work stealing

By default in DSE 6.8 work stealing is pretty conservative as the developers wanted us to get the benefit of TPC, but nearly every cluster does seem to have an application
that would benefit from work stealing so it is there. However, some clusters contain apps that primarily have anti-patterns, and in these cases the defaults for work stealing maybe too minimal.

#### track work stealing and pending cores

* using something like `sperf core statuslogger` try and see if there is a high number of pending operations, especially on singular cores, if so you may benefit from raising work stealing
* track how much work stealing is going on, if it is consistently happening, that is a hint there is a balance issue and raising it more may help, [my notebook on performance](https://github.com/foundev/notebooks/blob/main/performance/analysis-general.ipynb) can graph
this for you, the key thing you are looking for is _sustained_ work stealing.

Anothing thing you can use is [ripgrep](https://github.com/BurntSushi/ripgrep#installation) in your debug.log with this regex `DEBUG \[(?P<thread>.*)\] (?P<date>.{10} .{12}) *(?P<source_file>[^:]*):(?P<source_line>[0-9]*) - Stole (?P<tasks>\d+) tasks since last time\.`

##### Actions

to the jmv-server.options add the following and reboot:

```
-Ddse.tpc.work_stealing_max_unparks=<half of tpc_cores> (defaults to 1/4 of the TPC cores so if I had 8 cores, the default is 2, raising that to 4 may help work stealing) 
-Ddse.tpc.work_stealing_max_tasks=512 (default = 32)
```

Review if this helps the total pending tasks or not.

### changing data model

Writes will continue to pin to an individual core. The classic very naive time series data model where the partition key is a time bucket, will in the case of TPC pin
all writes to one core, and all requests to that core will be backed up. Eventually this will lead to backpressure, despite the node itself not being very much
stress and in fact being very underused.

#### Example TPC stats output for this sort of situation

Scenario:

* time is bucketed on a per minute basis and this is the partition key for all writes
* there are 4 cores per node
* there are 6 nodes with RF 3

##### At 2021-07-28 11:00:00 the write traffic for the next minute can looks like this

*cores list total pending writes* 

```
| node | cpu usage | cores1    | core2 | core3 | core4 | 
| ---- | --------- | –––------ | --–-— | ----- | ----- | 
| 1    | 25%       | 134211    | 0     | 0     |  0    |
| 2    | 25%       | 0         | 0     | 0     | 12441 |
| 3    | 25%       | 0         | 13441 | 0     | 0     |
| 4    | 0%        | 0         | 0     | 0     | 0     |
| 5    | 0%        | 0         | 0     | 0     | 0     |
| 6    | 0%        | 0         | 0     | 0     | 0     |
```

##### At 2021-07-28 11:01:00 the write traffic for the next minute can looks like this

```
| node | cpu usage | cores1    | core2 | core3 | core4 | 
| ---- | --------- | –––------ | --–-— | ----- | ----- | 
| 1    | 0%        | 0         | 0     | 0     | 0     |
| 2    | 25%       | 0         | 0     | 0     | 14552 |
| 3    | 25%       | 0         | 12442 | 0     | 0     |
| 4    | 25%       | 0         | 0     | 12498 | 0     |
| 5    | 0%        | 0         | 0     | 0     | 0     |
| 6    | 0%        | 0         | 0     | 0     | 0     |
```

You get the idea, this repeats like this for every minute, using effectivley only one CPU core on 3 nodes for an entire minute which is not something useful from a scaling standpoint an exposes problematic data models and hotspots pretty quickly, worse it will have global effects if those individual
cores hit the backpressure threshold levels.
    
#### The fix

The only fix for this is to change the data model and add in an extra column to the partition key which will require a new table. There are a few common approaches:

* add a known value from the data that is not so time deterministic, and still well enough distributed.  For example, if there is a state (something well known) you can use that and just query for all states during reads.
* add a known value that is known ahead of time, something like [1-30] and randomly pick one on each write, clients need to know to query all of those extra buckets.
* add a random value but track that the random value is in that time bucket so you can go back and query those. This has a lot of quirks and can be tricky, I do not see this very much now.

## Conclusion

This was a rather simplistic view of backpressure, and those that have moved beyond this level of depth can safely ignore this article, it is intended to make an audience understand the most basic behaviors of TPC Backpressure 
and is not to be viewed as the final word on backpressure tuning. This will help you out with 80 % of the cases where backpressure is enabled and what are the next steps.


