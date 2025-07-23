---
title: Dashboard Mirroring
linkTitle: 3.3 Dashboard Mirroring
weight: 3
authors: ["Tim Hard"]
time: 5 minutes
draft: false
---

Not only do the out-of-the-box dashboards provide rich visibility into the infrastructure that is being monitored they can also be mirrored. This is important because it enables you to create standard dashboards for use by teams throughout your organization. This allows all teams to see any changes to the charts in the dashboard, and members of each team can set dashboard variables and filter customizations relevant to their requirements.

{{% notice title="Exercise: Create a Mirrored Dashboard" style="green" icon="running" %}}

1. While on the Kubernetes Pods dashboard, you created in the previous step, In the upper right corner of the dashboard click the **Dashboard actions** button (3 horizontal dots) -> Click **Add a mirror...**. A configuration modal for the Dashboard Mirror will open.

    ![Mirror Dashboard Menu](../../images/mirror-dashboard-menu.png?width=40vw)

2. Under **My dashboard group** search for your e-mail address and select it.
3. (Optional) Modify the dashboard in **Dashboard name override** name.
4. (Optional) Add a dashboard description in **Dashboard description override**.
5. Under **Default filter overrides** search for `k8s.cluster.name` and select the name of your Kubernetes cluster.
6. Under **Default filter overrides** search for `store.location` and select the city you entered during the workshop setup.
![Mirror Dashboard Config](../../images/mirror-dashboard-config.png?width=40vw)
7. Click **Save**

You will now be taken to the newly created dashboard which is a mirror of the Kubernetes Pods dashboard you created in the previous section. Any changes to the original dashboard will be reflected in this dashboard as well. This allows teams to have a consistent yet specific view of the systems they care about and any modifications or updates can be applied in a single location, significantly minimizing the effort needed when compared to updating each individual dashboard.

In the next section, you'll add a new logs-based chart to the original dashboard and see how the dashboard mirror is automatically updated as well.
{{% /notice %}}
