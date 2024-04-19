---
title: Real User Monitoring
linkTitle: 8. Real User Monitoring
weight: 9
hidden: false
---

## 1. Enable RUM

To enable Real User Monitoring (RUM) instrumentation for your application, you need to add the Open Telemetry Javascript [**https://github.com/signalfx/splunk-otel-js-web**](https://github.com/signalfx/splunk-otel-js-web) snippet in the web pages.

The Spring PetClinic application uses a single HTML page as the "index" page, that is reused across all pages of the application. This is the perfect location to insert the Splunk RUM Instrumentation Library as it will be loaded in all pages automatically.
For our workshop, we will use the following snippet in the **HEAD** section of the index.html page to achieve the desired integration

``` html
<script src="/static/env.js"></script>  
    <script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js" crossorigin="anonymous"></script>
    <script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web-session-recorder.js" crossorigin="anonymous"></script>
    <script>
        var realm = env.RUM_REALM;
        console.log('Realm:', realm);
        var auth = env.RUM_AUTH;
        var appName = env.RUM_APP_NAME;
        var environmentName = env.RUM_ENVIRONMENT
        if (realm && auth) {
            window.SplunkRum && window.SplunkRum.init({ 
                beaconUrl: 'https://rum-ingest.' + realm + '.signalfx.com/v1/rum',
                rumAuth: auth,
                app: appName,
                version: '1',
                environment: environmentName

            });
            SplunkSessionRecorder.init({
                beaconUrl: 'https://rum-ingest.' + realm + '.signalfx.com/v1/rumreplay',
                rumAuth: auth
            });
            const Provider = SplunkRum.provider; 
            var tracer=Provider.getTracer('appModuleLoader');
        } else {
        // Realm or auth is empty, provide default values or skip initialization
        console.log("Realm or auth is empty. Skipping SplunkRum initialization.");
    }
    </script>
```

To speed up the workshop we already added the snippet to the code in the Repo you downloaded earlier, and you already have a build that includes this snippet when rebuilding all the services in the previous exercise

If you want you can verify the snippet  we added to  the index.html by viewing the file:

{{< tabs >}}
{{% tab title="view index.html [esc :q! to quit]" %}}

``` bash
 view ~/spring-petclinic-microservices/spring-petclinic-api-gateway/src/main/resources/static/index.html
```

{{% /tab %}}
{{< /tabs >}}

Note, that we also include an `env.js` file, which contains/sets the variables used by the integration to the desired values,  right now they are empty so the integration isn't loaded. and no Rum traces are sent to Splunk.

So, let's run the script that will update variables to the right value so we will see RUM traces in the Splunk Observability Suite RUM UI:

{{< tabs >}}
{{% tab title="Update env.js for RUM" %}}

``` bash
. ~/workshop/petclinic/scripts/push_env.sh
```

{{% /tab %}}
{{% tab title=" Output" %}}

```text
Repository directory exists.
JavaScript file generated at: /home/splunk/spring-petclinic-microservices/spring-petclinic-api-gateway/src/main/resources/static/scripts/env.js
```

{{% /tab %}}
{{< /tabs >}}

now to verify if the env.js has been created correctly  lets review the file
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
  RUM_APP_NAME: 'ph-zeroconf-dev-eu0-1-1-store',
  RUM_ENVIRONMENT: 'ph-zeroconf-dev-eu0-1-1-workshop'
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
