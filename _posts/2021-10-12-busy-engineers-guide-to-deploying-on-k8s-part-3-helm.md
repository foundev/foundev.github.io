---
title: Busy Engineers Guide to Deploying on K8s Part 3 - Helm
date: 2021-10-12T02:00:00+00:00
author: Ryan Svihla
layout: post
tags: [ kubernetes, github, docker, helm ]
---

Post Valid as of October 12, 2021.

### Busy Engineer's Guide to Deploying On K8s

* [Part 1 - GitHub Packages](/2021/10/12/busy-engineers-guide-to-deploying-on-k8s-part-1-github-packages.html)
* [Part 2 - Kind ](/2021/10/12/busy-engineers-guide-to-deploying-on-k8s-part-2-kind.html)
* [Part 3 - Helm (this post)](/2021/10/12/busy-engineers-guide-to-deploying-on-k8s-part-3-helm.html)

Ok so now that you have Kubernetes installing in a deployment and you can see it with kubectl port-forward how to you get beyond the
toy stage?

## Helm Charts

[Helm](helm.sh) is a great way to make your app "production ready" on Kubernetes with minimal effort assuming you do not try to overthink your deployment.
Helm fundamentally provides a way for us to deploy apps to kubernetes by easily changing a handful of values at deployment time or in something called a values.yaml

A helm "chart" is a series of kubernetes yaml templates with a values.yaml file providing you default values for your deployment. Do the following to get a basic one up and running

* Install helm `brew install helm`
* In your top level repository directory run `mkdir charts`
* Go to the charts folder `cd charts`
* Create your help chart `helm create myapp`
* Go to the new chart folder `cd myapp`
* Edit the values.yaml file with the following changes:
  * change image.tag from "" to "main"
  * change image.pullPolicy from IfNotPresent to Always
  * change image.repository from nginx to ghcri.io/<YOUR REPO>/app
  * Update the imagePullSecrets to use the regcred secret from the last post. Therefore, remove the [] for imagePullSecrets and below it add -name: regcred
  * Updated service.port from 80 to 3000

```yaml
# Default values for myapp.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

replicaCount: 1

image:
  repository: nginx
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: "main"

imagePullSecrets:
- name: regcred
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  # Specifies whether a service account should be created
  create: true
  # Annotations to add to the service account
  annotations: {}
  # The name of the service account to use.
  # If not set and create is true, a name is generated using the fullname template
  name: ""

podAnnotations: {}

podSecurityContext: {}
  # fsGroup: 2000

securityContext: {}
  # capabilities:
  #   drop:
  #   - ALL
  # readOnlyRootFilesystem: true
  # runAsNonRoot: true
  # runAsUser: 1000

service:
  type: ClusterIP
  port: 3000

ingress:
  enabled: false
  className: ""
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []
  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local

resources: {}
  # We usually recommend not to specify default resources and to leave this as a conscious
  # choice for the user. This also increases chances charts run on environments with little
  # resources, such as Minikube. If you do want to specify resources, uncomment the following
  # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
  # limits:
  #   cpu: 100m
  #   memory: 128Mi
  # requests:
  #   cpu: 100m
  #   memory: 128Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
  # targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}
```

* edit myapp/templates/deployment.yaml to use port 3000 instead of 80 for the containerPort

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "myapp.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 3000
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /
              port: http
          readinessProbe:
            httpGet:
              path: /
              port: http
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

* Install the app to your k8s cluster with helm `helm install mydeploy myapp`
* Test the access running the following commands
  * get pod name `export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=myapp,app.kubernetes.io/instance=mydeploy" -o jsonpath="{.items[0].metadata.name}")`
  * get container port `export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")`
  * port forward `kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT`
  * go to http://127.0.0.0:8080 in your browser

### Ingress

Ok so this portfoward stuff is great and all but not super impressive

* Tear down kind 
* create a new cluster with the following command to enable ingress
```sh
cat <<EOF | kind create cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
EOF
```
* don't forget to reinstall your GitHub Packages secrets 
 user and password to match the token) `kubectl create secret docker-registry regcred --docker-server=ghcr.io --docker-username=<changeme> --docker-password=<changeme>`
* install nginx ingress `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml`
* wait a couple of minutes
* edit the values.yaml now to the following values (there is a mountain to go over here so just copy and paste it)

```yaml
ingress:
  enabled: true
  className: ""
  annotations:
    # allows nginx to rewrite urls to keep everything happy
    nginx.ingress.kubernetes.io/rewrite-target: /$1
  hosts:
    - host: localhost # set localhost since that is how we will be accessing it
      paths:
        - path: /app/?(.*) #needed to allow node to be ok with this /app path
          pathType: Prefix # defines our strategy to be prefix instead of whatever default is on various platforms
  tls: []
```
* Assuming you are still in the charts folder upgrade your deployment `helm upgrade mydeploy myapp`
* navigate to http://localhost/app you should now see your express app exposed through http://localhost/app
<img title="express_80.png" src="/assets/express_80.png" border="0" alt="express_80" />

## Recap

* We installed helm
* We created a helm chart
* We setup kind to support ingress
* We installed the ingress-nginx controller
* We setup ingress to work through localhost and reroute /app to our newly deploy app
