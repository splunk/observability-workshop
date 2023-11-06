---
title: Checking Logs With Log Observer
linkTitle: 4. Log observer Home Page
weight: 40
---
 
{{% button icon="clock" %}}5 minutes{{% /button %}}

We continue out tour of the Splunk observability Ui with Log Observer. Log Observer is a feature within Splunk Observability Cloud hat allows you to seamlessly bring in log data from your Splunk Platform into an intuitive and codeless interface designed to help you find and fix problems fast. You will be able to easily perform log-based analysis and seamlessly correlate your logs with Splunk Infrastructure Monitoring’s real-time metrics and Splunk APM traces in one place.

If you have not done so already, please select ![Log observer](../images/log-observer-icon.png?classes=inline&height=25px) from the Main menu. This will bring you to the Log Observer Home page.

This Page has 4 distinct sections that provide information or allows you to navigate the Log Observer UI and see log data from the selected Indexes..

![Lo Page](../images/lo-home.png?width=30vw)

1. Onboarding Pane. Here you will find video's and references to document pages of interest for Log Observer.
(Can be closed by the **X** on the right, if space is at a premium.)
2. Filter Pane. This pane allows you to filter on Time, Indexes, Fields Application and source type. this pane also allows you to save or reused previously saved searches.
3. Log's Table Pane. This pane shows you a
4. Fields Pane. Here you can find all the fields that have been  used in the current Index selection.

#### WIP WIP WIP  WIP

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* First,  Make sure the time window is set to *-15m*, then let's make sure we are just looking at our own environment and application.
* In the Filter Pane, select your workshop from the *Environment* Dop down and make sure your workshop is the only one selected with a ![blue tick](../../images/blue-tick.png?classes=inline) in front of it. The naming convention for your environment is *[NAME OF WORKSHOP]-workshop*. You can also set the *App* name. Here the naming convention is *[NAME OF WORKSHOP]-shop* . We can leave *Source* on *All* or *Browser*.
* We now should now have a single application showing. Let's make sure it is in the right view. You can toggle between the compact and detailed views by clicking on the gray area around the tiles in the  Application Dashboard.
* First, make sure it in the detailed view as show below:
![rum detailed view](../images/rum-detail-view.png?width=40vw)

* Hover over the *Page/Java Script* Error tile. What can you conclude from the information provided?
* Does the second tile, the *Java Errors*  confirm your conclusion?
* We will look in more details at these errors in the RUM deep dive section. but indeed it looks like every Page view has 3 errors in the underlying java script.
* The 3rd Tile, the *Web Vitals* Provide you with key Metrics that relate to the behaviour of your site, the lower the number the better.

{{% notice title="Web Vitals infos" style="info" %}}
Web Vitals they are an industry-wide initiative to improve web performance and user experience a They are a set of measurements that tell you how well a website is performing for its visitors. These measurements include things like how fast the website loads, how quickly you can interact with it, and how stable it is.
 If a website has good Web Vitals, it means it's fast and easy to use. If the Web Vitals are bad, it might be slow and frustrating for people to use. Web developers use these measurements to make websites better and ensure a smoother experience for users.

{{% /notice %}}

* The last Tile, teh *Most recent detectors* tile, will show if any alert has fired for you application.  If no alerts have been set up, you can do so here as well.  We will look at his in the deep dive.

* Finally, click on the Gray area around the Application tile to switch the compact view, shown below:

![single view](../images/rum-single-view.png?width=40vw)

* Note that this  compact view show the same information in a concise way, this view is useful if you have  multiple application, this way you can see the health in one  over view
{{% /notice %}}

We will investigate RUM in more detail later, so lets have a look at how Splunk Log Observer works with Log data in the next page.

{{% notice title=" Rum Environments & Apps" style="info" %}}
As with APM, Real User Monitoring works with environments to separate RUM information/traces information, this allows you to separate RUM trace information from different teams/applications. It also adds an extra option for Apps (short for applications). This allows you to distinguish between separate browser applications in the same environment.

Splunk RUM offers RUM for both Browser & Mobile applications.  You will see that as the source type in the Ui. In this workshop we will just focus on browser based  RUM.
{{% /notice %}}
