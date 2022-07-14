---
layout: post
tags: []
categories: []
#date: 2019-06-25 13:14:15
#excerpt: ''
#image: 'BASEURL/assets/blog/img/.png'
#description:
#permalink:

---


# Coding in Lieu of Scripting in Practice

I wrote a short blog yesterday about how I approach the problem of munging large amount of log data without just relying on grep, sed or awk to do my troubleshooting. I would like to talk about how that tends to actually work out.

## finding patterns

Take the following log from a random server that maybe has issues.

```txt

INFO [main] 2019-12-10 22:37:19,773 YamlConfigurationLoader.java:89 - Configuration location: file:/home/ubuntu/apache-cassandra-3.11.5/conf/cassandra.yaml
INFO [main] 2019-12-10 22:37:20,087 Config.java:516 - Node configuration:[allocate_tokens_for_keyspace=null; authenticator=AllowAllAuthenticator; authorizer=AllowAllAuthorizer; auto_bootstrap=true; auto_snapshot=true; back_pressure_enabled=false; back_pressure_strategy=org.apache.cassandra.net.RateBasedBackPressure{high_ratio=0.9, factor=5, flow=FAST}; batch_size_fail_threshold_in_kb=50; batch_size_warn_threshold_in_kb=5; batchlog_replay_throttle_in_kb=1024; broadcast_address=null; broadcast_rpc_address=null; buffer_pool_use_heap_if_exhausted=true; cas_contention_timeout_in_ms=1000; cdc_enabled=false; cdc_free_space_check_interval_ms=250; cdc_raw_directory=null; cdc_total_space_in_mb=0; client_encryption_options=<REDACTED>; cluster_name=Test Cluster; column_index_cache_size_in_kb=2; column_index_size_in_kb=64; commit_failure_policy=stop; commitlog_compression=null; commitlog_directory=null; commitlog_max_compression_buffers_in_pool=3; commitlog_periodic_queue_size=-1; commitlog_segment_size_in_mb=32; commitlog_sync=periodic; commitlog_sync_batch_window_in_ms=NaN; commitlog_sync_period_in_ms=10000; commitlog_total_space_in_mb=null; compaction_large_partition_warning_threshold_mb=100; compaction_throughput_mb_per_sec=16; concurrent_compactors=null; concurrent_counter_writes=32; concurrent_materialized_view_writes=32; concurrent_reads=32; concurrent_replicates=null; concurrent_writes=32; counter_cache_keys_to_save=2147483647; counter_cache_save_period=7200; counter_cache_size_in_mb=null; counter_write_request_timeout_in_ms=5000; credentials_cache_max_entries=1000; credentials_update_interval_in_ms=-1; credentials_validity_in_ms=2000; cross_node_timeout=false; data_file_directories=[Ljava.lang.String;@3ee0fea4; disk_access_mode=auto; disk_failure_policy=stop; disk_optimization_estimate_percentile=0.95; disk_optimization_page_cross_chance=0.1; disk_optimization_strategy=ssd; dynamic_snitch=true; dynamic_snitch_badness_threshold=0.1; dynamic_snitch_reset_interval_in_ms=600000; dynamic_snitch_update_interval_in_ms=100; enable_materialized_views=true; enable_sasi_indexes=true; enable_scripted_user_defined_functions=false; enable_user_defined_functions=false; enable_user_defined_functions_threads=true; encryption_options=null; endpoint_snitch=SimpleSnitch; file_cache_round_up=null; file_cache_size_in_mb=null; gc_log_threshold_in_ms=200; gc_warn_threshold_in_ms=1000; hinted_handoff_disabled_datacenters=[]; hinted_handoff_enabled=true; hinted_handoff_throttle_in_kb=1024; hints_compression=null; hints_directory=null; hints_flush_period_in_ms=10000; incremental_backups=false; index_interval=null; index_summary_capacity_in_mb=null; index_summary_resize_interval_in_minutes=60; initial_token=null; inter_dc_stream_throughput_outbound_megabits_per_sec=200; inter_dc_tcp_nodelay=false; internode_authenticator=null; internode_compression=dc; internode_recv_buff_size_in_bytes=0; internode_send_buff_size_in_bytes=0; key_cache_keys_to_save=2147483647; key_cache_save_period=14400; key_cache_size_in_mb=null; listen_address=localhost; listen_interface=null; listen_interface_prefer_ipv6=false; listen_on_broadcast_address=false; max_hint_window_in_ms=10800000; max_hints_delivery_threads=2; max_hints_file_size_in_mb=128; max_mutation_size_in_kb=null; max_streaming_retries=3; max_value_size_in_mb=256; memtable_allocation_type=heap_buffers; memtable_cleanup_threshold=null; memtable_flush_writers=0; memtable_heap_space_in_mb=null; memtable_offheap_space_in_mb=null; min_free_space_per_drive_in_mb=50; native_transport_flush_in_batches_legacy=true; native_transport_max_concurrent_connections=-1; native_transport_max_concurrent_connections_per_ip=-1; native_transport_max_concurrent_requests_in_bytes=-1; native_transport_max_concurrent_requests_in_bytes_per_ip=-1; native_transport_max_frame_size_in_mb=256; native_transport_max_negotiable_protocol_version=-2147483648; native_transport_max_threads=128; native_transport_port=9042; native_transport_port_ssl=null; num_tokens=256; otc_backlog_expiration_interval_ms=200; otc_coalescing_enough_coalesced_messages=8; otc_coalescing_strategy=DISABLED; otc_coalescing_window_us=200; partitioner=org.apache.cassandra.dht.Murmur3Partitioner; permissions_cache_max_entries=1000; permissions_update_interval_in_ms=-1; permissions_validity_in_ms=2000; phi_convict_threshold=8.0; prepared_statements_cache_size_mb=null; range_request_timeout_in_ms=10000; read_request_timeout_in_ms=5000; repair_session_max_tree_depth=18; request_scheduler=org.apache.cassandra.scheduler.NoScheduler; request_scheduler_id=null; request_scheduler_options=null; request_timeout_in_ms=10000; role_manager=CassandraRoleManager; roles_cache_max_entries=1000; roles_update_interval_in_ms=-1; roles_validity_in_ms=2000; row_cache_class_name=org.apache.cassandra.cache.OHCProvider; row_cache_keys_to_save=2147483647; row_cache_save_period=0; row_cache_size_in_mb=0; rpc_address=localhost; rpc_interface=null; rpc_interface_prefer_ipv6=false; rpc_keepalive=true; rpc_listen_backlog=50; rpc_max_threads=2147483647; rpc_min_threads=16; rpc_port=9160; rpc_recv_buff_size_in_bytes=null; rpc_send_buff_size_in_bytes=null; rpc_server_type=sync; saved_caches_directory=null; seed_provider=org.apache.cassandra.locator.SimpleSeedProvider{seeds=127.0.0.1}; server_encryption_options=<REDACTED>; slow_query_log_timeout_in_ms=500; snapshot_before_compaction=false; ssl_storage_port=7001; sstable_preemptive_open_interval_in_mb=50; start_native_transport=true; start_rpc=false; storage_port=7000; stream_throughput_outbound_megabits_per_sec=200; streaming_keep_alive_period_in_secs=300; streaming_socket_timeout_in_ms=86400000; thrift_framed_transport_size_in_mb=15; thrift_max_message_length_in_mb=16; thrift_prepared_statements_cache_size_mb=null; tombstone_failure_threshold=100000; tombstone_warn_threshold=1000; tracetype_query_ttl=86400; tracetype_repair_ttl=604800; transparent_data_encryption_options=org.apache.cassandra.config.TransparentDataEncryptionOptions@48524010; trickle_fsync=false; trickle_fsync_interval_in_kb=10240; truncate_request_timeout_in_ms=60000; unlogged_batch_across_partitions_warn_threshold=10; user_defined_function_fail_timeout=1500; user_defined_function_warn_timeout=500; user_function_timeout_policy=die; windows_timer_interval=1; write_request_timeout_in_ms=2000]
INFO [main] 2019-12-10 22:37:20,088 DatabaseDescriptor.java:381 - DiskAccessMode 'auto' determined to be mmap, indexAccessMode is mmap
INFO [main] 2019-12-10 22:37:20,088 DatabaseDescriptor.java:439 - Global memtable on-heap threshold is enabled at 919MB
INFO [main] 2019-12-10 22:37:20,089 DatabaseDescriptor.java:443 - Global memtable off-heap threshold is enabled at 919MB
WARN [main] 2019-12-10 22:37:20,243 DatabaseDescriptor.java:579 - Only 54.609GiB free across all data volumes. Consider adding more capacity to your cluster or removing obsolete snapshots
INFO [main] 2019-12-10 22:37:20,281 RateBasedBackPressure.java:123 - Initialized back-pressure with high ratio: 0.9, factor: 5, flow: FAST, window size: 2000.
INFO [main] 2019-12-10 22:37:20,281 DatabaseDescriptor.java:773 - Back-pressure is disabled with strategy org.apache.cassandra.net.RateBasedBackPressure{high_ratio=0.9, factor=5, flow=FAST}.
INFO [main] 2019-12-10 22:37:20,430 JMXServerUtils.java:246 - Configured JMX server at: service:jmx:rmi://127.0.0.1/jndi/rmi://127.0.0.1:7199/jmxrmi
INFO [main] 2019-12-10 22:37:20,439 CassandraDaemon.java:476 - Hostname: ryan-java-devINFO [main] 2019-12-10 22:37:20,439 CassandraDaemon.java:483 - JVM vendor/version: OpenJDK 64-Bit Server VM/1.8.0_222
INFO [main] 2019-12-10 22:37:20,440 CassandraDaemon.java:484 - Heap size: 3.592GiB/3.592GiB
INFO [main] 2019-12-10 22:37:20,440 CassandraDaemon.java:489 - Code Cache Non-heap memory: init = 2555904(2496K) used = 4285440(4185K) committed = 4325376(4224K) max = 251658240(245760K)INFO [main] 2019-12-10 22:37:20,441 CassandraDaemon.java:489 - Metaspace Non-heap memory: init = 0(0K) used = 17108928(16707K) committed = 17694720(17280K) max = -1(-1K)INFO [main] 2019-12-10 22:37:20,441 CassandraDaemon.java:489 - Compressed Class Space Non-heap memory: init = 0(0K) used = 2056736(2008K) committed = 2228224(2176K) max = 1073741824(1048576K)
INFO [main] 2019-12-10 22:37:20,441 CassandraDaemon.java:489 - Par Eden Space Heap memory: init = 671088640(655360K) used = 161072712(157297K) committed = 671088640(655360K) max = 671088640(655360K)INFO [main] 2019-12-10 22:37:20,442 CassandraDaemon.java:489 - Par Survivor Space Heap memory: init = 83886080(81920K) used = 0(0K) committed = 83886080(81920K) max = 83886080(81920K)INFO [main] 2019-12-10 22:37:20,442 CassandraDaemon.java:489 - CMS Old Gen Heap memory: init = 3101687808(3028992K) used = 0(0K) committed = 3101687808(3028992K) max = 3101687808(3028992K)
INFO [main] 2019-12-10 22:37:20,442 CassandraDaemon.java:491 - Classpath: /home/ubuntu/apache-cassandra-3.11.5/bin/../conf:/home/ubuntu/apache-cassandra-3.11.5/bin/../build/classes/main:/home/ubuntu/apache-cassandra-3.11.5/bin/../build/classes/thrift:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/HdrHistogram-2.1.9.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/ST4-4.0.8.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/airline-0.6.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/antlr-runtime-3.5.2.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/apache-cassandra-3.11.5.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/apache-cassandra-thrift-3.11.5.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/asm-5.0.4.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/caffeine-2.2.6.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/cassandra-driver-core-3.0.1-shaded.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/commons-cli-1.1.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/commons-codec-1.9.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/commons-lang3-3.1.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/commons-math3-3.2.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/compress-lzf-0.8.4.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/concurrent-trees-2.4.0.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/concurrentlinkedhashmap-lru-1.4.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/disruptor-3.0.1.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/ecj-4.4.2.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/guava-18.0.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/high-scale-lib-1.0.6.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/hppc-0.5.4.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/jackson-core-asl-1.9.13.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/jackson-mapper-asl-1.9.13.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/jamm-0.3.0.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/javax.inject.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/jbcrypt-0.3m.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/jcl-over-slf4j-1.7.7.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/jctools-core-1.2.1.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/jflex-1.6.0.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/jna-4.2.2.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/joda-time-2.4.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/json-simple-1.1.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/jstackjunit-0.0.1.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/libthrift-0.9.2.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/log4j-over-slf4j-1.7.7.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/logback-classic-1.1.3.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/logback-core-1.1.3.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/lz4-1.3.0.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/metrics-core-3.1.5.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/metrics-jvm-3.1.5.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/metrics-logback-3.1.5.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/netty-all-4.0.44.Final.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/ohc-core-0.4.4.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/ohc-core-j8-0.4.4.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/reporter-config-base-3.0.3.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/reporter-config3-3.0.3.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/sigar-1.6.4.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/slf4j-api-1.7.7.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/snakeyaml-1.11.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/snappy-java-1.1.1.7.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/snowball-stemmer-1.3.0.581.1.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/stream-2.5.2.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/thrift-server-0.3.7.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/jsr223/*/*.jar:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/jamm-0.3.0.jar
INFO [main] 2019-12-10 22:37:20,443 CassandraDaemon.java:493 - JVM Arguments: [-Xloggc:/home/ubuntu/apache-cassandra-3.11.5/bin/../logs/gc.log, -ea, -XX:+UseThreadPriorities, -XX:ThreadPriorityPolicy=42, -XX:+HeapDumpOnOutOfMemoryError, -Xss256k, -XX:StringTableSize=1000003, -XX:+AlwaysPreTouch, -XX:-UseBiasedLocking, -XX:+UseTLAB, -XX:+ResizeTLAB, -XX:+UseNUMA, -XX:+PerfDisableSharedMem, -Djava.net.preferIPv4Stack=true, -XX:+UseParNewGC, -XX:+UseConcMarkSweepGC, -XX:+CMSParallelRemarkEnabled, -XX:SurvivorRatio=8, -XX:MaxTenuringThreshold=1, -XX:CMSInitiatingOccupancyFraction=75, -XX:+UseCMSInitiatingOccupancyOnly, -XX:CMSWaitDuration=10000, -XX:+CMSParallelInitialMarkEnabled, -XX:+CMSEdenChunksRecordAlways, -XX:+CMSClassUnloadingEnabled, -XX:+PrintGCDetails, -XX:+PrintGCDateStamps, -XX:+PrintHeapAtGC, -XX:+PrintTenuringDistribution, -XX:+PrintGCApplicationStoppedTime, -XX:+PrintPromotionFailure, -XX:+UseGCLogFileRotation, -XX:NumberOfGCLogFiles=10, -XX:GCLogFileSize=10M, -Xms3757M, -Xmx3757M, -Xmn800M, -XX:+UseCondCardMark, -XX:CompileCommandFile=/home/ubuntu/apache-cassandra-3.11.5/bin/../conf/hotspot_compiler, -javaagent:/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/jamm-0.3.0.jar, -Dcassandra.jmx.local.port=7199, -Dcom.sun.management.jmxremote.authenticate=false, -Dcom.sun.management.jmxremote.password.file=/etc/cassandra/jmxremote.password, -Djava.library.path=/home/ubuntu/apache-cassandra-3.11.5/bin/../lib/sigar-bin, -XX:OnOutOfMemoryError=kill -9 %p, -Dlogback.configurationFile=logback.xml, -Dcassandra.logdir=/home/ubuntu/apache-cassandra-3.11.5/bin/../logs, -Dcassandra.storagedir=/home/ubuntu/apache-cassandra-3.11.5/bin/../data]
INFO [main] 2019-12-10 22:37:20,939 NativeLibrary.java:176 - JNA mlockall successful
WARN [main] 2019-12-10 22:37:20,940 StartupChecks.java:136 - jemalloc shared library could not be preloaded to speed up memory allocations
WARN [main] 2019-12-10 22:37:20,941 StartupChecks.java:169 - JMX is not enabled to receive remote connections. Please see cassandra-env.sh for more info.
INFO [main] 2019-12-10 22:37:20,944 SigarLibrary.java:44 - Initializing SIGAR library
INFO [main] 2019-12-10 22:37:20,959 SigarLibrary.java:180 - Checked OS settings and found them configured for optimal performance.
WARN [main] 2019-12-10 22:37:20,963 StartupChecks.java:311 - Maximum number of memory map areas per process (vm.max_map_count) 65530 is too low, recommended value: 1048575, you can change it with sysctl.
WARN [main] 2019-12-10 22:37:20,974 StartupChecks.java:332 - Directory /home/ubuntu/apache-cassandra-3.11.5/bin/../data/data doesn't exist
WARN [main] 2019-12-10 22:37:20,981 StartupChecks.java:332 - Directory /home/ubuntu/apache-cassandra-3.11.5/bin/../data/commitlog doesn't exist
WARN [main] 2019-12-10 22:37:20,982 StartupChecks.java:332 - Directory /home/ubuntu/apache-cassandra-3.11.5/bin/../data/saved_caches doesn't exist
WARN [main] 2019-12-10 22:37:20,983 StartupChecks.java:332 - Directory /home/ubuntu/apache-cassandra-3.11.5/bin/../data/hints doesn't exist
```

