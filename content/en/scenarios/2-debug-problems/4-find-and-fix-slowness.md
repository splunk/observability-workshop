---
title: Find and Fix Application Slowness
linkTitle: 5.4 Find and Fix Application Slowness
weight: 4
---

In this section, we pick up where we left off last time.
We will use the profiling tool to explore our slow span and link it
back to the source code that caused the slowness. We will update the code to improve
the performance of this span, and we will use the APM profiling tools to verify
that our change is successful.

### Exploring the Span

At the end of the previous section, we have identified a span that was taking more
than 5 seconds to complete. We observed that the span showed that it was linked
to 2 or more sampled call stacks. Let's proceed by clicking on the span to expand its details.

![View Stack on Span](../images/view_stack_on_span.png)

When a span does not have CPU call stack data, we would normally just see the span details.
(you can drill into the parent stack to see this in action). When we expand the child span, however,
we have the option to see "CPU Call Stack" data as well.

At the bottom of the call stack, we can see that the thread was busy sleeping:

``` log
com.splunk.profiling.workshop.ServiceMain$$Lambda$.handle(Unknown Source:0)
com.splunk.profiling.workshop.ServiceMain.lambda$main$(ServiceMain.java:34)
com.splunk.profiling.workshop.DoorGame.getOutcome(DoorGame.java:41)
com.splunk.profiling.workshop.DoorChecker.isWinner(DoorChecker.java:14)
com.splunk.profiling.workshop.DoorChecker.checkDoorTwo(DoorChecker.java:30)
com.splunk.profiling.workshop.DoorChecker.precheck(DoorChecker.java:36)
com.splunk.profiling.workshop.Util.sleep(Util.java:9)
java.util.concurrent.TimeUnit.sleep(Unknown Source:0)
java.lang.Thread.sleep(Unknown Source:0)
java.lang.Thread.sleep(Native Method:0)
```

The call stack tells us a story -- reading from the bottom up, it lets us describe
what is happening inside the service code. A developer, even one unfamiliar with the
source code, should be able to look at this call stack to craft a narrative like:
> We are getting the outcome of a game. We leverage the DoorChecker to
> see if something is the winner, but the check for door two somehow issues
> a precheck() that, for some reason, is deciding to sleep for a long time.

Our workshop application is left intentionally simple -- a real-world service might see the
thread being sampled during a database call or calling into an un-traced external service.
It is also possible that a slow span is executing a complicated business process,
in which case maybe none of the stack traces relate to each other at all.

The longer a method or process is, the greater chance we will have call stacks
sampled during its execution.

### Let's Fix That Bug

By using the profiling tool, we were able to determine that our application is slow
when issuing the `DoorChecker.precheck()` method from inside `DoorChecker.checkDoorTwo()`.
Let's open the `doorgame/src/main/java/com/splunk/profiling/workshop/DoorChecker.java` source file in our editor.

By quickly glancing through the file, we see that there are methods for checking
each door, and all of them call `precheck()`. In a real service, we might be uncomfortable
simply removing the `precheck()` call because there could be unseen/unaccounted side
effects.

Down on line 29 we see the following:

``` java
    private boolean checkDoorTwo(GameInfo gameInfo) {
        precheck(2);
        return gameInfo.isWinner(2);
    }

    private void precheck(int doorNum) {
        long extra = (int)Math.pow(70, doorNum);
        sleep(300 + extra);
    }
```

With our developer hat on, we notice that the door number is zero based, so
the first door is 0, the second is 1, and the 3rd is 2 (this is conventional).
The `extra` value is used as extra/additional sleep time, and it is computed by taking
`70^doorNum` (`Math.pow` performs an exponent calculation). That's odd, because this means:

* door 0 => 70^0 => 1ms
* door 1 => 70^1 => 70ms
* door 2 => 70^2 => 4900ms

We've found the root cause of our slow bug! This also explains why the first two doors
weren't ever very slow.

We have a quick chat with our product manager and team lead, and we agree that the `precheck()`
method must stay but that the extra padding isn't required. Let's remove the `extra` variable
and make `precheck` now read like this:

```java
    private void precheck(int doorNum) {
        sleep(300);
    }
```

Now all doors will have a consistent behavior. Save your work and then rebuild and redeploy the application using the following command:

``` bash
cd workshop/profiling
./5-redeploy-doorgame.sh
```

Once the application has been redeployed successfully, visit The Door Game again to confirm that your fix is in place:
`http://<your IP address>:81`

## What did we accomplish?

* We learned how to view a series of call stacks captured during a Span.
* We learned how the call stack can tell us a story and point us to suspect lines of code.
* We identified the slow code and fixed it to make it faster.

In the next section, we'll explore how to enable the memory profiling component of AlwaysOn Profiling, which can tell us which objects are consuming the most heap memory.
