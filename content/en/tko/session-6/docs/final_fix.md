---
title: The Final Fix!
linkTitle: Developer Role (Part 2)
weight: 9
---

## 1. Let's play developer again

Edit the file `instruments: InstrumentRepository.findInstruments`

``` bash
vi instruments/src/main/java/com/shabushabu/javashop/instruments/repositories/FindInstrumentRepositoryImpl.java
```

``` java
    @SuppressWarnings("unchecked")
    @Override
    public Object findInstruments() {
        LOGGER.info("findInstruments Called (All)");

        Object obj = entityManager.createNativeQuery( "SELECT * FROM instruments_for_sale, instruments_for_sale_chicago").getResultList(); 

        return obj;
    }
```

We can see the developer accidently added the Instruments database with the Chicago Instruments database! Let's change the query and fix this, remove `instruments_for_sale` from our query.

Change this:

``` java
public Object findInstruments() {
   LOGGER.info("findInstruments Called (All)");

   Object obj = entityManager.createNativeQuery( "SELECT * FROM instruments_for_sale, instruments_for_sale_chicago").getResultList();

   return obj;
}
```

To this:

``` java
public Object findInstruments() {
    LOGGER.info("findInstruments Called (All)");
    //Object obj = entityManager.createNativeQuery( "SELECT * FROM instruments_for_sale, instruments_for_sale_chicago").getResultList();

    Object obj = entityManager.createNativeQuery( "SELECT * FROM instruments_for_sale_chicago").getResultList();

    return obj;
}
```

## 2. Build and Deploy Application once more

``` bash
cd javashop-otel directory
./BuildAndDeploy.sh
```

Now let's test the Chicago location once again, open a browser and navigate to [http://localhost:8010](http://localhost:8010). Select the Chicago Location and Login.

We now see the 500 error is gone! Let's confirm a clean Service Map!

![Screen Shot 2022-11-28 at 8 35 11 AM](https://user-images.githubusercontent.com/32849847/204350088-fca43e3c-42ea-4933-8a61-01eb2083fd23.png)

{{% alert title="Congratulations" color="info" %}}

If you see a clean service map, free of errors and Latency you have successfully completed the Java Instrumentation Workshop!**

{{% /alert %}}

**Have a lovely day!**
