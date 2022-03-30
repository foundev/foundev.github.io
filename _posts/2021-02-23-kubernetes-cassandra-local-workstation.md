---
layout: post
tags: [cassandra, kubernetes]
---
<h1>Getting the DataStax cass-operator working on Mac</h1>

Just leaving this here for anyone coming back to this later. This works as of Feb 23 2021 on Big Sur

* install docker desktop https://www.docker.com/products/docker-desktop
* install k3d https://github.com/rancher/k3d#get you can just run `curl -s https://raw.githubusercontent.com/rancher/k3d/main/install.sh | bash`
* create cluster: `k3d cluster create`
* install operator manifest `kubectl create -f https://raw.githubusercontent.com/datastax/cass-operator/v1.5.1/docs/user/cass-operator-manifests-v1.19.yaml`
* download a cassandra data center yaml `curl -O https://gist.githubusercontent.com/rsds143/0e9263ed4287d888fab36eb3e4aec502/raw/f919172c64452a2277b7523d680a9e12916d0d39/cassandra-dc.yaml`
* run `kubectl create -f cassandra-dc.yaml --namespace cass-operator`
* wait for cassandra to come up `kubectl logs cluster1-dc1-default-sts-0 --namespace cass-operator server-system-logger`
* get username `export CQLUSER=$(kubectl get secret cluster1-superuser -o json -n cass-operator | grep \"username\"  | sed -E 's/\"(.+)\": \"(.+)\"/\2/' | base64 -d)`
* get password `export CQLPASS=$(kubectl get secret cluster1-superuser -o json -n cass-operator | grep \"password\"  | sed -E 's/\"(.+)\": \"(.+)\"/\2/' | sed -E 's/,*$//g' | base64 -d )`
* log into cqlsh `kubectl exec -it -n cass-operator cluster1-dc1-default-sts-0 -- cqlsh -u $CQLUSER -p $CQLPASS`
* enjoy your cassandra cluster

The yaml I have linked too above is here

```yaml
apiVersion: cassandra.datastax.com/v1beta1
kind: CassandraDatacenter
metadata:
  name: dc1
spec:
  clusterName: cluster1
  serverType: cassandra
  serverVersion: 3.11.7
  managementApiAuth:
    insecure: {}
  size: 1
  storageConfig:
    cassandraDataVolumeClaimSpec:
      storageClassName: local-path
      accessModes:
      - ReadWriteOnce
      resources:
        requests:
          storage: 5Gi
  config:
    cassandra-yaml:
      authenticator: org.apache.cassandra.auth.PasswordAuthenticator
      authorizer: org.apache.cassandra.auth.CassandraAuthorizer
      role_manager: org.apache.cassandra.auth.CassandraRoleManager
    jvm-options:
      initial_heap_size: 800M
      max_heap_size: 800M
```


I also wrote a quick script [here](https://gist.githubusercontent.com/rsds143/0e9263ed4287d888fab36eb3e4aec502/raw/40632aa794a8be8aa7acf17da0e35a3b47ebc04a/autostart_cassandra.sh)

sorry you can not run it with curl -s due to [this issue](https://github.com/kubernetes/kubernetes/issues/37471) or at least I haven't figured it out yet, but downloading it and running it works fine

```sh
#!/bin/bash
echo "installing k3d"
curl -s https://raw.githubusercontent.com/rancher/k3d/main/install.sh | bash
echo "creating k3d cluster"
k3d cluster create
echo "installing cassandra operator"
kubectl create -f https://raw.githubusercontent.com/datastax/cass-operator/v1.5.1/docs/user/cass-operator-manifests-v1.19.yaml
echo "installing cassandra data center"
curl -O https://gist.githubusercontent.com/rsds143/0e9263ed4287d888fab36eb3e4aec502/raw/f919172c64452a2277b7523d680a9e12916d0d39/cassandra-dc.yaml
kubectl create -f cassandra-dc.yaml --namespace cass-operator
echo "Sleeping for 120 seconds…"
sleep 120
echo "getting username and password"
echo "trying to login"
export CQLUSER=$(kubectl get secret cluster1-superuser -o json -n cass-operator | grep \"username\"  | sed -E 's/\"(.+)\": \"(.+)\"/\2/' | base64 -d)
export CQLPASS=$(kubectl get secret cluster1-superuser -o json -n cass-operator | grep \"password\"  | sed -E 's/\"(.+)\": \"(.+)\"/\2/' | sed -E 's/,*$//g' | base64 -d )
kshell() {
kubectl exec -it -n cass-operator cluster1-dc1-default-sts-0 -- cqlsh -u $CQLUSER -p $CQLPASS
}
kshell
```