This is a Cassandra startup log I have taken from an old computer. This is only the first few lines and not even close to a full startup log. Most would agree, it is still a great deal of text.

# grep

The naive approach is to grep the WARN and ERROR logs and that can be sometimes interesting and when you are new to a tech thus is a good first pass.

```sh
grep WARN server.log
WARN [main] 2019-12-10 22:37:20,940 StartupChecks.java:136 - jemalloc shared library could not be preloaded to speed up memory allocations
WARN [main] 2019-12-10 22:37:20,941 StartupChecks.java:169 - JMX is not enabled to receive remote connections. Please see cassandra-env.sh for more info.
WARN [main] 2019-12-10 22:37:20,963 StartupChecks.java:311 - Maximum number of memory map areas per process (vm.max_map_count) 65530 is too low, recommended value: 1048575, you can change it with sysctl.
WARN [main] 2019-12-10 22:37:20,974 StartupChecks.java:332 - Directory /home/ubuntu/apache-cassandra-3.11.5/bin/../data/data doesn't exist
WARN [main] 2019-12-10 22:37:20,981 StartupChecks.java:332 - Directory /home/ubuntu/apache-cassandra-3.11.5/bin/../data/commitlog doesn't exist
WARN [main] 2019-12-10 22:37:20,982 StartupChecks.java:332 - Directory /home/ubuntu/apache-cassandra-3.11.5/bin/../data/saved_caches doesn't exist
WARN [main] 2019-12-10 22:37:20,983 StartupChecks.java:332 - Directory /home/ubuntu/apache-cassandra-3.11.5/bin/../data/hints doesn't exist
```

