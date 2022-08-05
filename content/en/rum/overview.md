---
title: Overview
weight: 2
menu:
  docs:
    weight: 2
---

## Overview of the RUM Workshop

The aim of this Splunk Real User Monitoring (RUM) workshop is to let you:

* Shop for some fantastic items on the Online Boutique to create traffic,</br>
  and create a number of RUM user sessions[^1] that you can view in the Splunk Observability Suite.

* See an overview of the performance of all your application(s)</br>
  in the Application Summary Dashboard (Both Mobile and Web based)

* Examine the performance of a specific website or Mobile App with RUM metrics.

* Investigate issues with your website and backend services.

* (Optionally) See how to add RUM to your website.

 In order to reach this goal, we will use an online boutique to order various products. Whilst shopping on the online boutique you will create what is called a User Session[^1].</br>
 You may encounter some issues with this web site, and you will use Splunk RUM to identify the issues, so they can be resolved by the developers.

If this an standalone RUM workshop, the workshop host will provide you with an URL for an online boutique store that has RUM enabled.

If you are running this session as part of the IMT/APM workshop you will be able to use your current online boutique store which is RUM enabled.

Each of these Online Boutique's are also being visited by few synthetic users, this will allow us to generate more live data to be analyzed later.

[^1]: A RUM Users session is a "recording" of a collection of user interactions on an application, basically collecting a website or app’s performance measured straight from the browser or Mobile App of the end user. To do this a small amount of JavaScript is embedded in each page. This script then collects data from each user as he or she explores the page, and transfers that data back for analysis.
