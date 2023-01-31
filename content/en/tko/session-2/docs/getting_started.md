---
title: GDI - Real Time Enrichment Workshop
linkTitle: Getting started
weight: 2
---

Please note to begin the following lab, you must have completed the prework:

- Obtain a Splunk Observability Cloud access key
- Obtained a docker hub username
- Understand cli commands
- Be able to [Clone this repository](https://github.com/leungsteve/realtime_enrichment)

Follow these steps if using O11y Workshop EC2 instances

``` bash
# note: verify yelp data files are present
ll /var/appdata/yelp*

export SPLUNK_ACCESS_TOKEN=<your access token>
export SPLUNK_REALM=<your realm>
export ACCESS_TOKEN=<your access token>
export REALM=<your realm>
export clusterName=<your-cluster>


git clone https://github.com/leungsteve/realtime_enrichment.git
cd realtime_enrichment/workshop
python3 -m venv rtapp-workshop
source rtapp-workshop/bin/activate
```
