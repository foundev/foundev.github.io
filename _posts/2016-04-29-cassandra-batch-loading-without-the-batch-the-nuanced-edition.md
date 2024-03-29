---
date: 2016-04-29T16:03:56+00:00
author: Ryan Svihla
layout: post
tags: [Cassandra, Java]
---
<h1>Cassandra - Batch Loading Without the Batch The Nuanced Edition</h1>
  My [previous post on this subject](https://blog.foundev.pro/2014/08/28/cassandra-batch-loading-without-the-batch-keyword.html) has proven extraordinarily popular and I get commentary on it all the time, most of it quite good. It has however, gotten a decent number of comments from people quibbling with the nuance of the post and pointing out it’s failings, which is fair because I didn’t explicitly spell this out as a “framework of thinking” blog post or a series of principles to consider. This is the tension between making something approachable and understandable to the new user but still technically correct for the advanced one. Because of where Cassandra was at the time and the user base I was encountering day to day, I took the approach of simplification for the sake of understanding. However, now I think is a good time to write this up with all the complexity and detail of a production implementation and the tradeoffs to consider.

### _TLDR_

  1. _Find the ideal write size it can make a 10x difference in perf (10k-100k is common)._
  2. _Limit threads in flight when writing._
  3. _Use tokenaware unlogged batches if you need to get to your ideal size._

_Details on all this below._

# You cannot escape physics

  Ok it’s not really physics, but it’s a good word to use to get people to understand you have to consider your hard constraints and that wishing them away or pretending they’re not there will not save you from their factual nature. So now lets talk about some of the constraints that will influence your optimum throughput strategy.

  <img src="https://cdn-images-1.medium.com/max/1600/0*_JADLLa1R1Noa6Gw.jpg" alt="large writes hurt" data-image-id="0*_JADLLa1R1Noa6Gw.jpg" data-external-src="http://i.imgur.com/7YloSab.jpg" /><span style="font-size: 16px;">Now that the clarification is out of the way. Something the previous batch post neglected to mention was the size of your writes can change these tradeoffs a lot, back in 2.0 I worked with Brian Hess of DataStax on figuring this out in detail (he did most of the work, I took most of the credit). And what we found with the hardware we had at the time was total THROUGHPUT in megabytes changed by an order of magnitude depending on the size of each write. So in the case of 10mb writes, total throughput plummeted to an embarrassing slow level nearly 10x.</span>

<img src="https://cdn-images-1.medium.com/max/1600/0*DZevfAvMS0Pl9tnr.jpg" alt="small writes hurt" data-image-id="0*DZevfAvMS0Pl9tnr.jpg" data-external-src="http://i.imgur.com/XYNoQTg.jpg" />

<span style="font-size: 16px;">Using the same benchmarks tiny writes still managed to hurt a lot and 1k writes were 9x less throughput than 10–100k writes. This number will vary depending on A LOT of factors in your cluster but it tells you the type of things you should be looking at if you’re wanting to optimize throughput.</span>

<img src="https://cdn-images-1.medium.com/max/1600/0*tmKbJfaYo4_feKy_.jpg" alt="bottlenecks" data-image-id="0*tmKbJfaYo4_feKy_.jpg" data-external-src="http://i.imgur.com/zoP29qM.jpg" />

  Can your network handle 100 of your 100mb writes? Can your disk? Can your memory? Can your client? Pay attention to whatever gets pegged during load and that should drive the size of your writes and your strategy for using unlogged batches or not.

### RECORD COUNT BARELY MATTERS

  I’m dovetailing here with the previous statement a bit and starting with something inflammatory to get your attention. But this is often the metric I see people use and it’s at best accidentally accurate.

  I’ve had some very smart people tell me "100 row unlogged batches that are token aware are the best". Are those 100 rows all 1GB a piece? or are they all 1 byte a piece?

# Your blog was wrong!

  I had many people smarter than I tell me my “post was wrong” because they were getting awesome performance by ignoring it. None of this is surprising. In some of those cases they were still missing the key component of what matters, in other cases rightly poking holes in the lack of nuance in my previous blog post on this subject (I never clarified it was intentionally simplistic).

<img src="https://cdn-images-1.medium.com/max/1600/0*-fdAtLLPFkuqpB55.jpg" alt="wrong - client death" data-image-id="0*-fdAtLLPFkuqpB55.jpg" data-external-src="http://i.imgur.com/gaA9z4K.jpg" />

I intentionally left out code to limit threads in flight. Many people new to Cassandra are often new to distributed programming and consequentially multi-threaded programming. I was in this world myself for a long time. Your database, your web framework and all of your client code do everything they can to hide threads from you and often will give you nice fat thread safe objects to work with. Not everyone in computer science has the same background and experience, and the folks in traditional batch jobs programming which is common in insurance and finance where I started do not have the same experience as folks working with distributed real time systems.

  In retrospect I think this was a mistake and I ran into a large number of users that did copy and paste my example code from the previous blog post and ran into issues with clients exhausting resources. So here is an updated example using the DataStax Java driver that will allow you to adjust thread levels easily and tweak the amount of threads in flight:


#### Using classic manual manipulation of futures

Works with Java Driver version 2.1–3.x:

```java
/**
 * I HAVE NOT BEEN FULLY TESTED DO NOT USE ME IN PRODUCTION CODE THERE ARE NO WARRANTIES
 * This is with using the approach in the previous blog post
 */ 
public class BulkLoader {

  private final int threads;
  private final String[] contactHosts;

  public BulkLoader(int threads, String...contactHosts){
    this.threads = threads;
    this.contactHosts = contactHosts;
  }

  public void ingest(Iterator<Object[]> boundItemsIterator, String insertCQL) throws InterruptedException {
    Cluster cluster = Cluster.builder()
            .addContactPoints(contactHosts)
            .build();
    Session session = cluster.newSession();
    //there are better ways to do this using executor pools
    List<ResultSetFuture> futures = new ArrayList<>();
    final PreparedStatement statement = session.prepare(insertCQL);
    int count = 0;
    while (boundItemsIterator.hasNext()) {
      BoundStatement boundStatement = statement.bind(boundItemsIterator.next());
      ResultSetFuture future = session.executeAsync(boundStatement);
      futures.add(future);
      count++;
      if(count % threads==0){
        futures.forEach(ResultSetFuture::getUninterruptibly);
        futures = new ArrayList<>();
      }
    }
    session.close();
    cluster.close();
  }

  public static void main(String[] args) throws InterruptedException {
    Iterator<Object[]> rows = new Iterator<Object[]>() {
      int i = 0;
      Random random = new Random();

      @Override
      public boolean hasNext() {
        return i!=100000;
      }

      @Override
      public Object[] next() {
        i++;
        return new Object[]{i, String.valueOf(random.nextLong())};
      }
    };

    System.out.println("Starting benchmark");
    Stopwatch watch = Stopwatch.createStarted();
    new BulkLoader(8, "127.0.0.1").ingest(rows,
          "INSERT INTO my_test.rows (id, value) VALUES (?,?)");
    System.out.println("total time seconds = " + watch.elapsed(TimeUnit.SECONDS));
    watch.stop();
  }
}
```

#### This is with a fixed thread pool and callbacks

Works with Java Driver version 2.1–3.x:

```java
/**
 * I HAVE NOT BEEN FULLY TESTED DO NOT USE ME IN PRODUCTION CODE THERE ARE NO WARRANTIES
 */ 
public class BulkLoader {

  private final int threads;
  private final String[] contactHosts;

  public BulkLoader(int threads, String...contactHosts){
    this.threads = threads;
    this.contactHosts = contactHosts;
  }

  //callback class
  public static class IngestCallback implements FutureCallback<ResultSet>{

    @Override
    public void onSuccess(ResultSet result) {
      //placeholder: put any logging or on success logic here.
    }

    @Override
    public void onFailure(Throwable t) {
      //go ahead and wrap in a runtime exception for this case, but you can do logging or start counting errors.
      throw new RuntimeException(t);
    }
  }

  public void ingest(Iterator<Object[]> boundItemsIterator, String insertCQL) throws InterruptedException {
    Cluster cluster = Cluster.builder()
            .addContactPoints(contactHosts)
            .build();
    Session session = cluster.newSession();
    //fixed thread pool that closes on app exit
    ExecutorService executor = MoreExecutors.getExitingExecutorService(
            (ThreadPoolExecutor)Executors.newFixedThreadPool(threads));
    final PreparedStatement statement = session.prepare(insertCQL);
    while (boundItemsIterator.hasNext()) {
      BoundStatement boundStatement = statement.bind(boundItemsIterator.next());
      ResultSetFuture future = session.executeAsync(boundStatement);
      Futures.addCallback(future, new IngestCallback(), executor);
    }
    executor.shutdown();
    try {
      executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
    } catch (InterruptedException e) { 
      //dosomething
    }
    session.close();
    cluster.close();
  }

  public static void main(String[] args) throws InterruptedException {
    Iterator<Object[]> rows = new Iterator<Object[]>() {
        int i = 0;
        Random random = new Random();

        @Override
        public boolean hasNext() {
          return i!=1000000;
        }

        @Override
        public Object[] next() {
          i++;
          return new Object[]{i, String.valueOf(random.nextLong())};
        }
    };

    System.out.println("Starting benchmark");
    Stopwatch watch = Stopwatch.createStarted();
    new BulkLoader(8, "127.0.0.1").ingest(rows,
            "INSERT INTO my_test.rows (id, value) VALUES (?,?)");
    System.out.println("total time seconds = " + watch.elapsed(TimeUnit.SECONDS));
    watch.stop();
    System.exit(0);
  }
}
```

  Either approach works as well as the other. Your preference should fit your background.

  <img src="https://cdn-images-1.medium.com/max/1600/0*oD6iAaOa31e2FMlf.jpg" alt="wrong - token aware batches" data-image-id="0*oD6iAaOa31e2FMlf.jpg" data-external-src="http://i.imgur.com/VrrnQnQ.jpg" />

  <span style="font-size: 16px;">Sure tokenaware unlogged batches that act like big writes, and really match up with my advice on unlogged batches and partition keys. If you can find a way to have all of your batch writes go to the correct node and use a routing key to do so then yes of course one can get some nice perf boosts. If you are lucky enough to make it work well, trust that you have my blessing.</span>

  Anyway it is advanced code and I did not think it appropriate for a beginner level blog post. I will later dedicate an entire blog post just to this.

## Conclusion

  I hope you found the additional nuance useful and maybe this can help some of you push even faster once all of these tradeoffs are taken into account. But I hope you take away my primary lesson: Distributed databases often require you to apply distributed principles to get the best experience out of them. Doing things the way we’re used to may lead to surprising results.
