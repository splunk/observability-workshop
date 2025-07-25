---
title: Splunk Data Management Workshop - Ingest Processor / Logs2Metrics
linkTitle: Splunk Data Management Workshop 
description: Discover data management principles and leverage ingest process for logs to metrics
weight: 10
authors: ["Jeremy Hicks", "Kyle Prins", "Joseph Kandatilparambil"]
time: 1 hour 30 minutes
---
This workshop will help you understand the power of Ingest Actions (IA), Edge Processor (EP), and Ingest Processor (IP) and how they help manage your data quickly as it streams into Splunk. You'll learn how to use these tools from a web browser and how to filter, mask, transform, enrich, and route data to multiple destinations. You'll also see that by using these tools, you can get faster feedback that your changes are working.

In this hands-on workshop, you will work with all three tools in a Splunk Cloud environment. This practical setting allows you to see where these components reside, when you should use them, and how they each process data. The interactive approach will ensure that you leave the workshop with a confident understanding of these tools and their applications.

Throughout the labs in this workshop, you will work with Cisco ASA logs. Using Ingest Actions, you will complete the base use case and build on it with Edge Processor and, finally, Ingest Processor.


#

## Base Use Cases

The base use cass you will use for all three labs follows. Edge Processor and Ingest Processor build on this. Those details are in their respective lab sections.   

### **1. Ingest Cisco ASA Logs**

The environment already has the Cisco ASA logs set up for you. You will need to work with them to achieve the lab goals.   


### **2. Remove Events with Lower-Level Information**

You will send information you don't need daily to S3 instead of a Splunk index. As part of your configuration, removing events with lower-level details is important to streamline your data and focus on the most relevant logs. You still want to keep these logs in a lower-cost object store for compliance. Send logs with the following information to S3 instead of your Splunk index:

1\. Built inbound UDP connection.

2\. Built inbound TCP connection.

3\. Teardown UDP connection.

4\. Teardown TCP connection.

5\. Disallowing new connections.

### **3. Mask the User Name Field**

Before indexing the Cisco ASA logs in Splunk, you want to mask the user name, which we regard as sensitive.


