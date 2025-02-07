---
title: Creating Basic Alerts
linkTitle: 2. Creating Basic Alerts
weight: 1
---

# Setting Up Basic Alerts in Splunk Enterprise, AppDynamics, and Splunk Observability Cloud

This section covers the creation of basic alerts in Splunk Enterprise, AppDynamics, and Splunk Observability Cloud.  These examples focus on simplicity and demonstrating the core concepts.  Remember that real-world alerting scenarios often require more complex configurations and thresholds.

## 1. Splunk Enterprise Alerts

Splunk alerts are triggered by search results that match specific criteria. We'll create a real-time alert that notifies us when a certain condition is met.

**Scenario:**  Alert when the number of "error" events in the "application_logs" index exceeds 10 in the last 5 minutes.

**Steps:**

1. **Create a Search:** Start by creating a Splunk search that identifies the events you want to alert on. For example:

   ```splunk
   index=application_logs level=error
   ```
    Use the time picker to select "Relative" and set the timespan to 10.

2. **Configure the Alert:**
   * Click "Save As" and select "Alert."
   * Give your alert a descriptive name (e.g., "Application Error Alert").
   * **Trigger Condition:**
      * **Scheduled:** Choose "Scheduled" to evaluate the search on a set schedule. Below scheduled will be the button to select the frequency, select "Run on Cron Schedule". If the time Range below that is different than 10 minutes, update it.
      * **Triggered when:** Select "Number of results" "is greater than" "10."
      * **Time Range:** Set to "5 minutes."
   * **Trigger Actions:**
      * For this basic example, choose "Add to Triggered Alerts."  In a real-world scenario, you'd configure email notifications, Slack integrations, or other actions.
   * **Save:** Save the alert.

**Explanation:** This alert runs the search every 10 minutes and triggers if the search returns more than 10 results. The "Add to Triggered Alerts" action simply adds a Alert to the Splunk Triggered Alerts list.

**Time Ranges and Frequency:** Since everything in Splunk core is a search, you need to consider the search timespan and frequency so that you are not a) searching the same data multiple times with an overlap timespan, b) missing events because of a gap between timespan and frequency, c) running too frequently and adding overhead or d) running too infrequently and experiencing delays in alerting.


## 2. AppDynamics Alerts (Health Rule Violations)

**2. Create a Health Rule (or modify an existing one):**
   * Click "Create Rule" (or edit an existing rule that applies to your application).
   * Give the health rule a descriptive name (e.g., "Order Service Response Time Alert").
   * **Scope:**  Select the application and tier (e.g., "OrderService").
   * **Conditions:**
      * Choose the metric "Average Response Time."
      * Set the threshold: "is greater than" "500" "milliseconds."
      * Configure the evaluation frequency (how often AppDynamics checks the metric).
   * **Actions:**
      * For this basic example, choose "Log to console."  In a real-world scenario, you would configure email, SMS, or other notification channels.
   * **Save:** Save the health rule.

**Explanation:** This health rule continuously monitors the average response time of the "OrderService." If the response time exceeds 500ms, the health rule is violated, triggering the alert and the configured actions.


## 3. Splunk Observability Cloud Alerts (Detectors) (Continued)

**2. Create a Detector:**
   * Click "Create Detector."
   * Give the detector a descriptive name (e.g., "High CPU Utilization Alert").
   * **Signal:**
      * Select the metric you want to monitor (e.g., "host.cpu.utilization").  Use the metric finder to locate the correct metric.
      * Add any necessary filters to specify the host (e.g., `host:my-hostname`).
   * **Condition:**
      * Set the threshold: "is above" "80" "%."
      * Configure the evaluation frequency and the "for" duration (how long the condition must be true before the alert triggers).
   * **Notifications:**
      * For this example, choose a simple notification method (e.g., a test webhook). In a real-world scenario, you would configure integrations with PagerDuty, Slack, or other notification systems.
   * **Save:** Save the detector.

**Explanation:** This detector monitors the CPU utilization metric for the specified host.  If the CPU utilization exceeds 80% for the configured "for" duration, the detector triggers the alert and sends a notification.

**Important Considerations for All Platforms:**

* **Thresholds:** Carefully consider the thresholds you set for your alerts.  Too sensitive thresholds can lead to alert fatigue, while thresholds that are too high might miss critical issues.
* **Notification Channels:**  Integrate your alerting systems with appropriate notification channels (email, SMS, Slack, PagerDuty) to ensure that alerts are delivered to the right people at the right time.
* **Alert Grouping and Correlation:**  For complex systems, implement alert grouping and correlation to reduce noise and focus on actionable insights.  ITSI plays a critical role in this.
* **Documentation:** Document your alerts clearly, including the conditions that trigger them and the appropriate response procedures.

These examples provide a starting point for creating basic alerts.  As you become more familiar with these platforms, you can explore more advanced alerting features and configurations to meet your specific monitoring needs.
