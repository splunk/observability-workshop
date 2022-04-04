---
title: APM
weight: 5
---

### Enable Modular Input for APM error rate and APM thruput

### Enable the Splunk APM Services

Enable APM Service (4 service to enable)

1. Application Duration
2. Application Error Rate
3. Application Performance Monitoring
4. Application Rate (Throughput)

### Enable Cloud Entity Search for APM  

Go to Settings -> Searches, Reports, and Alerts  

Select App Splunk Observability Cloud | Owner All  
Find the line ITSI Import Objects - Splunk-APM Application Entity Search -> (Actions) Edit -> Enable  
NOTE those searches are called Cloud Entity Searches  
Open ITSI ->  Infrastructure Overview  
Verify that you have your entities are showing up
Note: there isn't any out of the box Key vital metrics so the visualisation will look like this

![Splunk APM](../..//images/custom_service/SplunkAPM.png)

### Task 4.5: Add a dashboard Navigation

* Configuration -> Entity management -> Entity Types
* Find SplunkAPM -> Edit
* Open Navigations type
* Navigation Name: Traces View
* URL : <https://app.${sf_realm}.signalfx.com/#/apm/traces>
* Save navigation!!
* Save Entity type

In Service Analyzer open a Splunk APM entity and test your new navigation suggestion

![Navigation Suggestion](../../images/custom_service/navigation_suggestion.png)

### Add Key Vital metrics for Splunk APM

Configuration -> Entity management -> Entity Types
Find SplunkAPM -> Edit
Open Vital Metrics
Enter a name
Add a metric
Enter the search below and click run search

```splunk
| mstats avg(*) span=5m WHERE "index"="sim_metrics" AND sf_streamLabel="thruput_avg_rate" GROUPBY sf_service sf_environment | rename avg(service.request.count) as "val"
```

Entity matching field sf_service  
(note: verify that you are matching entities 10 entities matched in last hour)  
Unit of Display Percent (%)  
Choose a Key Metric Select Application Rate Thruput  
Save Application Rate  
Save Entity Type  

Your UI should look like this should look like this:

![Vital Metric](../../images/custom_service/vital_metric.png)
