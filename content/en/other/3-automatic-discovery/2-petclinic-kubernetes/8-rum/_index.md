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

The above snippet of code has already been added to `index.html` in the repository you cloned earlier, but it is not yet activated, we will do that in the next section.

If you want you can verify the snippet, we added to the index.html by viewing the file:

{{< tabs >}}
{{% tab title="View index.html" %}}

``` bash
 more ~/spring-petclinic-microservices/spring-petclinic-api-gateway/src/main/resources/static/index.html
```

{{% /tab %}}
{{% tab title="Output" %}}

```text
<!DOCTYPE html>

<html ng-app="petClinicApp" lang="en">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <meta charset="utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=0, minimal-ui"/>
    <!-- The above 4 meta tags *must* come first in the head; any other head content must come *after* these tags -->

    <link rel="shortcut icon" type="image/x-icon" href="/images/favicon.png"/>

    <title>PetClinic :: a Spring Framework demonstration</title>
    <link rel="stylesheet" href="/webjars/bootstrap/css/bootstrap.min.css"/>
    <link rel="stylesheet" href="/css/petclinic.css"/>

    <script src="/webjars/jquery/jquery.min.js"></script>
    <script src="/webjars/bootstrap/js/bootstrap.min.js"></script>

    <script src="/webjars/angularjs/angular.min.js"></script>
    <script src="/webjars/angular-ui-router/angular-ui-router.min.js"></script>
    <!-- Section added for  RUM -->
    <script src="/scripts/env.js"></script>
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
    <script src="/scripts/app.js"></script>
 ```
    
{{% /tab %}}
{{< /tabs >}}
