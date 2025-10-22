---
title: Don't Forget Chicago
linkTitle: 9. Don't Forget Chicago
weight: 9
---

## Don't forget Chicago

We are nearly done, one more location to go... Chicago.

Since we have been having so many issues related to "location" and we have added that custom attribute via Opentelemetry Manual Instrumentation, lets go to the Splunk Observability UI and look at an APM metric set around that tag that I created for us.

![9-chicago-1-metricset](../images/9-chicago-1-metricset.png)

* Open a browser and navigate to [http://EC2-Address:8010](http://EC2-Address:8010)
  * Replace **EC2-Address** with the ip address of your host
* Select a few locations and hit the Login button.
  * Make sure to also select the Chicago Location and hit the Login button.

![9-chicago-2-app](../images/9-chicago-2-app.png)

Uh oh! We received a 500 error, something is wrong there as well.

![9-chicago-3-map](../images/9-chicago-3-map.png)

* Return to the Splunk Observability UI and lets look once again at our Service Map
* Select the Instruments Service
* Click the Breakdowns dropdown on the right and select location

![9-chicago-4-map-breakdown](../images/9-chicago-4-map-breakdown.png)

We see there was an un-handled exception thrown in the Instruments service, and some latency from our database that is related to the Chicago location!

* Click on Traces on the right
* Click Errors Only
* Click one of the traces

![9-chicago-5-trace](../images/9-chicago-5-trace.png)

We can see the exception was thrown by Hibernate, however it was thrown in our method instruments: `InstrumentRepository.findInstruments`

![9-chicago-6-span](../images/9-chicago-6-span.png)

## Let's play developer again

* Edit the file `instruments: InstrumentRepository.findInstruments` using nano:

``` java
nano instruments/src/main/java/com/shabushabu/javashop/instruments/repositories/FindInstrumentRepositoryImpl.java
```

* Find the method: `findInstruments`
  * You know how to do this now, right?

![9-chicago-7-code](../images/9-chicago-7-code.png)

We can see the developer accidently added the Instruments database with the Chicago Instruments database!

Let's change the query and fix this, remove instruments_for_sale from our query.

* Change this:

``` java
public Object findInstruments() {
  LOGGER.info("findInstruments Called (All)");
  Object obj = entityManager.createNativeQuery( "SELECT * FROM instruments_for_sale, instruments_for_sale_chicago").getResultList(); 
  return obj;
}
```

* to this:

``` java
public Object findInstruments() {
  LOGGER.info("findInstruments Called (All)");
  Object obj = entityManager.createNativeQuery( "SELECT * FROM instruments_for_sale_chicago").getResultList(); 
  return obj;
}
```

* Save the changes: **[CTRL]-o [Enter]**
* Exit: **[CTRL]-x**

* Build and Deploy Application

``` bash
./BuildAndDeploy.sh
```

Now let's test the Chicago location once again

* Open a browser and navigate to [http://EC2-Address:8010](http://EC2-Address:8010)
* Select the Chicago location and Login

We now see the 500 error is gone!

* Let's confirm a clean Service Map:

![9-chicago-8-map-clean](../images/9-chicago-8-map-clean.png)

If you see a clean service map, free of errors and Latency you have successfully completed the Java Instrumentation Workshop!

**Congratulations!!!**
