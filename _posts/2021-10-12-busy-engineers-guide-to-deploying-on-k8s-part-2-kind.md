---
title: Busy Engineers Guide to Deploying on K8s Part 2 - Kind
date: 2021-10-12T01:00:00+00:00
author: Ryan Svihla
layout: post
tags: [ kubernetes, github, docker ]
---

Post Valid as of October 12, 2021.

### Busy Engineer's Guide to Deploying On K8s

* [Part 1 - GitHub Packages](/2021/10/12/busy-engineers-guide-to-deploying-on-k8s-part-1-github-packages.html)
* [Part 2 - Kind (this post)](/2021/10/12/busy-engineers-guide-to-deploying-on-k8s-part-2-kind.html)
* [Part 3 - Helm](/2021/10/12/busy-engineers-guide-to-deploying-on-k8s-part-3-helm.html)

This is a continuation from the [last post in the series](/2021/10/12/busy-engineers-guide-to-deploying-on-k8s-part-1-github-packages.html). There are three primary ways
to run Kubernetes locally on a notebook: [Kind](https://kind.sigs.k8s.io), [k3d](https://k3d.io/v5.0.0/), and [Minikube](https://github.com/kubernetes/minikube). I personally far prefer k3d due to it having good defaults to get
up and running with stateful sets long before the other two and it can create large worker nodes, these have lead to a loyalty to the product. However, my org seems to have standardized on Kind for most of their CI so I will be covering
that here as it is the easiest for my coworkers to find help and documentation. It is also an excellent product to get started with Kubernetes.

## Install Kind Mac and Linux

* Assuming you followed the last guide we will use Homebrew again install kubernetes cli `brew install kubernetes-cli`
* Install kind `brew install kind`
* Then create a cluster `kind create cluster`
* To verify this is all working run `kubectl get nodes` where you should see on node

## Setup kind to access your GitHub credentials

* First make a GitHub token that has read:packages access [following the directions here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
* Next create a [Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/) where we can store our GitHub package credentials note (change the user to your GitHub user and password to match the token) `kubectl create secret docker-registry regcred --docker-server=ghcr.io --docker-username=<changeme> --docker-password=<changeme>`
* create a Kubernetes deployment to access your image and get it running (change the image name to match your GitHub user name) with the following `deployment.yaml` file
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nodejs-deployment
spec:
  selector:
    matchLabels:
      app: nodejs
  replicas: 2 # tells deployment to run 2 pods matching the template
  template:
    metadata:
      labels:
        app: nodejs
    spec:
      imagePullSecrets:
      - name: regcred
      containers:
      - name: nodejs
        image: ghcr.io/CHANGEME/app:main
        imagePullPolicy: Always
        ports:
        - containerPort: 3000
```
* install the deployment `kubectl create -f deployment.yaml`
* check on it's progress with `kubectl get pods --watch`
<img title="kubectl get pods" src="/assets/kubectlgetpods.png" border="0" alt="kubectl get pods" />
* when your nodes are running you can port-forward `kubectl port-forward $( kubectl get pods  -o name | head -n 1) 3000:3000`
* open your web browser to http://localhost:3000
<img title="express.png" src="/assets/express.png" border="0" alt="express" />

### What did we do

* We installed the kubectl cli
* We installed kind
* Created a GitHub token with read rights to our new package
* Created a deployment in Kubernetes that deployed the newly pushed package to our local kind instance
* Used kubectl to make the deployment visible and opened it in a browser

Follow the [next steps here](2021/10/12/busy-engineers-guide-to-deploying-on-k8s-part-3-helm.html)
