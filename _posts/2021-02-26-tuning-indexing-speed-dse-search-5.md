---
title: Tuning Indexing Speed in DSE Search 5.x
tags: [dse, solr]
---
What follows is a summary of the things you need to consider dealing with indexing speed problems in DSE 5.x (note the model of indexing is wildly different in DSE 6.x and will not apply, I will have a guide on that soon).

## Dropped Mutations

With Solr 5.x dropped mutations have three causes over regular Cassandra:
* During the merging of Solr indexes, you can "stall" due to configuration limits.
* By default, Solr indexing is very aggressive and can starve IO, all activities will slow, and the cluster may experience dropped mutations.
* Back pressure leading to drops. If QueueWeight in the com.datastax.bdp.search.keyspace_name.table_name.IndexPool MBean is greater than back_pressure_threshold_per_core, back pressure is happening.

To minimize IO contention and merge stalling do the following steps:
* Run at least DSE version 5.1.8 as there are several performance bugs in the earlier releases.
* Make sure MAX_HEAP_SIZE in jvm.options is 31GB if possible unless you have enough ram to get away with 64GB.
* Move `solr_data_dir` to it's own dedicated drive or raid array see set the location of search indexes for 5.0 or 5.1
* Set read ahead to 8 on the storage device backing the folder. 
* Set in solr_data_dir: in "dse.yaml" (assuming the storage is SSD/NVMe or equivalent latency and throughput). If LVM or RAID is in use, make sure it's set to 8 on all underlying devices.
* If needed raise `maxMergeCount` to 8 x `num_tokens` or 2 x `max_concurrency_solr_per_core`, whichever is higher, in solrconfig.xml for each Solr enabled table.
* Raise `back_pressure_threshold_per_core` up to 100k (assuming adequate heap available). This can also be done at runtime via `nodetool sjk mx -b "com.datastax.bdp:type=search,index=keyspace.table_name,name=IndexPool" -f BackPressureThreshold --set -v 100000`.
* Disable `enable_back_pressure_adaptive_nrt_commit` to minimize dropped mutations. Note: this setting will not eliminate them and sometimes cause them. Therefore, disable `enable_back_pressure_adaptive_nrt_commit` to get rid of them entirely.
* Lower `max_solr_concurrency_per_core` to reduce the IO load, raise the same to increase indexing rate. We need to find the right level for each use case and set of hardware.
* Raise autoCommitTime to 60000 milliseconds on each table where `<rt>false</rt> `in their solrconfig.xml:
  * In CQLSH, run `ALTER SEARCH INDEX CONFIG ON demo.health_data SET autoCommitTime = 60000`; This will mean updates to search are visible only after a minute.
  * In CQLSH, run `RELOAD SEARCH INDEX ON demo.health_data`;
* raise ram buffer:
  * In the solrconfig.xml for any table then raise `<ramBufferSizeMB></ramBufferSizeMB>` by some multiple (up to several gigabytes).
* Index fewer columns.
* Index fewer tables. If there are just 10s-1000s of active Solr tables on a system, the system will become overwhelmed.
* If columns where Trie types are used only for sorting, then we can either decrease precision or disable indexing and keep docValues - this should reduce index size.

## Delayed Updates

Records aren't available for search as soon as the users would like them or are "out of sync" between Cassandra data and Solr. Sometimes, this is just how Solr works with DSE.
However, there is one nasty bug that affects 5.1.x where stale data may stick around in the Solr Index on Solr enabled tables using  `<rt>true</rt>` in solrconfig.xml. The fix is simple, upgrade to  DSE 5.1.17

### Consistency Problems

Solr only consults a SINGLE replica when querying data, and Cassandra can query all the replicas. The fix is easy: nodetool repair -pr on all the nodes. However, this will not prevent further inconsistency, and periodic inconsistency is fundamentally a DSE search design issue.

Mutation lag problems
The users may complain about matching records on DSE Search that do not match the actual data found. An example of this follows:
```
SELECT * from my_table where solr_query='{"q":"status:processed"}'

-- [id] | [status]
--  1   | processed
--- 2   | completed
```
This behavior is easy to explain, the Solr index updates AFTER Cassandra is already updated, so there are periods Cassandra and Solr will potentially be out of sync. Since this is the reality, the fixes for this can be challenging:
* Data modeling and or application design changes
* However, if index lag is taking longer than `autoCommitTime`, consider all the steps above in the "Dropped Mutations" section as this may be a throughput issue.

### Shrinking an index

A good way to index more rows per second is to index less per row. Some text types generate more data on disk and require more IO and CPU to index the values. The following is the list of most expensive text field types to index in order of most (at #1) to least (#5)
* Text with `NGramTokenizer`
* Text with `StandardTokenizer` or `WhiteSpaceTokenizer`.
* Text with `omitNorms=true` (this disables length normalization for the field and saves some memory)
* Text with `omitNorms=true` and `omitTermFreqAndPositions=true` (Queries that rely on term position with this option will silently fail to find documents.)
* Text with KeywordTokenizer or the String type (not tokenized text

## Conclusion

This is a very whirlwind walk through of the various tunings one can do to get indexing throughput up in DSE Search. I myself have used this framework many times and realized gains of 10x in indexing throughput just doing these steps. For more in deph tuning taking into account IO and CPU stay tuned.
