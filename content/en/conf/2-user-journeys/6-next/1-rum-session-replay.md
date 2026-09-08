---
title: "1. Bonus Bonus Activity: Configure RUM and Session Replay"
linkTitle: "1. Configure RUM and Session Replay"
weight: 1
time: 10 minutes
---

This activity shows how a front-end developer instruments a small application with **Splunk Real User Monitoring (RUM)** and then adds **Session Replay**. The example is intentionally framework-free so that the configuration is easy to recognize in any application.

Download or copy the {{< rum-example-link >}} and replace the placeholders for `realm`, `rumAccessToken`, and the RUM agent `VERSION`. Serve the file over **HTTPS** in a test environment; the browser agent should load synchronously and as early as possible in the page `<head>`.

## Prepare the lab

1. In Splunk Observability Cloud, open **Digital Experience** > **Real User Monitoring** > **RUM Configuration** > **Create RUM Integration** > **Browser Instrumentation**.
2. On **Select Token**, choose an organization access token with **Ingest Token** permissions. The RUM token is a public ingestion key that is expected to appear in client-side JavaScript; never use an admin or user API token here.
3. Record your organization’s realm from the Observability Cloud URL or ask the instructor. For example, `app.us1.signalfx.com` uses the `us1` realm.
4. Use the selected token and realm in the example app. Keep the token scoped to this lab and do not commit it to the repository.

<!-- TODO screenshot: Browser Instrumentation guided setup on the Select Token step with no token value exposed. -->
![Browser Instrumentation Select Token step](../images/rum-token-step.png)

## Serve the example over HTTPS

The browser agent should be tested over HTTPS. One simple local approach is to create a trusted development certificate with `mkcert`, then use the Node-based static server:

```bash
mkcert -install
mkcert localhost 127.0.0.1 ::1
npx http-server static -S -C localhost+2.pem -K localhost+2-key.pem -p 8443
```

Open `https://localhost:8443/examples/rum-session-replay/index.html`. If Chrome warns about the certificate, confirm that `mkcert -install` completed successfully and restart the browser. For a workshop, an instructor-provided HTTPS host is also fine.

### Quick HTTP-only option (insecure)

For a fast localhost smoke test, you can skip the certificate and serve the files over HTTP:

```bash
npx http-server static -p 8080
```

Open `http://localhost:8080/examples/rum-session-replay/index.html`. This is acceptable only for a disposable local lab. It does not protect the page or any values typed into it, and browser security policies or Session Replay requirements may prevent it from working. Use the HTTPS option above if RUM or replay data does not appear, and never use this approach for real users or production data.

## Basic RUM

Basic RUM needs the browser agent and a call to `SplunkRum.init`. This captures front-end telemetry such as page loads, resource and network requests, interactions, errors, and web vitals.

```html
<script src="https://cdn.observability.splunkcloud.com/o11y-gdi-rum/VERSION/splunk-otel-web.js" crossorigin="anonymous"></script>
<script>
  SplunkRum.init({
    realm: "us0",
    rumAccessToken: "<RUM_ACCESS_TOKEN>",
    applicationName: "northstar-coffee",
    version: "1.0.0",
    deploymentEnvironment: "workshop"
  });
</script>
```

The `applicationName`, `version`, and `deploymentEnvironment` values are how you separate this application and its releases in RUM. Do not commit a real access token to source control; inject it during deployment or replace the placeholder only in a local test copy.

<!-- TODO screenshot: RUM Overview showing the application summary dashboard, filters, errors, and web vitals. -->
![Splunk RUM application overview](../images/rum-overview.png)

## Add Session Replay

Session Replay is an additional recorder. Load both scripts first, then initialize RUM and the recorder in that order:

```html
<script src="https://cdn.observability.splunkcloud.com/o11y-gdi-rum/VERSION/splunk-otel-web.js" crossorigin="anonymous"></script>
<script src="https://cdn.observability.splunkcloud.com/o11y-gdi-rum/VERSION/splunk-otel-web-session-recorder.js" crossorigin="anonymous"></script>
<script>
  SplunkRum.init({
    realm: "us0",
    rumAccessToken: "<RUM_ACCESS_TOKEN>",
    applicationName: "northstar-coffee",
    version: "1.0.0",
    deploymentEnvironment: "workshop"
  });

  SplunkSessionRecorder.init({
    realm: "us0",
    rumAccessToken: "<RUM_ACCESS_TOKEN>",
    recorder: "splunk"
  });
</script>
```

