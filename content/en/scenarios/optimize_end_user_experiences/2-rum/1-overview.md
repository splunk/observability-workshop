---
title: 1. Overview
linkTitle: 1. Overview
weight: 1
---

## Overview of the RUM Workshop

The aim of this Splunk Real User Monitoring (RUM) workshop is to let you:

* Shop for some fantastic items on the Online Boutique to create traffic, and create a number of RUM User Sessions[^1] that you can view in the Splunk Observability Suite.

* See an overview of the performance of all your application(s) in the Application Summary Dashboard (Both Mobile and Web based)

* Examine the performance of a specific website or Mobile App with RUM metrics.

* Investigate issues with your website and backend services.

* (Optionally) See how to add RUM to your website.

In order to reach this goal, we will use an online boutique to order various products. Whilst shopping on the online boutique you will create what is called a User Session.

You may encounter some issues with this web site, and you will use Splunk RUM to identify the issues, so they can be resolved by the developers.

If this a standalone RUM workshop, the workshop host will provide you with a URL for an online boutique store that has RUM enabled.

Each of these Online Boutiques are also being visited by a few synthetic users, this will allow us to generate more live data to be analyzed later.

[^1]: A RUM Users session is a "recording" of a collection of user interactions on an application, basically collecting a website or app’s performance measured straight from the browser or Mobile App of the end user. To do this a small amount of JavaScript is embedded in each page. This script then collects data from each user as he or she explores the page, and transfers that data back for analysis.
