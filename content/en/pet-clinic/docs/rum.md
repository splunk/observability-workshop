---
title: Real User Monitoring
weight: 4
---

## Splunk Real User Monitoring

For the Real User Monitoring (RUM) instrumentation, we will add the Open Telemetry Javascript [https://github.com/signalfx/splunk-otel-js-web](https://github.com/signalfx/splunk-otel-js-web) snippet in the pages, we will use the wizard again **Data Setup → RUM Instrumentation → Monitor user experience → Browser Instrumentation → Add Integration**.

Then you'll need to select the workshop RUM token and define the application and environment names. The wizard will then show a snipped of HTML code that needs to be place at the top at the pages in the `<head>` section. In this example we are using:

- Application Name: `<hostname>-petclinic-service`
- Environment: `<hostname>-petclinic-env`

Copy the following code snippet and update the value for `app` and `environment` accordingly:

```html
    <script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js" crossorigin="anonymous"></script>
    <script>
    SplunkRum.init({
        beaconUrl: "https://rum-ingest.<REALM>.signalfx.com/v1/rum",
        rumAuth: "<RUM_ACCESS_TOKEN>",
        app: "<hostname>-petclinic-service",
        environment: "<hostname>-petclinic-env"
        });
    </script>
```

The Spring PetClinic application uses a single HTML page as the "layout" page, that is reused across all pages of the application. This is the perfect location to insert the Splunk RUM Instrumentation Library as it will be loaded in all pages automatically.

Let's then edit the layout page:

```bash
vi src/main/resources/templates/fragments/layout.html
```

and let's insert the snipped we generated above in the `<head>` section of the page. Now we need to rebuild the application and run it again:

## Rebuild PetClinic

run the maven command to compile/build/package PetClinic:

```bash
./mvnw package -Dmaven.test.skip=true
```

```bash
java \
-Dotel.service.name=$(hostname)-petclinic.service \
-Dsplunk.profiler.enabled=true \
-Dsplunk.metrics.enabled=true \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

Then let's visit the application again to generate more traffic `http://<VM_IP_ADDRESS>:8080`, now we should see RUM traces being reported

Let's visit RUM and see some of the traces and metrics **Hamburger Menu → RUM** and you will see some of the Spring PetClinic URLs showing up in the UI.
