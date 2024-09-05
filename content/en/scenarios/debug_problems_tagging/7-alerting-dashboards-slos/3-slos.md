---
title: Use Tags with Service Level Objectives
linkTitle: 3. ...with SLOs
weight: 3
time: 10 minutes
---

We can now use the created Monitoring MetricSet together with Service Level Objectives a similar way we used them with dashboards and detectors/alerts before. For that we want to be clear about some key concepts:

## Key Concepts of Service Level Monitoring

([skip](#creating-a-new-service-level-objective) if you know this)

|Concept|Definition|Examples|
|---|---|---|
|Service level indicator (SLI)|An SLI is a quantitative measurement showing some health of a service, expressed as a metric or combination of metrics.|*Availability SLI*: Proportion of requests that resulted in a successful response<br>*Performance SLI*: Proportion of requests that loaded in < 100 ms|
|Service level objective (SLO)|An SLO defines a target for an SLI and a compliance period over which that target must be met. An SLO contains 3 elements: an SLI, a target, and a compliance period. Compliance periods can be calendar, such as monthly, or rolling, such as past 30 days.|*Availability SLI over a calendar period*: Our service must respond successfully to 95% of requests in a month<br>*Performance SLI over a rolling period*: Our service must respond to 99% of requests in < 100 ms over a 7-day period|
|Service level agreement (SLA)|An SLA is a contractual agreement that indicates service levels your users can expect from your organization. If an SLA is not met, there can be financial consequences.|A customer service SLA indicates that 90% of support requests received on a normal support day must have a response within 6 hours.|
|Error budget|A measurement of how your SLI performs relative to your SLO over a period of time. Error budget measures the difference between actual and desired performance. It determines how unreliable your service might be during this period and serves as a signal when you need to take corrective action.|Our service can respond to 1% of requests in >100 ms over a 7 day period.|
|Burn rate|A unitless measurement of how quickly a service consumes the error budget during the compliance window of the SLO. Burn rate makes the SLO and error budget actionable, showing service owners when a current incident is serious enough to page an on-call responder.|For an SLO with a 30-day compliance window, a constant burn rate of 1 means your error budget is used up in exactly 30 days.|

## Creating a new Service Level Objective

There is an easy to follow wizard to create a new Service Level Objective (SLO). In the left navigation just follow the link "**Detectors & SLOs**". From there select the third tab "**SLOs**" and click the blue button to the right that says "**Create SLO**".

![Create new SLO](../../images/slo_0_create.png)

The wizard guides you through some easy steps. And if everything during the previous steps worked out, you will have no problems here. ;)

In our case we want to use `Service & endpoint` as our **Metric type** instead of `Custom metric`. We filter the **Environment** down to the environment that we are using during this workshop (i.e. `tagging-workshop-yourname`) and select the `creditcheckservice` from the **Service and endpoint** list. Our **Indicator type** for this workshop will be `Request latency` and not `Request success`.

Now we can select our **Filters**. Since we are using the `Request latency` as the **Indicator type** and that is a metric of the APM Service, we can filter on `credit.score.category`. Feel free to try out what happens, when you set the **Indicator type** to `Request success`.

Today we are only interested in our `exceptional` credit scores. So please select that as the filter.

![Choose Service or Metric for SLO](../../images/slo_1_choose.png)

In the next step we define the objective we want to reach. For the `Request latency` type, we define the **Target (%)**, the **Latency (ms)** and the **Compliance Window**. Please set these to `99`, `100` and `Last 7 days`. This will give us a good idea what we are achieving already.

Here we will already be in shock or play around with the numbers to make it not so scary. Feel free to play around with the numbers to see how well we achieve the objective and how much we have left to burn.

![Define Objective for SLO](../../images/slo_2_define_objective.png)

The third step gives us the chance to alert (aka annoy) people who should be aware about these SLOs to initiate countermeasures. These "people" can also be mechanism like ITSM systems or webhooks to initiate automatic remediation steps.

Activate all categories you want to alert on and add recipients to the different alerts.

![Define Alerting for SLO](../../images/slo_3_define_alerting.png)

The next step is only the naming for this SLO. Have your own naming convention ready for this. In our case we would just name it `creditchceckservice:score:exceptional:YOURNAME` and click the **Create**-button **BUT** you can also **just cancel the wizard** by clicking anything in the left navigation and confirming to **Discard changes**.

![Name and Save the SLO](../../images/slo_4_name_and_save.png)

And with that we have (*nearly*) successfully created an SLO including the alerting in case we might miss or goals.
