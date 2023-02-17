---
title: 6. O11y - Distributed Tracing for modern applications
linkTitle: Module 1
weight: 2
alwaysopen: false
---

## Set Environment Variables

Environment Variables:

Using nano edit .env in `javashop-otel` directory

``` bash
nano .env
```

``` ini
SHOP_USER=<your_name>

SPLUNK_ACCESS_TOKEN=<your_token>

SPLUNK_REALM=<your_realm>
```

Save in nano

CTRL-O ENTER

Exit nano

CTRL-X

## Build and Deploy Application

Let's get started by building and deploying our Application, the Buttercup Instrument Shop. Run the commands below to begin and start reading ahead as your traces are coming up !

``` bash
cd javashop-otel

./BuildAndDeploy.sh
```

## Users and Workflows

As we go through this workshop we will be switching roles from SRE to Developer.  First we will start with alert responders or SREs who will identify an issue in Splunk Observability UI.  Next, we will jump to a Developer Role to see how a Developer will debug and repair/fix a software problem using trace data provided by our SRE.

Of course, we are not requiring 2 people for this workshop as each participant will play both roles.

## Today we will learn

Today we will learn the type of data ( In the form of a trace ) that an SRE or alert responder would send to a developer to then repair/fix software. We will do this with both Auto-Instrumentation data and Custom attributes, via Manual Instrumentation data.

While we will be spending time Debugging code, .... Don't worry, ...there is no programming experience necessary, as our goal here is for everyone in the audience to understand how using Custom Attributes in Splunk APM @ Full Fidelity can accelerate Mean Time to Repair Software problems for our customers.

Translated, Developers are High Cost resources, with high opportunity cost. Less time on fixing problems = more time for features.

## Let's define a few terms for those new to APM / Software Development or Java

1. What's a Function in Java ?
   A Function  in most languages including Java, is a logical chunk of code when executed that solves a repeatable task. This is basically what our customers' Dev teams spend their time building and where software issues will most commonly be.
2. What's a  Method in Java ?
   See What's a function -> Function and method are synonymous.
3. What's an Exception in Java ?
   An Exceptional error condition that indicates abnormal or unhandled condition, that interrupts program execution abnormally.

## View Service Map

Please note it may take 3-4 minutes for traces to show up and you will see full map "form" as traces are coming in, so you may have to refresh the page a few times each time we Build and Deploy.

It is recommended to use a -5m look back during this lab. Start there, use 15 if you feel you have to.

