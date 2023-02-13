---
title: Root Cause Analysis
linkTitle: Root Cause Analysis
weight: 7
---

## 1. Latency Root Cause

Open Service Map in Splunk Observability UI

![Screen Shot 2022-12-08 at 11 48 58 AM](https://user-images.githubusercontent.com/32849847/206542093-f97b37ce-7e58-45bc-a281-5a388d60617e.png)

We can see we still have our original Latency issue, however our exception for Invalid Locale should be gone.

Let's check to see our InvalidLocale Exception is gone. Click Shop Service, click Traces on the right. We did remove the exception however it seems removing the Exception did not fix the latency...

Lets see if the newly added annotations provide us more relevant information for the next responder once we find the cause.

{{% notice title="Note:" color="warning" %}}

We added additional information Parameter Values at Time of Latency. In this case the **Location** tag was created due our handy Annotator, that did the [OpenTelemetry Annotations](https://opentelemetry.io/docs/instrumentation/java/automatic/annotations/)

{{% /notice %}}

![image](https://user-images.githubusercontent.com/32849847/213582624-66466a19-00fa-4dda-acd0-f6970d594ba1.png)

We can see that the actual function call that has the latency was not `ProductResource.getAllProducts` but the function call `ProductResource.myCoolFunction234234234`!

With this information a Developer can debug very quickly. Consider the case of debugging code, that you may not have written yourself without Parameter Values at the time of the issue? You would have no choice but to go line .... by line ..... by line..... which can take a very long time.

Since we now have the parameter tagged as part of our span metadata the actual root cause is seemingly related to the "location" Colorado!

It appears the one custom attribute that was tagged for function `ProductResource.myCoolFunction234234234` was `myInt` with a value of `999`.

Let's see if we can find the code that is causing this latency.

## 2. Fix the code

``` bash
vi products/src/main/java/com/shabushabu/javashop/products/resources/ProductResource.java
```

search for 999 `/999`

We found and fixed the Needle In Haystack more quickly! Let's fix our code, enter `i` for insert.

Change this:

``` java
private void myCoolFunction234234234(@SpanAttribute("myInt") int myInt) {
    // Generate a FAST sleep of 0 time !
    Random sleepy = new Random();
    try{
        if (999==myInt)
            Thread.sleep(sleepy.nextInt(5000 - 3000)  + 3000);
    } catch (Exception e){
```

To this:

``` java
private void myCoolFunction234234234(@SpanAttribute("myInt") int myInt) {
    // Generate a FAST sleep of 0 time !
    Random sleepy = new Random();
    try{
    //    if (999==myInt)
    //        Thread.sleep(sleepy.nextInt(5000 - 3000) + 3000);
    } catch (Exception e){
```

Save changes in vi type `:wq`

Make sure you saved your changes to: `products/src/main/java/com/shabushabu/javashop/products/resources/ProductResource.java`
