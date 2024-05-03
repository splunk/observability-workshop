---
title: Select the RUM view for the Petclinic App
linkTitle: 2.Select Rum env
weight: 2
---


Once the RUM has been configured an you have added a visit for a pet, you can log in to **Splunk Observability Cloud** and verify that the RUM traces are flowing in from you app.

From the left-hand menu click on **RUM** ![RUM](../../images/rum-icon.png?classes=inline&height=25px) and change the **Environment** filter **(1)** to the name of your workshop instance from the dropdown box, it will be **`<INSTANCE>-workshop`** **(1)**(where **`INSTANCE`** is the value from the shell script you ran earlier). Make sure it is the only one selected.
Then change the **App** **(2)** dropdown box to the  name of your app, it will be **`<INSTANCE>-store`**

![rum select](../../images/rum-env-select.png)

If you have selected your Environment and App, you see an overview page showing the RUM status of you App.

![rum overview](../../images/rum-overview.png)

Click on the blue link to get to the details page

![rum  main](../../images/rum-main.png)


