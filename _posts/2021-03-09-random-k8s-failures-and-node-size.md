---
title: Random Kubernetes Failures and Node Size
tags: [ kubernetes ]
---
I had a report of ingress failing on traefik randomly during a test job and since it worked on a local workstation the belief was it had to be a problem with traefik. I looked at the logs and asked them to spin up bigger nodes for the test and it fixed things.

The reason the beefier machines come into play are varied but ultimately come down to "no free lunch". It all started with these log entries in traefik:

`Error while setting deadline: set tcp 10.244.3.2:44070: use of closed network connection`

* The log turns out to be a pretty generic "nope there is nothing to use in this network connection, giving up" and happens if I just use the wrong username and password (read any reason)
* Kubernetes master nodes needs scale up the more nodes you add, if the master node is under strain the all sorts of random things start to break (just from experience) this fits "random"
* KIND is intentionally running a very stripped down K8s compared to vanilla K8s (generally true of all Kubernetes distributions compared to the laptop optimised kind)
* The project in question was a pretty big deployment, and is just going to put a lot of strain on the nodes.
* Pretty sure (though not proven) Flannel routing across a network needs more resources than [whatever local interface magic KIND is doing](https://kind.sigs.k8s.io/docs/user/configuration/#disable-default-cni).
* To tie in with the previous points, these K8s nodes only had 2 cores and were running very slow CPUs. While [a 5 node cluster only gets a m3.medium on EKS](https://learnk8s.io/kubernetes-node-size) these nodes are probably slower still.
* Finally most of the devs running KIND on this project had notebooks faster with more cores than the whole K8s cluster so KIND was getting more juice.

So anytime there are intermittent failures node size maybe the culprit (Not a bad idea to check if there is expensive work scheduled on the master)

Final pro tip (note you need to change the namespace in 2 places)

```kubectl port-forward $(kubectl get pods --selector "app.kubernetes.io/name=traefik" --output=name) 9000:9000```

will open up a port for you to browse traefik and make sure it is configured correctly and everything is happy, just browse to http://127.0.0.1:9000/dashboard/#/ and enjoy

