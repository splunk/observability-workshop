---
title: Build and Deploy again
linkTitle: Build and Deploy again
weight: 8
draft: true
---

## 1. Build and Deploy Application again

``` bash
./BuildAndDeploy.sh
```

Now that we have rebuilt and deployed our application, traffic is being sent once again.  

We are waiting a few minutes . . .

{{% notice title="Congratulations" color="info" %}}

If you do not see Red in your service map, you have successfully completed our Inventory application review for Shri Lanka and Colorado locations!!

{{% /notice %}}

Now let's ensure Chicago was on-boarded correctly. However, since we have been having so many issues related to "location" and we have added that custom attribute via Opentelemetry Manual Instrumentation, lets go to the Splunk Observability UI and create an APM metric set around that tag.

NOTE: We can do this without concern for Cardinality as we know this tag only has 6 possible values.

Index the location Tag.

![image](https://user-images.githubusercontent.com/32849847/213540265-5b0567ab-c9f3-412f-bec0-07277c7e8650.png)

## 2. Build and Deploy Application to run traffic again

``` bash
./BuildAndDeploy.sh
```

Open a browser and navigate to [http://localhost:8010](http://localhost:8010)

![image](https://user-images.githubusercontent.com/32849847/213541843-30266285-787f-493b-bc90-ffb4ac6e4c77.png)

Select a few locagtions and hit the login button, remember to select the Chicago Location and Login

Uhh ohh ! We received a 500 error, something is wrong there as well.  Return to the Splunk Observability UI and lets look once again at our Service Map

![Screen Shot 2022-11-28 at 8 11 47 AM](https://user-images.githubusercontent.com/32849847/204349595-fca270ad-379e-48c5-b2e1-7f222af82c55.png)

We see there was an un-handled exception thrown in Instruments service and some latency from our database.

Select the Instruments Service, click on Traces on the right and select **Errors Only**

![Screen Shot 2022-11-28 at 8 14 50 AM](https://user-images.githubusercontent.com/32849847/204349696-dc19d62f-ed82-4533-ad27-138237821b8e.png)

We can see the exception was thrown by Hibernate, however it was thrown in our method `instruments: InstrumentRepository.findInstruments`

![Screen Shot 2022-11-28 at 8 14 37 AM](https://user-images.githubusercontent.com/32849847/204351905-03fe632b-b21c-4e8d-8044-dc582fed2253.png)
