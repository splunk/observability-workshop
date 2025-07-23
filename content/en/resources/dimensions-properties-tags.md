---
title: Dimension, Properties and Tags
weight: 3
description: One conversation that frequently comes up is Dimensions vs Properties and when you should use one verus the other. 
draft: false
---

## Applying context to your metrics

One conversation that frequently comes up is Dimensions vs Properties and when you should use one verus the other. Instead of starting off with their descriptions it makes sense to understand how we use them and how they are similar, before diving into their differences and examples of why you would use one or the other.

## How are Dimensions and Properties similar?

The simplest answer is that they are both metadata `key:value` pairs that add context to our metrics. Metrics themselves are what we actually want to measure, whether it’s a standard infrastructure metric like​ ​`cpu.utilization` or a custom metric like number of API calls received.

If we receive a value of 50% for th​e ​`cpu.utilization` metric without knowing where it came from or any other context it is just a number and not useful to us. We would need at least to know what host it comes from.

These days it is likely we care more about the performance or utilization of a cluster or data center as a whole then that of an individual host and therefore more interested in things like the average `cpu.utilization` across a cluster of hosts, when a​ host’s `​cpu.utilization` is a outlier when compared to other hosts running the same service or maybe compare the ​average ​`cpu.utilization` of one environment to another.

To be able to slice, aggregate or g​roup our ​`cpu.utilization` metrics in this way we will need additional metad​ata for the `​cpu.utilization` metrics we receive to include what cluster a host belongs to, what service is running on the host and what environment it is a part of. This metadata can be in the form of either dimension or property `key:value` pairs.

For example, if I go to apply a filter to a dashboard or use the Group by function when running analytics, I can use a property or a dimension.

## So how are Dimensions and Properties different?

Dimensions are sent in with metrics at the time of ingest while properties are applied to metrics or dimensions after ingest. This means that any metadata you need to make a datapoint (​a single reported value of a metric) ​unique, like what host a value of `cpu.utilization` is coming from needs to be a dimension. Metric names + dimensions uniquely define an MTS (metric time series).

Example: the `​cpu.utilization` metric sent by a particular host (​server1) with a dimension `​host:server1` would be considered a unique time series. If you have 10 servers, each sending that metric, then you would have 10 time series, with each time series sharing the metric name `​cpu.utilization` and uniquely identified by the dimension key-value pair (​host:server1, host:server2...host:server10).

However, if your server names are only unique within a datacenter vs your whole environment you would need to add a 2n​d​ dimension `dc` for the datacenter location. You could now have double the number of possible MTSs. cpu.utilization metrics received would now be uniquely identified by 2 sets of dimension key-value pairs.

cpu.utilization plus ​dc:east &​ host:server1 would create a different time series then ​cpu.utilization plus dc:west & ​host:server1.

## Dimensions are immutable while properties are mutable

As we mentioned above, Metric name + dimensions make a unique MTS. Therefore, if the dimension value changes we will have a new unique combination of metric name + dimension value and create a new MTS.

Properties on the other hand are applied to metrics (or dimensions) after they are ingested. If you apply a property to a metric, it propagates and applies to all MTS that the metric is a part of. Or if you apply a property to a dimension, say ​host:server1 then all metrics from that host will have those properties attached. If you change the value of a property it will propagate and update the value of the property to all MTSs with that property attached. Why is this important? It means that if you care about the historical value of a property you need to make it a dimension.

Example: We are collecting custom metrics on our application. One metric is ​latency which counts the latency of requests made to our application. We have a dimension ​customer, so we can sort and compare latency by customer. We decide we want to track the ​application version as well so we can sort and compare our application ​latency by the version customers are using. We create a property ​version that we attach to the customer dimension. Initially all customers are using application version 1, so ​version:1.

