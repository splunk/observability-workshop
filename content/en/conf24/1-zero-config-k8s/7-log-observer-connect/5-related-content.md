---
title: Related Content
linkTitle: 5. Related Content
weight: 5
---

Also, at the bottom next to APM, there should be a number, this is the number of related AP Content items for this logline.  click on the APM pane **(1)** as shown below:

![RC](../../images/log-apm-rc.png)

- The *Map for customers-service*  **(2)** brings us to the APM dependency map with the workflow focused on Customer Services, allowing you to quickly understand how this logline is related to the overall flow of service interaction.
- The *Trace for 34c98cbf7b300ef3dedab49da71a6ce3* **(3)** will bring us to the waterfall in APM for this specific trace that this log line was generated in.

As a last exercise, click on  the Trace for Link, this will bring you to the waterfall for this specific trace:

![waterfall logs](../../images/waterfall-with-logs.png)

Note that you now have Logs Related Content Pane **(1)** appear, clicking on this will bring you back to log observer with all the loglines that are part of this Trace.
This will help you to quickly find relevant log lines for an interaction or a problem.

## Summary

This is the end of the workshop and we have certainly covered a lot of ground. At this point, you should have metrics, traces, logs, database query performance and code profiling being reported into Splunk Observability Cloud.

**Congratulations!**

<!--
docker system prune -a --volumes

  81  . ~/workshop/petclinic/scripts/add_otel.sh
   82  . ~/workshop/petclinic/scripts/update_logback.sh
   83  ./mvnw clean install -DskipTests -P buildDocker
   84  . ~/workshop/petclinic/scripts/push_docker.sh
   85  . ~/workshop/petclinic/scripts/set_local.sh
   86  kubectl apply -f ~/workshop/petclinic/petclinic-local.yaml
   87  k9s
   88  kubectl delete -f ~/workshop/petclinic/petclinic-local.yaml
   89  kubectl apply -f ~/workshop/petclinic/petclinic-local.yaml
   90  k9s
   91  kubectl delete -f ~/workshop/petclinic/petclinic-local.yaml
   92  kubectl apply -f ~/workshop/petclinic/petclinic-local.yaml
   93  k9s
   94  kubectl get deployments -l app.kubernetes.io/part-of=spring-petclinic -o name | xargs -I % kubectl patch % -p "{\"spec\": {\"template\":{\"metadata\":{\"annotations\":{\"instrumentation.opentelemetry.io/inject-java\":\"true\"}}}}}"
-->