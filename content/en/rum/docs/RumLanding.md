---
title: Reviewing the RUM Landing Page 
weight: 1
---

* Visit  the RUM landing page and and check the overview of the performance of all your RUM enabled applications with the Application Summary Dashboard (Both Mobile and Web based)

---

## 1. Visit the RUM Landing Page

Visit and login into your Splunk IMT/APM/RUM Website. From the left side menu bar select **RUM** ![RUM-ico](../../images/RUM_ico.png). This will bring you to your the RUM Landing Page .

The goal of this page is to give you in a single page, a clear indication of the health, performance and potential errors found in your application(s) and allow you dive deeper into the information about your User Session collected from your web page/App.  
You will have a pane for each of your active RUM applications. (The view below is the default expanded view)

![RUM-App-sum](../../images/Applicationsummarydashboard.png)

If you have multiple applications, the pane view may be automatically reduced by collapsing the panes as shown below:

![RUM-App-sum-collapsed](../../images/multiple_apps_collapsed.png)

You can expanded a condensed RUM Application Summary View to the full dashboard by clicking on the small browser ![RUM-browser](../../images/browser.png) or Mobile ![RUM-mobile](../../images/mobile.png)icon. (Depending on the type of application: *Mobile* or *Browser* based) on the left in front of the applications name, highlighted by the red arrow.

## 2. Configure the RUM Application Summary Dashboard Header Section

 RUM Application Summary Dashboard consists of 6 major sections. The first is the selection header, where you can set/filter a number of options:

* A drop down for the time window you're reviewing (You are looking at the past 15 minutes by default)
* A drop down to select the Environment[^1] you want to look at.</br>
  (This allows you to focus on just the subset of application belonging to that environment).
* A drop down with the available Environments to view:  (Choose the one provided by the workshop host or *Select all* for the workshop)
* A drop down list with the various web apps being monitored (You    can use the one provided by the workshop host or use *Select all*)</br>
This will focus you on just 1 (One) application.</br>
For the workshop make sure you can use the one provided by the workshop host or or *Select all*.  
* A drop down to select the source type  *Browser* or *Mobile* applications to view</br> For the Workshop  select *All* as the source.
* A hamburger menu located at the right of the header allowing to configure some settings of your Splunk RUM application. (we will visit this in a later section).

![RUM-SummaryHeader](../../images/RUM_SummaryHeader.png)

For the workshop lets investigate your application in the next section: [Check Health Browser Application](../browserapp-summary/)

---

[^1]: A deployment environment is a distinct deployment of your system or application that allows you to set up configurations that don’t overlap with configurations in other deployments of the same application. Separate deployment environments are often used for different stages of the development process, such as development, staging, and production.</br></br>A common application deployment pattern is to have multiple, distinct application environments that don’t interact directly with each other but that are all being monitored by Splunk APM or RUM: for instance, quality assurance (QA) and production environments, or multiple distinct deployments in different datacenters, regions or cloud providers.
[](http://nebezb.com/)