# Creating a Spark cluster with Cass Operator

This is not officially supported as of June 8, 2021 but I am including it anyway since it is not obvious and documented anywhere. There are cases where for some POC or simple
thing you want to test out in development this maybe a desirable thing to have handy (I use it to run clusters on my notebook).

First install the cass-operator by running the following [helm commands](https://helm.sh/docs/intro/install/)

```bash
helm repo add datastax https://datastax.github.io/charts
helm repo update
helm install cass-operator datastax/cass-operator -n dse-clusters --create-namespace
```

Wait for the cass-operator to come up, you can see it by running the following command which you should repeat until you get a running status

```bash
%kubectl get pods -n dse-clusters
NAME                             READY   STATUS    RESTARTS   AGE
cass-operator-6d8d7cd8db-4nr85   1/1     Running   0          17s
```

Once you have done that you can run the following yaml (adjust for your desired cluster size and available resources)

```yaml
apiVersion: cassandra.datastax.com/v1beta1
kind: CassandraDatacenter
metadata:
  name: dc1
spec:
  clusterName: cluster1
  serverType: dse
  serverVersion: "6.8.12"
  dseWorkloads:
    analyticsEnabled: true #key thing to add
  managementApiAuth:
    insecure: {}
  size: 2 
  storageConfig:
      cassandraDataVolumeClaimSpec:
        storageClassName: server-storage
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 20Gi
  resources:
    requests:
      memory: 6Gi
      cpu: 3000m
    limits:
      memory: 6Gi
      cpu: 3000m
  racks:
    - name: r1
  config:
    jvm-server-options:
      initial_heap_size: "4000m" #you want to set heap size or you will have issues with auto detection on kubernetes
      max_heap_size: "4000m"
    cassandra-yaml:
      num_tokens: 8 # balances the cluster
      allocate_tokens_for_local_replication_factor: 2 # balances the cluster, should be 3 if RF is expected to be 3
      file_cache_size_in_mb: 256
```

Using the yaml above run the following command.

```bash
kubectl create -f spark.yaml -n dse-clusters
```
