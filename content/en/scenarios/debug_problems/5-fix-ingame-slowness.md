---
title: Fix In Game Slowness
linkTitle: 5.5 Fix In Game Slowness
weight: 5
---

{{% badge icon="clock" color="#ed0090" %}}10 minutes{{% /badge %}}

Now that our game startup slowness has been resolved, let's play several rounds of the Door Game and ensure the rest of the game performs quickly. 

As you play the game, do you notice any other slowness?  Let's look at the data in **Splunk Observability** Cloud to put some numbers on what we're seeing. 

### Review Game Performance in Splunk Observability Cloud

Navigate to APM then click on Traces on the right-hand side of the screen. Sort the traces by Duration in descending order: 

![Slow Traces](../images/slow_trace.png)

We can see that a few of the traces with an operation of `GET /game/:uid/picked/:picked/outcome` have a duration of just over five seconds. This explains why we're still seeing some slowness when we play the app (note that the slowness is no longer on the game startup operation, `GET /new-game`, but rather a different operation used while actually playing the game). 

Let's click on one of the slow traces and take a closer look. Since profiling is still enabled, call stacks have been captured as part of this trace. Click on the child span in the waterfall view, then click CPU Stack Traces: 

![View Stack on Span](../images/view_stack_on_span.png)

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

* We found another performance issue with our application that impacts game play. 
* We used the CPU call stacks included in the trace to understand application behavior. 
* We learned how the call stack can tell us a story and point us to suspect lines of code.
* We identified the slow code and fixed it to make it faster.
