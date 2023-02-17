---
title: Fix the issue
linkTitle: Fix the issue
weight: 6
draft: true
---

## 1. Let's play Developer once again and fix our issue

We already know exactly what file to look in and what method to look at as it is called out in the trace.

![Screen Shot 2022-11-28 at 7 43 58 AM](https://user-images.githubusercontent.com/32849847/204349038-3b43a5ba-18e3-4d58-8985-29ee1f7da40a.png)

Edit the file

``` bash
vi shop/src/main/java/com/shabushabu/javashop/shop/model/Instrument.java
```

Search for the method buildForLocale `/buildForLocale`

Look at Code, notice the Annotation `@WithSpan()`? `@WithSpan()` is an [OpenTelemetry Annotation](https://opentelemetry.io/docs/instrumentation/java/automatic/annotations/) for Java that automatically generates a span around a the function that follows.

`@SpanAttribute()` is another [OpenTelemetry Annotation](https://opentelemetry.io/docs/instrumentation/java/automatic/annotations/) that automatically adds a tag to a span with the corresponding parameter it annotates and its value. Using this technique we can tell developers exactly what the values of every parameter of a function the wrote or must repair at the time the problem occurred.

 ![Screen Shot 2022-11-28 at 7 45 13 AM](https://user-images.githubusercontent.com/32849847/204349143-1e35b6e4-4059-4c56-8718-76c14d41727c.png)

Now let's fix this code. We are going to simply comment this out for now and see if it fixes our latency issue. Type `i` for insert

Change this:

``` java
if (!isEnglish(title)) {
  throw new InvalidLocaleException("Non English Characters found in Instrument Data");
 } else {
 System.out.println("Characters OK ");
}
```

To this:

``` java
//if (!isEnglish(title)) {
//  throw new InvalidLocaleException("Non English Characters found in Instrument Data");
// } else {
// System.out.println("Characters OK ");
//}
```

To save changes in vi type `:wq`

Make sure you saved your changes to `shop/src/main/java/com/shabushabu/javashop/shop/model/Instrument.java`

## 2. Build and Deploy Application

``` bash
./BuildAndDeploy.sh
```

Wait a few minutes.....
