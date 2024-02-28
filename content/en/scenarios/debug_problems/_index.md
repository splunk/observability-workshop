---
title: Debug Problems in Microservices
linkTitle: 3. Debug Problems in Microservices
weight: 3
archetype: chapter
---
{{% badge icon="clock" style="primary" %}}2 minutes{{% /badge %}} {{% badge style="blue" title="Authors" %}}Derek Mitchell{{% /badge %}}

**Service Maps** and **Traces** are extremely valuable in determining what service an issue resides in.  And related log data helps provide detail on why issues are occurring in that service.  

But engineers sometimes need to go even deeper to debug a problem that’s occurring in one of their services.  

This is where features such as Splunk's **AlwaysOn Profiling** and **Database Query Performance** come in.

**AlwaysOn Profiling** continuously collects stack traces so that you can discover which lines in your code are consuming the most CPU and memory.  

And **Database Query Performance** can quickly identify long-running, unoptimized, or heavy queries and mitigate issues they might be causing. 

In this workshop, we'll explore:

* How to debug an application with several performance issues. 
* How to use **Database Query Performance** to find slow-running queries that impact application performance. 
* How to enable **AlwaysOn Profiling** and use it to find the code that consumes the most CPU and memory. 
* How to apply fixes based on findings from **Splunk Observability Cloud** and verify the result. 

The workshop uses a Java-based application called `The Door Game` hosted in Kubernetes. Let's get started!

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
The easiest way to navigate through this workshop is by using:

* the left/right arrows (**<** | **>**) on the top right of this page
* the left (◀️) and right (▶️) cursor keys on your keyboard
  {{% /notice %}}