We now have some customers using version 2 of our application, for those customers we update the property to ​version:2. When we update the value of the ​version property for those customers it will propagate down to all MTS for that customer. We lose the history that those customers at some point used ​version 1, so if we wanted to compare ​latency of ​version 1 and ​version 2 over a historical period we would not get accurate data. In this case even though we don’t need application ​version to make out metric time series unique we need to make ​version a dimension, because we care about the historical value.

## So when should something be a Property instead of a dimension?

The first reason would be if there is any metadata you want attached to metrics, but you don’t know it at the time of ingest.
The second reason is best practice is if it doesn’t need to be a dimension, make it a property. Why?
One reason is that today there is a limit of 5K MTSs per analytics job or chart rendering and the more dimensions you have the more MTS you will create. Properties are completely free-form and let you add as much information as you want or need to metrics or dimensions without adding to MTS counts.

As dimensions are sent in with every datapoint, the more dimensions you have the more data you send to us, which could mean higher costs to you if your cloud provider charges for data transfer.

A good example of some things that should be properties would be additional host information. You want to be able to see things like machine_type, processor, or os, but instead of making these things dimensions and sending them with every metric from a host you could make them properties and attach the properties to the host dimension.

Example where ​host:server1 you would set properties ​machine_type:ucs, processor:xeon-5560, os:rhel71. Anytime a metric comes in with the dimension ​host:server1 all the above properties will be applied to it automatically.

Some other examples of use cases for properties would be if you want to know who is the escalation contact for each service or SLA level for every customer. You do not need these items to make metrics uniquely identifiable and you don’t care about the historical values, so they can be properties. The properties could be added to the service dimension and customer dimensions and would then apply to all metrics and MTSs with those dimensions.

## What about Tags?

Tags are the 3r​d​ type of metadata that can be used to give context to or help organize your metrics. Unlike dimensions and properties, tags are NOT key:value pairs. ​Tags can be thought of as labels or keywords. Similar to Properties, Tags are applied to your data after ingest via the Catalog in the UI or programmatically via the API.​ Tags can be applied to Metrics, Dimensions or other objects such as Detectors.

## Where would I use Tags?

Tags are used when there is a need for a many-to-one relationship of tags to an object or a one-to-many relationship between the tag and the objects you are applying them to. They are useful for grouping together metrics that may not be intrinsically associated.

One example is you have hosts that run multiple applications. You can create tags (labels) for each application and then apply multiple tags to each host to label the applications that are running on it.

Example: Server1 runs 3 applications. You create tags ​app1, app2 and app3 and apply all 3 tags to the dimension ​host:server1

To expand on the example above let us say you also collect metrics from your applications.​ You could apply the tags you created to any metrics coming in from the applications themselves. You can filter based on a tag allowing you to filter based on an application, but get the full picture including both application and the relevant host metrics.

Example: App1 sends in metrics with the dimension ​service:application1. You would apply tag ​app1 to the dimension ​service:application1. You can then filter on the tag ​app1 in charts and dashboards.

Another use case for tags for binary states where there is just one possible value. An example is you do canary testing and when you do a canary deployment you want to be able to mark the hosts that received the new code, so you can easily identify their metrics and compare their performance to those hosts that did not receive the new code. There is no need for a key:value pair as there is just a single value “canary”.

Be aware that while you can filter on tags you cannot use the groupBy function on them. The groupBy function is run by supplying the key part of a key:value pair and the results are then grouped by values of that key pair.

## Additional information

For information on sending dimensions for custom metrics please review the ​Client Libraries documentation for your library of choice.

For information on how to apply properties & tags to metrics or dimensions via the API please see the API documentation for ​/metric/:name​ ​/dimension/:key/:value

For information on how to add or edit properties and tags via the Metadata Catalog in the UI please reference the section **​Add or edit metadata** in [Search the Metric Finder and Metadata catalog](https://docs.splunk.com/Observability/metrics-and-metadata/metrics-finder-metadata-catalog.html#use-the-metadata-catalog).
