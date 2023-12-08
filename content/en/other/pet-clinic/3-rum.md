---
title: 3. Real User Monitoring
weight: 3
---

## 1. Enable RUM

For the Real User Monitoring (RUM) instrumentation, we will add the Open Telemetry Javascript [https://github.com/signalfx/splunk-otel-js-web](https://github.com/signalfx/splunk-otel-js-web) snippet in the pages, we will use the wizard again **Data Management → Add Integration → RUM Instrumentation → Browser Instrumentation**.

Select the preconfigured **RUM ACCESS TOKEN** from the dropdown, and click **Next**. Enter **App name** and **Environment** using the following syntax:

- `[instance]-petclinic-service` - replacing `[instance]` with your actual hostname.
- `[instance]-petclinic-env` - replacing `[instance]` with your actual hostname.

Then you'll need to select the workshop RUM token and define the application and environment names. The wizard will then show a snippet of HTML code that needs to be placed at the top of the pages in the `<head>` section. In this example, we are using:

- Application Name: `<instance>-petclinic-service`
- Environment: `<instance>-petclinic-env`

Copy the generated code snippet in the wizard or copy and edit the snippet below accordingly. You need to replace `<REALM>`, `<RUM_ACCESS_TOKEN>` and `<instance>` with the actual values.

``` html
<script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js" crossorigin="anonymous"></script>
<script>
SplunkRum.init({
    beaconUrl: "https://rum-ingest.<REALM>.signalfx.com/v1/rum",
    rumAuth: "<RUM_ACCESS_TOKEN>",
    app: "<instance>-petclinic-service",
    environment: "<instance>-petclinic-env"
    });
</script>
```

The Spring PetClinic application uses a single HTML page as the "layout" page, that is reused across all pages of the application. This is the perfect location to insert the Splunk RUM Instrumentation Library as it will be loaded in all pages automatically.

Let's then edit the layout page:

```bash
vi src/main/resources/templates/fragments/layout.html
```

Next, insert the snippet we generated above in the `<head>` section of the page. Now we need to rebuild the application and run it again:

## 2. Rebuild PetClinic

Run the `maven` command to compile/build/package PetClinic:

```bash
./mvnw package -Dmaven.test.skip=true
```

```bash
java \
-Dserver.port=8083 \
-Dotel.service.name=$INSTANCE-petclinic-service \
-Dotel.resource.attributes=version=0.314 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

Then let's visit the application using a browser to generate real-user traffic `http://<VM_IP_ADDRESS>:8083`, now we should see RUM traces being reported.

Let's visit RUM and see some of the traces and metrics **Hamburger Menu → RUM** and you will see some of the Spring PetClinic URLs showing up in the UI.

When you drill down into a RUM trace you will see a link to APM in the spans. Clicking on the trace ID will take you to the corresponding APM trace for the current RUM trace.
