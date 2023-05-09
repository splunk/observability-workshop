---
title: Getting Started with O11y GDI - Real Time Enrichment Workshop
linkTitle: 1. Getting Started
weight: 1
---

Please note to begin the following lab, you must have completed the prework:

- Obtain a Splunk Observability Cloud access key
- Understand cli commands

Follow these steps if using O11y Workshop EC2 instances

## 1. Verify yelp data files are present

``` bash
ll /var/appdata/yelp*
```

## 2. Export the following variables

``` bash
export ACCESS_TOKEN=<your-access-token>
export REALM=<your-o11y-cloud-realm>
export clusterName=<your-k8s-cluster>
```

## 3. Clone the following repo

``` bash
cd /home/ubuntu 
git clone https://github.com/leungsteve/realtime_enrichment.git 
cd realtime_enrichment/workshop 
python3 -m venv rtapp-workshop 
source rtapp-workshop/bin/activate
```