But grep wouldn't filter the logs down very much and it still requires a lot of reading. However, I can tell you at glance there are two performance issues in there and depending of the scale of issue this is a good potential explaination for root cause of performance issues. I am intentionally going to avoid explaining which of those lines has issues to demonstrate how experienced one has to be to make use of just grep.

# Script

OK so you get more experience and you learn INFO contains some super useful information but you learn to look at specific lines, this is difficult to teach your newer colleagues so you now write this script `get_heap.sh`

```bash
#!/bin/sh

grep 'Heap size' $1
```
And I run it in my file 

```shell
./get_heap.sh ./system.log
INFO  [main] 2019-12-10 22:37:20,440 CassandraDaemon.java:484 - Heap size: 3.592GiB/3.592GiB
```

This is great now I see a tiny heap let's say I want to do comparison now to tell the new guys a 3.593GiB heap is way to small, doing this in script is frankly ugly and error prone.

```bash
#!/bin/bash

heap=$(grep 'Heap size' $1  | awk '{print $9}' | awk -F . '{print $1}')
minheap=16
if (( $heap < $minheap )); then
        echo "heap size of $heap GiB is smaller than the minimum heap of $minheap GiB needed for decent performance"
fi
```
Ok great now I get a warning for the new hires. Maybe in the future though somone slips through because there are other logs that match but have a different format so now I need to either use regexps which no one seems to understand. What happens if I want to find multple types of lines with different rules? Say I want to include those two other issues I eluded too earlier? How do I write automated tests so I don't break it later? While I can still do all that in Bash it is not the common path.

## Python

What if I just did all this in Python? Is it any slower to write? Probably not all.

```python
#!/usr/bin/python                                                     
import sys
file = sys.argv[1]

def check_heap(line):
  tokens = line.split(' ')
  heap = int(tokens[9].split(".")[0])
  minheap =16
  if heap < minheap:
    return  f"heap size of {{heap}} GiB is smaller than the minimum heap of {{minheap}} GiB needed for decent performance"

with open(file) as f:
  lines = f.readlines()
  for line in lines:
    if "Heap size" in line:
     print(check_heap(line))
```

This is not harder to grasp in fact for many it maybe easier, it is easier to test, to automate and it took me less time to write.
Most importantly it will be trivial to add several checks without reparsing the whole file
over and over again.