![Service Map](https://user-images.githubusercontent.com/32849847/218923108-6c6a7efb-588e-4f7b-b788-768037eae4bb.png)

{{% notice title="NOTE" style="note" %}}
Typically, to identify root cause and route an issue, an SRE or alert responder would check metrics and logs to determine if it is a software or hardware related issue, and thus route to the correct party. In this exercise we are ONLY handling software issues, so we are skipping the metrics and logs parts of normal triage.
{{% /notice %}}

If your instrumentation was successful, the service-map will show latency from the shop service to the products service.

![Screen Shot 2022-12-08 at 11 48 58 AM](https://user-images.githubusercontent.com/32849847/206541846-7f0e6462-7659-44bc-bc48-3621c2872fc4.png)

Ok let's triage this SOFTWARE ISSUE and skip directly to the traces.

- Click on shop service
- Click Traces ( right side )
- Sort by Duration

Select the longest duration trace ( or one of the obvious much longer ones )

![LongTrace](https://user-images.githubusercontent.com/32849847/204347798-4f232b7f-7a7a-483f-9d61-f0b535e9ecf0.png)

Now we can see the long latency occurred in the products service and if we click on products: /products
we can see the offending method was products:ProductResource.getAllProducts

![long-trace-detail-GetAllProducts](https://user-images.githubusercontent.com/32849847/204347855-724545bf-c3df-478a-a27d-e4f85f708e15.png)

Our next step here would be to send that trace to a developer by clicking download trace and
they will have to debug the function. Since we will be the developer there is no need to download the trace. Just remember that is normal workflow for alert responders to route an issue to the "Repairers" while providing trace data.

Before we do that please take note of the Tags available for the developer to leverage to find the root cause. We see standard out of the box Otel tags on the span, environmental information, but no indications of data specific to something inside custom code ( which is where the problem always is. )

## Now let's play the role of the developer

As a developer we must debug the function products:ProductResource.getAllProducts to find the problem.

## Debugging 101, the Line by Line method

Without anything to go on other than "BAD FUNCTION", a Developer must then look at code visually line by line to find and fix the problem. To make this worse, Functions, call Functions and it can get very messy in bad code scenarios.

We will do the visual inspection method next.

Using Nano:

```bash
nano products/src/main/java/com/shabushabu/javashop/products/resources/ProductResource.java
```

Search in Nano
CTRL-W

Enter in: getAllProducts

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

We can see here in getAllProducts, the first call is to myCoolFunction1(), so as may have guessed our next step is to go look at myCoolFunction1()

Search in Nano
CTRL-W

Enter in: myCoolFunction1

CTRL-W

Enter in: ENTER  

Keep doing that until you get to the actual function definition, it looks like this:

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

Now, myCoolFunction1 calls lookupLocation1(location)

Search in Nano
CTRL-W

Enter in: lookupLocation1

I think you get the picture by now, you have no choice but to inspect every line of code and every function called and visually inspect them for problems. This can be a VERY long process and kills our customers Mean time to Repair. This happens quite often to our customers with our competition because they can't provide all the traces 100% of the time and most can't scale to add more data, via Custom Attributes on top of that !

Remember, without Full Fidelity, you have to either reproduce errors / latency in another environment or inspect code line by line.

So they are stuck where we are, quite often.

OK, enough fun ..let's make this easier for our developer... and show off some Splunk APM Scale!

OK, exit your editor:

Edit nano CTRL-X ( DO NOT SAVE IF MODIFIED )

## Custom Attribution

To take a deeper look at this issue and make this much easier to debug we will implement Custom Attributes via Opentelemetry Manual Instrumentation.

To speed up manual instrumentation in Java you can leverage [OpenTelemetry Annotations](https://opentelemetry.io/docs/instrumentation/java/automatic/annotations/ ), which automatically create a span around a method without modifying the actual code inside the method. This can be very valuable if you are working with an SRE that may have limited access to source code changes.

To add even more information to help our developers find the root cause faster,
[OpenTelemetry Annotations](https://opentelemetry.io/docs/instrumentation/java/automatic/annotations/ ) can be used to generate span tags with parameter values for the method in question. This is incredibly important to mean time to Repair, because as a Developer, if I know the parameter values of a function at the time of latency or error, I can debug this without having to reproduce an issue in another environment if I have Full Fidelity Tracing.

Splunk Full Fidelity APM allows our customers' development teams to debug their code as it runs in production, 100% of the time . With Custom Attribution, you are providing repeatable Mean Time to Repair reduction...  100% of the time, only with Full Fidelity tracing.

To expedite manual instrumentation implementation for this exercise, we have provided a tool which will annotate the entirety of the "shop" and "products" services with OpenTelemetry standard annotations for every method call without having to write any code. This "annotator" tool will also tag every parameter in every function, which adds a span tag with Parameter=Value.

## Run Manual Instrumentation Tool

``` bash
cd javashop-otel directory

./AutomateManualInstrumentation.sh
```

## Rebuild and Deploy Application

``` bash
./BuildAndDeploy.sh
```

Now that we have rebuilt and deployed our application, traffic is being sent once again.

Go back to the Splunk Observability UI and let's see if these annotations help us narrow down the root cause more quickly.

Let's try to find our latency root cause again, this time with every function and every parameter spanned and tagged respectively.... You will see exactly what this means and how it benefits developers in a moment...

![Screen Shot 2022-12-08 at 11 48 58 AM](https://user-images.githubusercontent.com/32849847/206541846-7f0e6462-7659-44bc-bc48-3621c2872fc4.png)

- Click on shop service
- Click Traces ( right side )
- Sort by Duration

Select the longest duration trace ( or one of the obvious much longer ones )

![image](https://user-images.githubusercontent.com/32849847/213582624-66466a19-00fa-4dda-acd0-f6970d594ba1.png)

We can see that the actual function call that has the latency was not ProductResource.getAllProducts but the function call "ProductResource.myCoolFunction234234234" !

Since we now have the parameter tagged as part of our span metadata the actual root cause is seemingly related to the  "location" Colorado ! And it appears the one custom attribute that was tagged for the function "ProductResource.myCoolFunction234234234" was "myInt" with a value of 999. With this information a Developer can debug very quickly.

Consider the case of debugging code which each of you have just experienced. Imagine that you may have not written the code yourself and the code is a mess, which I can tell you from a former developer, everyone else's code sucks.... So without Parameter Values at the time of the issue .. You would have no choice but to go line .... by line ..... by line..... which I am sorry I forced you to do earlier... this can take a very long time.

{{% notice title="NOTE" style="note" %}}
We added additional span information, which we call "Custom Attributes" here at Splunk, in this case our "Custom Attributes" are "Parameter Values at Time of Latency".
{{% /notice %}}

In our example  the "Location" tag was created due our handy Annotator, that did the [OpenTelemetry Annotations](https://opentelemetry.io/docs/instrumentation/java/automatic/annotations/ ) for us.

Using nano:

``` bash
nano products/src/main/java/com/shabushabu/javashop/products/resources/ProductResource.java
```

Search in Nano
CTRL-W

Enter in: 999

We can see here,  someone wrote some very bad code in the form of a long Sleep !

``` java
if (999==myInt)

Thread.sleep(

sleepy.nextInt(5000 - 3000) + 3000);

)
```

## How did we get here ? How did the 999 end up in the trace as a Custom Attribute ?

Take a look at the function signature

private void myCoolFunction234234234(@SpanAttribute("myInt") int myInt)

@SpanAttribute("myint") is an Opentelemetry Java Annotation that was added by our Java Otel Annotator tool.

Let's fix our code.

Change this:

``` java
private void myCoolFunction234234234(@SpanAttribute("myInt") int myInt) {

// Generate a FAST sleep of 0 time !
Random sleepy = new Random();
try{

if (999==myInt)

Thread.sleep(

sleepy.nextInt(5000 - 3000)

+ 3000);

} catch (Exception e){
```

To this:

``` java
private void myCoolFunction234234234(@SpanAttribute("myInt") int myInt) {

// Generate a FAST sleep of 0 time !
Random sleepy = new Random();
try{

// if (999==myInt)

//  Thread.sleep(

//  sleepy.nextInt(5000 - 3000)

//  + 3000);

} catch (Exception e){

```

Using nano

place comments before every line in myCoolFunction234234234

``` java
// if (999==myInt)

//  Thread.sleep(

//  sleepy.nextInt(5000 - 3000)

//  + 3000);
```

Write out changes in nano

CTRL-O

CTRL-X to exit.

Make sure you saved your changes to:  products/src/main/java/com/shabushabu/javashop/products/resources/ProductResource.java

## Let's go see if our manual instrumentation uncovered any other issues we did not see before

So you may be asking yourself, "How does manual instrumentation alone show us "more problems" than before latency is latency is it ?

The answer is, with auto-instrumentation you are in most situations NOT covering functions our customers' development teams wrote, which is of course the bulk of what developers do, they write functions.... and of course this is where the  bulk of  software problems occur.

You may have noticed a new exception in our trace that was not present with Auto-Instrumentation during our latency fix use-case. Since we skipped over this,  let's walk you through it.

Return to the service map

- Click on shop service
- Click Traces ( right side )
- Select "Errors Only"

![Screen Shot 2022-11-28 at 7 36 50 AM](https://user-images.githubusercontent.com/32849847/204348492-84a4ad45-e11c-4e75-a6a9-d6e52e0eb13e.png)

Note: we haven't changed the code at all by adding annotations.

Click on a trace with an error present

![Screen Shot 2022-11-28 at 7 38 33 AM](https://user-images.githubusercontent.com/32849847/204348687-12241153-b297-4bd7-9ea8-4b410369e82c.png)

We can see our Exception is InvalidLocaleException !

The real problem must be related to the new data associated with SRI LANKA as the Exception says "Non English Characters found in Instrument Data.

This exception had not surfaced in previous traces based on ONLY Auto-Instrumentation because the method where it was thrown was NOT covered with Auto-Instrumentation.

Once we completed the Manual Instrumentation via the Otel Annotator, this method was instrumented  and we can now see we had a buried Exception being thrown.

## Let's play Developer once again and fix our issue

We already know exactly what file to look in and what method to look at as it is called out in the trace.

![Screen Shot 2022-11-28 at 7 43 58 AM](https://user-images.githubusercontent.com/32849847/204349038-3b43a5ba-18e3-4d58-8985-29ee1f7da40a.png)

Edit the file

Using nano

``` bash
nano shop/src/main/java/com/shabushabu/javashop/shop/model/Instrument.java
```

Search in Nano
CTRL-W

Enter in: buildForLocale

Look just above the buildForLocale function, notice the Annotation @WithSpan? @WithSpan is an [OpenTelemetry Annotation](https://opentelemetry.io/docs/instrumentation/java/automatic/annotations/ ) for Java that automatically generates a span around the function that follows.

![Screen Shot 2022-11-28 at 7 45 13 AM](https://user-images.githubusercontent.com/32849847/204349143-1e35b6e4-4059-4c56-8718-76c14d41727c.png)

Now let's fix this code. We are going to simply comment this out for now and see if it fixes our latency issue.

Using nano

Place comments in front of the entire if statement as follows:

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

//  System.out.println("Characters OK ");

//}
```

Save Changes in nano

CTRL-O

Exit nano

CTRL-X

Make sure you saved your changes to shop/src/main/java/com/shabushabu/javashop/shop/model/Instrument.java

## Rebuild and Deploy Application

``` bash
./BuildAndDeploy.sh
```

We are waiting a few minutes...

Return to the service map

If you do NOT see RED in your service map, you have completed the Latency Repair for the Colorado Location !

Now let's check for our exception in the traces.

- Click on shop service
- Click Traces ( right side )
- Select "Errors Only"

If you do not have red in your service map and you do not see Errors in traces, you have successfully completed our Inventory application review for Sri Lanka and Colorado locations!!

## We are nearly done, one more location to go... Chicago

Last but not least, let's ensure Chicago was on-boarded correctly. However, since we have been having so many issues related to "location" and we have added that custom attribute via Opentelemetry Manual Instrumentation, let's go to the Splunk Observability UI and look at an APM metric set around that tag that I created for us.

![image](https://user-images.githubusercontent.com/32849847/213540265-5b0567ab-c9f3-412f-bec0-07277c7e8650.png)

Open a browser and navigate to <http://localhost:8010>

Select a few locations and hit the login button, remember to select the Chicago Location and Login

![image](https://user-images.githubusercontent.com/32849847/213541843-30266285-787f-493b-bc90-ffb4ac6e4c77.png)

Uhh ohh ! We received a 500 error, something is wrong there as well.

![Screen Shot 2022-11-28 at 8 11 47 AM](https://user-images.githubusercontent.com/32849847/204349595-fca270ad-379e-48c5-b2e1-7f222af82c55.png)

Return to the Splunk Observability UI and lets look once again at our Service Map, select the Instruments Service and click the breakdowns on the right and select "location"

![image](https://user-images.githubusercontent.com/32849847/214941419-2eaae297-e246-460b-a913-28c2a28fcd6a.png)

We see there was an un-handled exception thrown in Instruments service and some latency from our database that is related to the Chicago location !

- Click on Traces on the right
- Select "Errors Only"

![Screen Shot 2022-11-28 at 8 14 50 AM](https://user-images.githubusercontent.com/32849847/204349696-dc19d62f-ed82-4533-ad27-138237821b8e.png)

We can see the exception was thrown by Hibernate, however it was thrown in our method "instruments: InstrumentRepository.findInstruments"

![Screen Shot 2022-11-28 at 8 14 37 AM](https://user-images.githubusercontent.com/32849847/204351905-03fe632b-b21c-4e8d-8044-dc582fed2253.png)

## Let's play developer again

Edit the file "instruments: InstrumentRepository.findInstruments"

Using nano

``` bash
nano instruments/src/main/java/com/shabushabu/javashop/instruments/repositories/FindInstrumentRepositoryImpl.java
```

![Screen Shot 2022-11-28 at 8 20 24 AM](https://user-images.githubusercontent.com/32849847/204349802-06135d9d-d70b-4cf1-aaea-3ba737e5c2b9.png)

We can see the developer accidently added the Instruments database with the Chicago Instruments database !

Let's change the query and fix this, remove "instruments_for_sale" from our Query

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
// public Object findInstruments() {
//   LOGGER.info("findInstruments Called (All)");

//   Object obj = entityManager.createNativeQuery( "SELECT * FROM instruments_for_sale_chicago").getResultList(); 

//  return obj;
//}
```

Save Changes in nano

CTRL-O

Exit nano

CTRL-X

### Build and Deploy Application

``` bash
cd javashop-otel directory

./BuildAndDeploy.sh
```

Now let's test the Chicago location once again

- Open a browser and navigate to <http://localhost:8010>
- Select the Chicago Location and Login

We now see the 500 error is gone! Let's confirm a clean Service Map

![Screen Shot 2022-11-28 at 8 35 11 AM](https://user-images.githubusercontent.com/32849847/204350088-fca43e3c-42ea-4933-8a61-01eb2083fd23.png)

If you see a clean service map, free of errors and Latency you have successfully completed the Java Instrumentation Workshop!

**Have a lovely day.**
