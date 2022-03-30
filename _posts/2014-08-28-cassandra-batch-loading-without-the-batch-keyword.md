---
date: 2014-08-28T13:10:55+00:00
author: Ryan Svihla
layout: post
tags:
  - Cassandra
---
<h1>Cassandra - Batch loading without the Batch keyword</h1>
ATTENTION:

_This post is intentionally simplistic to help explain tradeoffs that need to be made. If you are looking for some production level nuance go [read this afterwords.](https://blog.foundev.pro/2016/04/29/cassandra-batch-loading-without-the-batch-the-nuanced-edition.html)_

Batches in Cassandra are often mistaken as a performance optimization. They can be but only in rare cases. First we need to discuss the different types of batches:

## Unlogged Batch

A good example of an unlogged batch follows and assumes a partition key of date. The following batch is effectively one insert because all inserts are sharing the same partition key. Assuming a partition key of date the above batch will only resolve to one write internally, no matter how many there are as long as they have the same date value. This is therefore the primary use case of an unlogged batch:

```sql
BEGIN BATCH; 
UPDATE users SET name='Jim' where id =1; 
UPDATE users_by_ssn set name='Jim' where ssn='888–99–9999'; 
APPLY BATCH;
```

A common anti pattern I see is:

```sql
-—NEVER EVER EVER DO 
BEGIN UNLOGGED BATCH;
INSERT INTO tester.users (userID, firstName, lastName) VALUES (1, 'Jim', 'James') 
INSERT INTO tester.users (userID, firstName, lastName) VALUES (2, 'Ernie', 'Orosco') 
INSERT INTO tester.users (userID, firstName, lastName) VALUES (3, 'Jose', 'Garza') 
INSERT INTO tester.users (userID, firstName, lastName) VALUES (4, 'Sammy', 'Mason') 
INSERT INTO tester.users (userID, firstName, lastName) VALUES (5, 'Larry', 'Bird') 
INSERT INTO tester.users (userID, firstName, lastName) VALUES (6, 'Jim', 'Smith') 
APPLY BATCH; 
```

Unlogged batches require the coordinator to do all the work of managing these inserts, and will make a single node do more work. Worse if the partition keys are owned by other nodes then the coordinator node has an extra network hop to manage as well. The data is not delivered in the most efficient path.

## Logged Batch (aka atomic)

A good example of a logged batch looks something like:

```sql
BEGIN BATCH; 
UPDATE users SET name='Jim' where id =1; 
UPDATE users_by_ssn set name='Jim' where ssn='888–99–9999'; 
APPLY BATCH;
```

This is keeps tables in sync, but at the cost of performance. A common anti pattern I see is:

```sql
-—NEVER EVER EVER DO 
BEGIN BATCH; 
INSERT INTO tester.users (userID, firstName, lastName) VALUES (1, 'Jim', 'James') 
INSERT INTO tester.users (userID, firstName, lastName) VALUES (2, 'Ernie', 'Orosco') 
INSERT INTO tester.users (userID, firstName, lastName) VALUES (3, 'Jose', 'Garza') 
INSERT INTO tester.users (userID, firstName, lastName) VALUES (4, 'Sammy', 'Mason') 
INSERT INTO tester.users (userID, firstName, lastName) VALUES (5, 'Larry', 'Bird') 
INSERT INTO tester.users (userID, firstName, lastName) VALUES (6, 'Jim', 'Smith') 
APPLY BATCH; 
```

This ends up being expensive for the following reasons. Logged batches add a fair amount of work to the coordinator. However it has an important role in maintaining consistency between tables. When a batch is sent out to a coordinator node, two other nodes are sent batch logs, so that if that coordinator fails then the batch will be retried by both nodes.

This obviously puts a fair a amount of work on the coordinator node and cluster as a whole. Therefore the primary use case of a logged batch is when you need to keep tables in sync with one another, and NOT performance.

## Fastest option no batch

I’m sure about now you’re wondering what the fastest way to load data is, allow the distributed nature of Cassandra to work for you and distribute the writes to the optimal destination. The following code will lead to not only the fastest loads (assuming different partitions are being updated), but it’ll cause the least load on the cluster. If you add retry logic you’ll only retry that one mutation while the rest are fired off.

For code samples go [read the article I mentioned above.](https://blog.foundev.pro/2016/04/29/cassandra-batch-loading-without-the-batch-the-nuanced-edition.html)
