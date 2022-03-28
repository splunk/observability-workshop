---
title: Real User Monitoring
weight: 4
---

### Splunk Real User Monitoring (RUM)

For the Real User instrumentation, we will add the Open Telemetry Javascript ([https://github.com/signalfx/splunk-otel-js-web](https://github.com/signalfx/splunk-otel-js-web)) snippet in the pages. We will use the wizard again.

Data Setup >> RUM Instrumentation >> Browser Instrumentation >> Add Connection

Then you'll need to select the RUM token and define the application and environment names. The wizard will then show a snipped of HTML code that needs to be place at the top at the pages (preferably in the < HEAD > section). In this example we are using:
- Application Name: petclinic
- Environment: conf21

``

    <script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js" crossorigin="anonymous"></script>
    <script>
    SplunkRum.init({
        beaconUrl: "https://rum-ingest.us1.signalfx.com/v1/rum",
        rumAuth: "XXXXXXXXXXXXXXXXXXXX",
        app: "petclinic",
        environment: "conf21"
        }); </script>

The Spring PetClinic application uses a single html page as the "layout" page that is reused across all pages of the application. This is the perfect location to insert the Splunk RUM Instrumentation Library as it will be loaded in all pages automatically.

Let's then edit the layout page:

    vim src/main/resources/templates/fragments/layout.html

and let's insert the snipped we generated above in the < HEAD > section of the page.

Now we need to rebuild the application and run it again:

    ./mvnw package -Dmaven.test.skip=true
    java  -javaagent:./splunk-otel-javaagent.jar -jar target/spring-petclinic-*-SNAPSHOT.jar

Then let's visit the application again to generate more traffic, now we should see RUM traces being reported.

    http://<VM_IP_ADDRESS>:8080 

(feel free to navigate and click around )

Let's visit RUM and see some of the traces and metrics.

Hamburger Menu >> RUM

You should see some of the Spring PetClinic urls showing up in the UI
