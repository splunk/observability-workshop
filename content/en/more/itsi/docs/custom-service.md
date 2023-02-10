---
title: Custom Service
weight: 3
---

In this section, we will create a custom Service in Splunk ITSI based on observations in the Splunk Observability Cloud Platform.

## Access the Splunk Observability Cloud Platform

Visit the [Splunk Observability Cloud Platform](https://app.eu0.signalfx.com/#/home) and log in with the credentials that have been provided to you.  If everything went well you should see the Home screen which looks like this:

<!-- <img src="../../images/custom_service/o11y_home.png" alt="O11y Home Screen" style="width: 70%;"/> -->
![O11y Home Screen](../../images/custom_service/o11y_home.png)

On the menu on the left (you might have to expand it by clicking on the double arrow on the bottom left), choose **Dashboards**, locate the pre-built **AWS EBS** Dashboard, and select **EBS Volumes**.

<!-- <img src="../../images/custom_service/ebs_dashboard.png" alt="EBS Dashboards" style="width: 50%;"/><br> -->
![EBS Dashboards](../../images/custom_service/ebs_dashboard.png)

Open the dashboard with the title **Total Ops/Reporting Interval** by locating the relating tile, clicking on the three little dots on the upper right of the tile, and then **Open**.

<!-- <img src="../../images/custom_service/open_dashboard.png" alt="Open Dashboard" style="width: 90%;"/><br> -->
![Open Dashboard](../../images/custom_service/open_dashboard.png)

Click on **View SignalFlow**.

<!-- <img src="../../images/custom_service/view_sf.png" alt="View Signal Flow" style="width: 90%;"/><br> -->
![View Signal Flow](../../images/custom_service/view_sf.png)

You should see the following:

```text
A = data('VolumeReadOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='A')
B = data('VolumeWriteOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='B')
```

Let's modify the SignalFlow so we can use it to create our query in Splunk Enterprise - We have to remove the `A =`, `B =`, and add a `semicolon` `;` to the end of the first line so we end up with the following:

```text
data('VolumeReadOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='A');
data('VolumeWriteOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='B')
```

Now go to your Splunk Enterprise UI and open the **Search & Reporting** app. We can craft the following SPL Search Term by adding `| sim flow query=` and including the modified SignalFlow statement wrapped in double quotes:

```text
| sim flow query="data('VolumeReadOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='A');
data('VolumeWriteOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='B')"
```

Execute this search.

{{% notice title="Caution" %}}
Internal note: If I run the below search, my line chart is empty. Is this supposed to be like this?
{{% /notice %}}

If you would like to see the results in a visualisation, you can append a *timechart* command to the search term with a "|". The complete search term would then look something like this:

```text
| sim flow query="data('VolumeReadOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='A');
data('VolumeWriteOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').scale(60).sum().publish(label='B')"
| timechart max(VolumeReadOps) max(VolumeWriteOps)
```

### Let's create our EBS service

In order to create our own custom create our EBS service, let's navigate to the Splunk IT Service Intelligence Add-On. Click on **Configuration** and select **Service** from the dropdown menu.
Next, click on the green **Create Service** button and select the **Create Service** option from the dropdown menu.

<img src="../../images/custom_service/create_service_dd.png" alt="Create Service" style="width: 15%;"/>

In the following input form, provide a meaningful title (we choose *EBS Volumes* on the screenshot below), tick the *Manually add service content* radio button, and click on the **Create** button.

<img src="../../images/custom_service/title.png" alt="Create Service" style="width: 40%;"/>

In the following view, select the **KPIs** tab, click the **New** dropdown menu, and select **Generic KPI**.

<img src="../../images/custom_service/generic_kpi.png" alt="Creation of Generic KPI" style="width: 40%;"/>

What follows now is a Step-by-Step walkthrough. Please click the **Next** button which brings you to the *Step 2 of 7: Source* screen.
Paste the command we just created in the textbox with the lable *Search*.

```text
| sim flow query="data('VolumeReadOps', filter=filter('namespace', 'AWS/EBS') and filter('stat', 'sum'), rollup='rate', extrapolation='zero').publish()"
| rename _value as VolumeReadOps
```

In the field with the *Threshold* label, enter "VolumeReadOps".

<img src="../../images/custom_service/step2.png" alt="Pasting search string" style="width: 60%;"/>

Navigate to *Step 7 of 7* by clicking on the *Next* buttons. You can leave everything between the first and seventh step as default.
On the *Step 7 of 7* dialog, manually add a threshold by clicking **+ Add Threshhold**. (if nothing is happening on the Disk it might show close to 0 as a number)

<img src="../../images/custom_service/add_threshold.png" alt="Manually add Threshold" style="width: 61%;"/>

Click on the **Finish** button, and subsequently, when the dialog is closed, on the **Save** button on the lower right.

<img src="../../images/custom_service/save_enable.png" alt="Click the 'Save and Enable' button" style="width: 50%;"/>

Let's attach our standalone to the AWS service. To do that, click on the **Configurations** dropdown menu and select the **Services** option.
Locate the *AWS* service in the list of available services and open it by clicking on it. Click on the *Service Dependencies* tab, and click on the
**Add dependencies** button.

Locate our custom *EBS Volume* service by using the filter, select it, and select the *ServiceHealthScore* KPI.

<img src="../../images/custom_service/ebs.png" alt="Add dependencies" style="width: 50%;"/>

Click on the **Done** button. Verify that the service got added to the list of available serives and click the **Save** button on the lower right.
In the pop-up dialogue, click **Save and Enable**.

go to Service open AWS serv
go to Service Analyzer -> Default Analyzer
review what you built

Finally, view the result of your work by clicking on the *Service Analyzer* tab and choose the *Default Analyzer* option. In the *Service Analyzer* view, click the **Tree view** button. You should see the Tree view with our newly created service:

<img src="../../images/custom_service/tree_view.png" alt="How to navigate to the Tree View" style="width: 100%;"/>

<img src="../../images/custom_service/result.png" alt="Service Analzyer" style="width: 100%;"/>
