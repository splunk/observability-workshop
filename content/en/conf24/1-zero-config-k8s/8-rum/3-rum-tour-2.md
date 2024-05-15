---
title: RUM trace  Waterfall view & linking to APM 
linkTitle: 2. Follow RUM Traces
weight: 3
---

Once RUM has been configured and you have added a visit for a pet, you can log in to **Splunk Observability Cloud** and verify that RUM traces are flowing in.

From the left-hand menu click on **RUM** ![RUM](../../images/rum-icon.png?classes=inline&height=25px) and change the **Environment** filter **(1)** to the name of your workshop instance from the dropdown box, it will be **`<INSTANCE>-workshop`** **(1)** (where **`INSTANCE`** is the value from the shell script you ran earlier). Make sure it is the only one selected.

Then change the **App** **(2)** dropdown box to the name of your app, it will be **`<INSTANCE>-store`**

![rum select](../../images/rum-env-select.png)

Once you have selected your **Environment** and **App**, you will see an overview page showing the RUM status of your App (if your Summary Dashboard is just a single row of numbers, you are looking at the condensed view. You can expand it by clicking on the **>** in front of the Application name).
