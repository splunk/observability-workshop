# uAPM troubleshooting - Hot R.O.D.- Lab Summary

* Explore troubleshooting and dependencies interface in uAPM
* Use the Breakdown feature to enrich the troubleshooting info
* Examine a trace in waterfall mode

!!! note "Ensure you have a running instance that has the hot R.O.D app running"
    The setup part is already documented in the [Preparation](../../smartagent/prep/), [Deploy the Smart Agent in K3s](../../smartagent/k3s/) and [Deploying hot-rod in K3s](../../apm/hotrod/) steps. If you are using an AWS/EC2 instance, make sure it is available and skip to [Step 1](../../apm/hotrod/#1-find-a-specific-trace-using-time-slots-andor-tags), otherwise ensure your Multipass instance is available and running before continuing.

    === "Shell Command"

        ```
        multipass list
        ```

    === "Example Output"

        ```
        Name                     State             IPv4             Image
        vmpe-k3s                 Running           192.168.64.17    Ubuntu 18.04 LTS
        ```

---

## 1. Find a problematic traces using dependencies and/or tags

For this use case we assume there is an intermittent problem but we do not have a clear time frame for the occurrence. This is the very the case when a working on a performance problem. or edge cases,
Using the Analytic engine of SignalFx, combined with using tags and/or services selections, we can find relevant traces, and dive into them to explore.

### 1.1 Select Application Environment

First, we need to know the name of your application environment.
In this workshop all the environments use your `{==hostname==}-apm-env`

To find the hostname, check the prompt of you instance, please go to your
instance (Multipass or EC2) and run the following command.

=== "Shell Command"

    ```text
    echo "Your µAPM environment is: $(hostname)-apm-env"
    ```

=== "Example Multipass Output"

    ```text
    Your µAPM environment is: vmpe-apm-env
    ```

=== "Example AWS/EC2 Output"

    ```text
    Your µAPM environment is: ip-172-31-30-133-apm-env

    ```

Open SignalFx in your browser and select the **µAPM** tab.

![select APM](../images/apm/select-apm.png){: .zoom}

Select the **Troubleshooting** tab, and select your environment you found and set the time to 1 hour. This will show you the automatically generated Dependency Map for the Hot R.O.D. application.

In the scenario we are working with, we have been told that we get intermittent errors in the front end service, but not much more , so we need to discover what is going on.

So the first activity for identifying the issue, is to pre-select both the  front-end service and follow the dependencies.

---

## 2. Explore the troubleshooting and dependencies view

---

## 3. Use the breakdown feature to enrich troubleshooting info
