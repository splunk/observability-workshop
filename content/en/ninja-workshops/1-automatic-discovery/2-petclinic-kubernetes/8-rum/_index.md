---
title: Real User Monitoring
linkTitle: 8. Real User Monitoring
weight: 9
time: 10 minutes
---

To enable Real User Monitoring (RUM) instrumentation for an application, you need to add the Open Telemetry Javascript [**https://github.com/signalfx/splunk-otel-js-web**](https://github.com/signalfx/splunk-otel-js-web) snippet to the code base.

The Spring PetClinic application uses a single [**index**](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/main/spring-petclinic-api-gateway/src/main/resources/static/index.html) HTML page, that is reused across all views of the application. This is the perfect location to insert the Splunk RUM instrumentation library as it will be loaded for all pages automatically.

The `api-gateway` service is already running the instrumentation and sending RUM traces to Splunk Observability Cloud and we will review the data in the next section.

If you want you can verify the snippet, you can view the page source in your browser by right-clicking on the page and selecting **View Page Source**.

``` html
    <script src="/env.js"></script>  
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
     <!-- Section added for  RUM -->
```
