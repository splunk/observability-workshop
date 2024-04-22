---
title: Database Query Performance
linkTitle: 3. Database Query Performance
weight: 3
---

With Database Query Performance, you can monitor the impact of your database queries on service availability directly in Splunk APM. This way, you can quickly identify long-running, unoptimized, or heavy queries and mitigate issues they might be causing, without having to instrument your databases.

To look at the performance of your database queries, make sure you are on the APM **Explore** page either by going back in the browser or navigating to the APM section in the Menu bar, then click on the **Explore** tile.
Select the inferred database service `mysql:petclinic` Inferred Database server in the Dependency map **(1)**, then scroll the right-hand pane to find the **Database Query Performance** Pane **(2)**.

![DB-query from map](../../images/db-query-map.png)

If the service you have selected in the map is indeed an (inferred) database server, this pane will populate with the top 90% (P90) database calls based on duration. To dive deeper into the db-query performance function click somewhere on the word **Database Query Performance** at the top of the pane.

This will bring us to the DB-query Performance overview screen:

![DB-query full](../../images/db-query-full.png)

{{% notice title="Database Query Normalization" style="info" %}}
By default, Splunk APM instrumentation sanitizes database queries to remove or mask sensible data, such as secrets or personally identifiable information (PII) from the `db.statements`. You can find how to turn off database query normalization [here](https://docs.splunk.com/observability/en/apm/db-query-perf/db-perf-troubleshooting.html#turn-off-database-query-normalization).
{{% /notice %}}

This screen will show us all the Database queries **(1)** done towards our database from your application, based on the Traces & Spans sent to the Splunk Observability Cloud.  Note that you can compare them across a time block or sort them on Total Time, P90 Latency & Requests **(2)**.

For each Database query in the list, we see the highest latency, the total number of calls during the time window and the number of requests per second **(3)**. This allows you to identify places where you might optimize your queries.

You can select traces containing Database Calls via the two charts in the right-hand pane **(5)**. Use the Tag Spotlight pane **(6)** to drill down what tags are related to the database calls, based on endpoints or tags.

If you click on a specific Query **(1)** you get a detailed query Details pane appears **(2)**, which you can use for more detailed investigations:
![details](../../images/query-details.png)
<!--

## 4. Adding Resource Attributes to Spans

Resource attributes can be added to every reported span. For example `version=0.314`. A comma-separated list of resource attributes can also be defined e.g. `key1=val1,key2=val2`.

Let's launch the PetClinic again using new resource attributes. Note, that adding resource attributes to the run command will override what was defined when we installed the collector. Let's add two new resource attributes `deployment.environment=$INSTANCE-petclinic-env,version=0.314`:

```bash
java \
-Dserver.port=8083 \
-Dotel.service.name=$INSTANCE-petclinic-service \
-Dotel.resource.attributes=deployment.environment=$INSTANCE-petclinic-env,version=0.314 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

Back in the Splunk APM UI we can drill down on a recent trace and see the new `version` attribute in a span.
-->