---
title: Rebuild PetClinic with RUM enabled
linkTitle: 1. Rebuild PetClinic
weight: 1
---

At the top of the previous code snippet, there is a reference to the file `/static/env.js`, which contains/sets the variables used by the RUM, currently these are not configured and therefore no RUM traces are currently being sent.

So, let's run the script that will update variables to enable RUM traces so they can be viewable in the **Splunk Observability Cloud** RUM UI:

{{< tabs >}}
{{% tab title="Update env.js for RUM" %}}

``` bash
. ~/workshop/petclinic/scripts/push_env.sh
```

{{% /tab %}}
{{% tab title=" Output" %}}

```text
Repository directory exists.
JavaScript file generated at: /home/splunk/spring-petclinic-microservices/spring-petclinic-api-gateway/src/main/resources/static/env.js
```

{{% /tab %}}
{{< /tabs >}}

Verify if the `env.js` has been created correctly:

{{< tabs >}}
{{% tab title="cat env.js" %}}

``` bash
cat ~/spring-petclinic-microservices/spring-petclinic-api-gateway/src/main/resources/static/scripts/env.js
```

{{% /tab %}}
{{% tab title=" Output" %}}

``` javascript
 env = {
  RUM_REALM: 'eu0',
  RUM_AUTH: '[redacted]',
  RUM_APP_NAME: 'o11y-workshop-1-store',
  RUM_ENVIRONMENT: 'o11y-workshop-1-workshop'
}
```

{{% /tab %}}
{{< /tabs >}}

``` bash
./mvnw clean install -D skipTests -P buildDocker
```

``` bash
. ~/workshop/petclinic/scripts/push_docker.sh
```

Now restart the `api-gateway` to apply the changes:

``` bash
kubectl rollout restart deployment api-gateway
```

In RUM, filter down into the environment as defined in the RUM snippet above and click through to the dashboard.

When you drill down into a RUM trace you will see a link to APM in the spans. Clicking on the trace ID will take you to the corresponding APM trace for the current RUM trace.

## More image's needed for better info plz?
