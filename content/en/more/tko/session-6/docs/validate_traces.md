---
title: Validate Traces are being collected
linkTitle: Validate Traces
weight: 2
---

## 1. Users and Workflows

As we go through this workshop we will be switching roles from SRE to Developer.  First we will start with first responders or SREs who will identify an issue in Splunk Observability UI.

Next, we will jump to a Developer Role to see how a Developer will solve a problem using trace data identified by our SRE. Of course, we are not requiring 2 people for this workshop as each participant will play both roles.

## 2. View Service Map

If your instrumentation was successful, the service-map will show latency from the shop service to the products service.

![Screen Shot 2022-12-08 at 11 48 58 AM](https://user-images.githubusercontent.com/32849847/206541846-7f0e6462-7659-44bc-bc48-3621c2872fc4.png)

Click on shop service, click Traces (right side), sort by Duration and select the longest duration trace.

![LongTrace](https://user-images.githubusercontent.com/32849847/204347798-4f232b7f-7a7a-483f-9d61-f0b535e9ecf0.png)

Now we can see the long latency occurred in the products service and if we click on `products: /products` we can see the offending method was `products:ProductResource.getAllProducts`.

![long-trace-detail-GetAllProducts](https://user-images.githubusercontent.com/32849847/204347855-724545bf-c3df-478a-a27d-e4f85f708e15.png)

Our next step here would be to send that trace to a developer by clicking download trace and they will have to debug the method. Before we do that please take note of the Tags available for the developer to leverage to find root cause.

{{% alert title="Note:" color="info" %}}

Since they do not have full parameter information it can be a long process.

{{% /alert %}}
