---
title: Select the RUM view for the Petclinic App
linkTitle: 1. Verify RUM Data
weight: 1
---

Lets start a quick high level tour into RUM by clicking ![RUM](../../images/rum-icon.png?classes=inline&height=25px)  **RUM** in the left-hand menu. Then change the **Environment** filter **(1)** to the name of your workshop instance from the dropdown box, it will be **`<INSTANCE>-workshop`** **(1)** (where **`INSTANCE`** is the value from the shell script you ran earlier). Make sure it is the only one selected.

Then change the **App** **(2)** dropdown box to the name of your app, it will be **`<INSTANCE>-store`**

![rum select](../../images/rum-env-select.png)

Once you have selected your **Environment** and **App**, you will see an overview page showing the RUM status of your App (if your Summary Dashboard is just a single row of numbers, you are looking at the condensed view. You can expand it by clicking on the **> (1)** in front of the Application name). If any JavaScript error occurred they will show up as shown below:

![rum overview](../../images/rum-overview.png)

To continue, click on the blue link (with your workshop name) to get to the details page, this will bring up a new dashboard view breaking down the interactions by UX Metrics, Front-end Health, Back-end Health and Custom Events and comparing them to historic metrics (1 hour by default).

![rum  main](../../images/rum-main.png)
Normally you have only one line inside the first chart,  Click on the link that relates to your Petclinic shop,
http://198.19.249.202:81 in our example:

This will bring us to the Tag Spotlight page.
