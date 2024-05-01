---
title: Real User Monitoring
linkTitle: 8. Real User Monitoring
weight: 9
time: 10 minutes
---

To enable Real User Monitoring (RUM) instrumentation for your application, you need to add the Open Telemetry Javascript [**https://github.com/signalfx/splunk-otel-js-web**](https://github.com/signalfx/splunk-otel-js-web) snippet to your code.

The Spring PetClinic application uses a single HTML page as the "index" page, that is reused across all pages of the application. This is the perfect location to insert the Splunk RUM Instrumentation Library as it will be loaded for all pages automatically.

The following snippet is inserted into the **<head>** section of the `index.html` page:

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
        SplunkRum.init({
            realm: realm,
            rumAccessToken: auth,
            applicationName: appName,
            deploymentEnvironment: environmentName,
            version: '1.0.0',
        });

        SplunkSessionRecorder.init({
            app: appName,
            realm: realm,
            rumAccessToken: auth
        });
        const Provider = SplunkRum.provider; 
        var tracer=Provider.getTracer('appModuleLoader');
    } else {
    // Realm or auth is empty, provide default values or skip initialization
    console.log("Realm or auth is empty. Skipping Splunk Rum initialization.");
    }
</script>
```

The above snippet of code has already been added to `index.html` in the repository you cloned earlier, and you already have a build that includes this snippet when rebuilding all the services in the previous exercise

If you want you can verify the snippet  we added to the index.html by viewing the file:

{{< tabs >}}
{{% tab title="View index.html" %}}

``` bash
 more ~/spring-petclinic-microservices/spring-petclinic-api-gateway/src/main/resources/static/index.html
```

{{% /tab %}}
{{< /tabs >}}
