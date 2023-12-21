---
title: Debugging 101
linkTitle: 5. Debugging 101
weight: 5
---

## Now let's play the role of the developer

As a developer we must debug the function products:ProductResource.getAllProducts to find the problem.

## Debugging 101, the Line by Line method

Without anything to go on other than "BAD FUNCTION", a Developer must then look at code visually line by line to find and fix the problem. To make this worse, **functions call other functions**, and it can get very messy in bad code scenarios.

We will do the visual inspection mehtod next.

* Using Nano:

``` bash
nano products/src/main/java/com/shabushabu/javashop/products/resources/ProductResource.java
```

* Search in Nano: **[CTRL]-w**
* Enter in: **getAllProducts [Enter]**
* You will be taken here:

``` java
  @GET
    public Response getAllProducts(@DefaultValue("California") @QueryParam("location") String location) {
      
      // STEP X: All we know right now is somewhere in this function, latency was introduced.
  
      myCoolFunction1(location);
      myCoolFunction2(location);
      myCoolFunction10(location);
      myCoolFunction13(location);
      myCoolFunction5(location);
      myCoolFunction6(location);
```

We can see here in getAllProducts, the first call is to `myCoolFunction1()`, so as may have guessed our next step is to go look at `myCoolFunction1()`.

* Search in Nano: **[CTRL]-w**
* Enter in: myCoolFunction1 **[Enter]**
* Find the next occurrence: **[CTRL]-w [Enter]**
* Keep repeating **[CTRL]-w [Enter]** until you get to the actual function definition

It looks like this:

``` java
private void myCoolFunction1(String location) {
      // Generate a FAST sleep of 0 time !
      int sleepy = lookupLocation1(location);
      try{
      Thread.sleep(sleepy);

      } catch (Exception e){

      }
    }
```

Now, `myCoolFunction1` calls `lookupLocation1(location)`

* Search in Nano: **[CTRL]-w**
* Enter in: lookupLocation1 **[Enter]**

I think you get the picture by now, you have no choice but to inspect every line of code and every function called and visually inspect them for problems. This can be a VERY long process and kills our customers Mean Time to Repair. This happens quite often to our customers with our competition beacsue they can't provide all the traces 100% of the time and most can't scale to add more data, via Custom Attributes on top of that!

Remember, without Full Fidelty, you have to either reproduce errors / latency in another environment or inspect code line by line.

So they are stuck where we are, quite often.

OK, enough fun. Let's make this easier for our developer, and show off some Splunk APM Scale!

* Exit your editor:
* Exit nano: **[CTRL]-X**
* Optional: If it asks you to save, hit **N**
