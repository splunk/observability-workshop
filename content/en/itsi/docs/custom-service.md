---
title: Custom Service
weight: 3
---

## Create a custom service

Open the EBS Dashboard -> open Total Ops/Reporting Interval -> view signalflow

You hould see the following :

```text
A = data('VolumeReadOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='A')
B = data('VolumeWriteOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='B')
```

Let's change the signalflow to create our query in Splunk Enterprise :

```text
data('VolumeReadOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='A');
data('VolumeWriteOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='B')
```

In Splunk Enterprise open Search and Reporting :

run the following command:

```text
| sim flow query=data('VolumeReadOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='A');
data('VolumeWriteOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='B')
```

if you want to build a chart:

```text
| sim flow query=data('VolumeReadOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='A');
data('VolumeWriteOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='B')
| timechart max(VolumeReadOps) max(VolumeWriteOps)
```

### Let's create our EBS service

Make sure to go into Splunk IT Service Intelligence.
Configuration -> Service -> Create services -> Create service
Enter Title: EBS volumes
Select Manually add service content

(screenshot to be added)

KPI -> new -> Generic KPI
Click Next
Paste the command we just created in the textbox

```text
| sim flow query="data('VolumeReadOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').publish()"
| rename _value as VolumeReadOps
```

In the treshold field enter VolumeReadOps (you can keep everything default for the rest of the configuration)  
click next
click next
click next
add threshold manually (if nothing is happening on the Disk it might show close to 0 as a number)
save on the bottom of the page !!!
Let's attach our standalone to the AWS service
go to Service open AWS service
go to Service Dependencies tab
Add Dependencies
Use the filter to select EBS volumes
Select the service health score
go to Service Analyzer -> Default Analyzer
review what you built
