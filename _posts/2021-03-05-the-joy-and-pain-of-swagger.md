---
layout: post
title: The Joy and Pain of Swagger
tags: [swagger, api]
---

I have had to use [Swagger](https://swagger.io) for many a project since my first introduction to it while working for an ecommerce site in 2015. I did like being able to
easily convert documentation into viewable API docs complete with executable examples and forms ready to go that let me actually try out my new API. In many ways it is the closest
to the promise of API first development.

## Code Generation

However, the generation of code with it can be pretty grim, and the trick to gettting the code generated that you want from the spec is challenging to say the least.
Let us take a look at some of the go code I had generated for the [Astra DevOps API](https://docs.datastax.com/en/astra/docs/_attachments/devopsv1.html)


### How to generate

Easiest way I have found is through Docker.

* Download swagger.json (or just find the URL)
* create a directory next to where you downloaded the swagger.json file `mkdir goclient` 
* run the following command from the folder you downloaded 
```sh
docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli-v3 generate -v \
    -i /local/swagger.json \
    -l go \
    -o /local/goclient
```
This generates something that looks pretty good from a glance, but there are lots of files.

<img width="332" alt="generated_files" src="https://user-images.githubusercontent.com/43972/110086267-71085200-7d92-11eb-8d04-1429a3c9084f.png">


## Problems

### The initial client

If you look at the client which there are [no timeouts set by default](https://medium.com/@nate510/don-t-use-go-s-default-http-client-4804cb19f779) . Now this is a decision that I get and it is a relatively sane one, but for new to Go folks this is a common issue.
At least we can override it. Also, the API makes liberaly use of contexts as [per Google's suggestion](https://blog.golang.org/context) which allows us to set timeouts per request.

```go
/ NewAPIClient creates a new API client. Requires a userAgent string describing your application.
// optionally a custom http.Client to allow for advanced features such as caching.
func NewAPIClient(cfg *Configuration) *APIClient {
    if cfg.HTTPClient == nil {
        cfg.HTTPClient = http.DefaultClient # this is a bad default, but at least you can override it
    }
    c := &APIClient{}
    c.cfg = cfg
    c.common.client = c
    // API Services
    c.OperationsApi = (*OperationsApiService)(&c.common)
    c.PublicApi = (*PublicApiService)(&c.common)
    return c
}
```

### Silly structs and hard to use arguments

My least favorite behavior I see from generated swagger and I have seen this across a number of clients in other languages. Here is a type that is created for an integer argument.

```go
// CapacityUnits is used to horizontally scale a database.
type CapacityUnits struct {
    // CapacityUnits an be increased by a max of three additional capacity units per operation. Reducing capacity units is not supported at this time
    CapacityUnits int32 `json:"capacityUnits,omitempty"`
}
```

Now I think I know why this happened, I believe it is an optional argument somewhere in the API but this is ugly. I would rather have two methods than to have to instantiate a struct
when all I want to do is pass in an int32

### Generated docs never seem to be what you want

This a few things going on I don't prefer:

* The comment style is in /* form instead of the typical // you wee with go docs
* OperationsApiService is the name of the type this function is attached to and is not actually the correct annotation for this. It should be AddKeyspace
* The return types are missing because they're too generic. I will admit this is a taste thing.

```go
/*
OperationsApiService Adds keyspace into database
Adds the specified keyspace to the database
 * @param ctx context.Context - for authentication, logging, cancellation, deadlines, tracing, etc. Passed from http.Request or context.Background().
 * @param databaseID String representation of the database ID
 * @param keyspaceName Name of database keyspace

*/
func (a *OperationsApiService) AddKeyspace(ctx context.Context, databaseID string, keyspaceName string) (*http.Response, error) {
```

### The spec can be very complicated

During one project this past year [I spent an enourmous amount of time trying to get swagger to generate documentation in the correct places](https://github.com/rsds143/stargate/blob/f9a0d3035645fe88d1a646bc03ef9969158d2c58/src/main/scala/stargate/service/Namespaces.scala#L94-L270), I ended up trying a half dozen similarly named fields just to
get examples to prepopulate correctly, and one field would work for one type of data and not another.

In the end most of them unded up working under some combination of type/description/content/mediaType/schema, but there many other locations for example that just never showed up in the UI for some types:

```
.addParametersItem(new QueryParameter()
            .name("payload")
            .required(true)
          .description("query payload")
            .content(new Content()
              .addMediaType("application/json", new MediaType()
                .schema(new Schema().`type`("string").example(getSample)))
          )))
```

## Closing

Now even with all the problems I don't think I could do better and it is a great service and overall a great product. I typically use it as a starting point for my code
and then promply rewrite the bits I don't like very much. However, I think it is helpful for
