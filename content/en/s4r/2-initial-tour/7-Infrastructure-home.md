---
title: 7. Infrastructure Home Page
description: This section of the workshop will equip you with the basic understanding of the Kubernetes and Database Navigators in the infrastructure section.
weight: 70
---

{{% button icon="clock" %}}15 minutes{{% /button %}}

This section is going to be a little longer, as we are using this section to  dive deeper into some of the special features of the Splunk Observability suite, before we use  them to investigate issues in our application further in the workshop.

Please select Splunk Infrastructure from the menu bar on the right by selecting the ![Infra-monitoring](../images/inframon-icon.png?classes=inline&height=25px). This will bring us to the Infrastructure  Home Page. It has 4 distinct sections that provide either useful information you pick or create a Synthetic Test.

![Infra main](../images/infrastructure-main.png?width=40vw)

* 1. Onboarding Pane, Here you will find video's and information related to Splunk Synthetics. (Can be closed by pressing the X, if space is a premium)
* 2. Test Pane, Here you find the list of all the test that are active in your org, and you can select them to see the results
* 3. Create Test Pane, This drop down pane gives you the option to create a new Synthetic test.

As part of the workshop we have created a default browser test against the application we are running, You find it in the Test Pane (2). It will have the following name **Workshop Browser Test for **, followed by the name of your Workshop.(Your instructor should have provided that to you.)

To continue our tour, lets look at the result of our workshop automatic browser test.  
In the Test Pane, double click on line that contains the name of your workshop. The result should look like this:


Let's run an exercise and  look at some UI options:
{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* In the Performance KPI Drop down box, change the time  from the default 8 hours to Last hour.  
  What can you concluded from the dotted chart, how often are these test ran, and from where?
* Click on a dot in the chart. This should bring you to a new screen. This is th detailed Test Run Results page for the selected test. We will examine this page in great detail later in the workshop, so for now  go back to the Synthetic Home page by clicking on the (the robot icon) ![syntheticsMenu](../../images/synthetics-icon.png?classes=inline&height=25px).
{{% /notice %}}
Lets continue to Infra mon and examine the infrastructure our application is running on.