RUM answers **what** happened and how long it took. Replay adds the visual sequence of DOM changes and interactions that helps explain **what the user experienced**. Session Replay requires an Enterprise subscription and RUM browser agent version 2.1.0 or later. Pin and test a released agent version before using it in production.

After generating a session, open **Digital Experience** > **Real User Monitoring** > **Session Search**. A check mark in the **Session Replay** column indicates that replay data is available for that session.

<!-- TODO screenshot: RUM Session Search showing sessions, the Session Replay column, issues, and browser context. -->
![RUM Session Search with replay availability](../images/rum-session-search.png)

## Protect PII in Session Replay

Treat replay as user data. The recorder defaults to a conservative posture: input values and text are masked. Keep those defaults unless there is a documented reason to reveal a field.

The example app marks product names as safe to show, masks the customer email, and excludes the payment form entirely:

```html
<script>
  SplunkSessionRecorder.init({
    realm: "us0",
    rumAccessToken: "<RUM_ACCESS_TOKEN>",
    recorder: "splunk",
    maskAllInputs: true,
    maskAllText: true,
    sensitivityRules: [
      { rule: "unmask", selector: ".product-name" },
      { rule: "mask", selector: ".customer-email" },
      { rule: "exclude", selector: "#payment-form" }
    ]
  });
</script>
```

Rules are evaluated in order, so put general rules first and specific overrides later. The available actions are:

* `mask` replaces content with black bars.
* `unmask` reveals a previously masked element.
* `exclude` removes the element from the recording, including its interactions; `exclude` cannot be overridden.

Use stable CSS classes or IDs for data classifications rather than brittle selectors. For example, a product name may be unmasked, while an email address, account area, password field, or payment form should remain masked or excluded. Validate the rendered replay—not just the configuration—before enabling it for real users.

<!-- TODO screenshot: RUM session detail showing Session Events, the Session Replay player, and the session timeline. -->
![RUM session detail with Session Replay](../images/rum-session-replay.png)

### RUM span data is a separate concern

Replay masking does not sanitize attributes already collected by RUM. If the application puts a secret in a URL or custom attribute, redact it before export with `exporter.onAttributesSerializing`:

```js
SplunkRum.init({
  // ... realm, token, and application settings ...
  exporter: {
    onAttributesSerializing: (attributes) => ({
      ...attributes,
      "http.url": typeof attributes["http.url"] === "string"
        ? attributes["http.url"].replace(/([?&]token=)[^&]+(&|$)/g, "$1<redacted>$2")
        : attributes["http.url"]
    })
  }
});
```

The safest design is to avoid placing PII in URLs, DOM identifiers, custom attributes, or user metadata in the first place. RUM does not automatically identify users; only add user identifiers when there is a clear operational need and the value has been approved for collection.

{{% notice title="Exercise" style="green" icon="running" %}}

1. Open the example `index.html` and enable **Basic RUM**. Use your browser's developer tools to confirm the agent loads before the application script.
2. Serve the example over HTTPS, open it in a private browser window, and interact with the product and checkout form.
3. Enable the Session Replay script and initialization, repeat the journey, and open the session in Splunk RUM.
4. Confirm that product names are visible, the email is masked, and the payment form is excluded from the replay.
5. Add a sample `?token=do-not-ship-this` query parameter and verify the RUM attribute sanitizer would redact it before export.

{{% /notice %}}

For the complete list of recorder options, see the [Splunk RUM browser session configuration examples](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/real-user-monitoring/replay-user-sessions/record-browser-sessions/browser-session-configuration-examples) and [controls for sensitive data in Splunk RUM](https://help.splunk.com/en/splunk-observability-cloud/manage-data/manage-sensitive-data/use-controls-for-sensitive-data-in-splunk-rum).
