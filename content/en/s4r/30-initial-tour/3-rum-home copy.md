---
title: Real User Monitoring Home Page
linkTitle: 3. RUM Home Page
weight: 30
---
 
{{% button icon="clock" color="#ed0090" %}}5 minutes{{% /button %}}

Again, as this is a quick tour and we will be visiting the Real User Monitoring UI in more detail later, this will just highlight the main options.

{{% notice title=" Rum Environments & Apps" style="info" %}}
As with APM, Real User Monitoring works with environments to separate RUM information/traces information, this allows you to separate RUM trace information from different teams/applications. It also adds an extra option for Apps (short for applications). This allows you to distinguish between separate browser applications in the same environment.

Splunk RUM is available for both browser and mobile applications. You will see that as the source type in the UI. In this workshop, we will just focus on browser-based RUM.
{{% /notice %}}

If you have not done so already, please select ![RUM](../images/rum-icon.png?classes=inline&height=25px) from the Main menu. This will bring you to the RUM Home page.

This Page has 3 distinct sections that provide information or allow you to navigate the RUM UI.

![RUM Page](../images/rum-main-page.png?width=30vw)

1. **Onboarding Pane:** Here you will find videos and references to document pages of interest for RUM  
(Can be closed by the **X** on the right, if space is at a premium.)
2. **Filter Pane:** This pane allows you to filter on Environment, Application and source type.
3. **Application Summary Pane:** This pane shows you a health summary of all your applications that send RUM trace info. Note, that the summaries have a compact and detailed view (as shown in the image above).

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* First,  Make sure the time window is set to *-15m*, then let's make sure we are just looking at our own environment and application.
* In the Filter Pane, select your workshop from the *Environment* Dop down and make sure your workshop is the only one selected with a ![blue tick](../../images/blue-tick.png?classes=inline) in front of it. The naming convention for your environment is *[NAME OF WORKSHOP]-workshop*. You can also set the *App* name. Here the naming convention is *[NAME OF WORKSHOP]-shop*. We can leave *Source* on *All* or *Browser*.
* We should now have a single application showing. Let's make sure it is in the right view. You can toggle between the compact and detailed views by clicking on the grey area around the tiles in the  Application Dashboard.
* First, make sure it is in the detailed view as shown below:
![rum detailed view](../images/rum-detail-view.png?width=40vw)

* Hover over the *Page/Java Script* Error tile. What can you conclude from the information provided?
* Does the second tile, the *Java Errors* confirm your conclusion?
* We will look in more detail at these errors in the RUM deep dive section. but indeed it looks like every Page view has 3 errors in the underlying javascript.
* The 3rd Tile, the *Web Vitals* provides you with key metrics that relate to the behaviour of your site, the lower the number the better.

{{% notice title="Web Vitals infos" style="info" %}}
Web Vitals are an industry-wide initiative to improve web performance and user experience they are a set of measurements that tell you how well a website is performing for its visitors. These measurements include things like how fast the website loads, how quickly you can interact with it, and how stable it is.

If a website has good Web Vitals, it means it's fast and easy to use. If the Web Vitals are bad, it might be slow and frustrating for people to use. Web developers use these measurements to make websites better and ensure a smoother experience for users.

{{% /notice %}}

* The last tile, the *Most recent detectors* tile, will show if any alert has been fired for your application.  If no alerts have been set up, you can do so here as well.  We will look at this in the deep dive.

* Finally, click on the Gray area around the Application tile to switch to the compact view, shown below:

![single view](../images/rum-single-view.png?width=40vw)

* Note that this  compact view shows the same information concisely, this view is useful if you have  multiple applications, this way you can see the health in one  overview
{{% /notice %}}

We will investigate RUM in more detail later, so let's have a look at how Splunk Log Observer works with Log data on the next page.
