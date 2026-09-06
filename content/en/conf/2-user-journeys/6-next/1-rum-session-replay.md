---
title: "1. Bonus Bonus Activity: Configure RUM and Session Replay"
linkTitle: "1. Configure RUM and Session Replay"
weight: 1
time: 20 minutes
---

This activity shows how a front-end developer instruments a small application with **Splunk Real User Monitoring (RUM)** and then adds **Session Replay**. The example is intentionally framework-free so that the configuration is easy to recognize in any application.

Download the {{< rum-example-link >}} and replace the placeholders for `realm` and `rumAccessToken`. The example uses the current `v3` agent path; for production, pin the exact released version you tested. For this lab, start with the easier, certificate-free `http://localhost` path. An optional HTTPS path is also provided. The browser agent should load synchronously and as early as possible in the page `<head>`.

## Prepare the lab

1. In Splunk Observability Cloud, select **Settings** > **Access Tokens** > **New Token**. You can also reach this token from the guided **Browser Instrumentation** setup under **Digital Experience** > **Real User Monitoring**.
2. Give the token a name and select the **RUM token** authorization scope. A RUM token is a public ingestion key intended for client-side JavaScript; do not use an **Ingest token**, **API token**, admin token, or user session token here.
3. Find the organization’s realm under **Settings** > your username. For example, `app.us1.observability.splunkcloud.com` uses the `us1` realm.
4. Use the RUM token and realm in the example app. The RUM token will be visible in client-side code, so use a dedicated lab token and never substitute a broader token. Do not commit the workshop token to this repository.

![Browser Instrumentation Select Token step](../images/rum-token-step.png)

## Path 1: Run locally over HTTP—recommended for this lab

This path is intentionally insecure but requires the least setup. Use it only on your own device with dummy lab data. Do not bind the server to an external network interface.

Complete these steps on your own device:

1. Create a folder named `rum-session-replay-lab` under your home directory:

   #### macOS/Linux

   ```bash
   mkdir -p "$HOME/rum-session-replay-lab"
   ```

   #### Windows PowerShell

   ```powershell
   New-Item -ItemType Directory -Force "$env:USERPROFILE\rum-session-replay-lab" | Out-Null
   ```

2. Click the downloadable `index.html` link above and save the file as `index.html` in that folder:

   * macOS/Linux: `$HOME/rum-session-replay-lab/index.html`
   * Windows: `$env:USERPROFILE\rum-session-replay-lab\index.html`

   If the browser opens the file instead of downloading it, use **Save Link As** and keep the filename `index.html`.
3. Open `index.html` in a text editor and replace:

   * `us0` with your realm, such as `us1`.
   * `<RUM_ACCESS_TOKEN>` with your RUM token. It appears twice when Session Replay is enabled.

4. Choose **one** of the following options. The commands include the full path to the lab folder, so they can be run from any directory. Do not open the file directly with a `file://` URL; using a local web server gives the browser a consistent origin for session tracking.

### Option 1: Python

Python includes a small web server and is often already installed.

#### macOS/Linux

```bash
python3 -m http.server 8080 --directory "$HOME/rum-session-replay-lab"
```

#### Windows PowerShell

```powershell
py -m http.server 8080 --directory "$env:USERPROFILE\rum-session-replay-lab"
```

### Option 2: Node.js

If Node.js is installed, the same command works in macOS, Linux, and Windows PowerShell:

```bash
npx --yes http-server "$HOME/rum-session-replay-lab" -p 8080
```

### Option 3: Docker

If Docker Desktop or Docker Engine is installed, Nginx can serve the folder without installing Python or Node.js.

#### macOS/Linux

```bash
docker run --rm --name rum-session-replay-lab \
  -p 8080:80 \
  -v "$HOME/rum-session-replay-lab:/usr/share/nginx/html:ro" \
  nginx:alpine
```

#### Windows PowerShell

```powershell
docker run --rm --name rum-session-replay-lab `
  -p 8080:80 `
  -v "${env:USERPROFILE}\rum-session-replay-lab:/usr/share/nginx/html:ro" `
  nginx:alpine
```

On the first run, Docker downloads the Nginx image. `-p 8080:80` exposes Nginx on local port `8080`, the `-v` option mounts the lab folder, and `:ro` prevents the container from changing your file. Docker Desktop might prompt for permission to share the folder.

Open `http://localhost:8080/index.html`. Keep the terminal open while testing and press `Ctrl+C` to stop the server. If port `8080` is already in use, use `8081` in the command and URL instead.

This certificate-free setup is intended only for the local workshop. Use dummy names, email addresses, and card digits. Do not expose the server to the local network or use this setup for production data.

If data does not appear, open the browser developer tools and check:

* **Console** for messages beginning with `SplunkRum:`.
* **Network** for requests to `rum-ingest.<realm>.observability.splunkcloud.com`.
* That the realm and active RUM token belong to the same organization.
* Whether an ad blocker or privacy extension blocked the CDN or ingest request.

## Path 2: Run locally over HTTPS—optional

Use this path if your browser or organization policy requires HTTPS, or if you want a more production-like test. It requires Node.js and a locally trusted development certificate from `mkcert`. The commands below use the same `rum-session-replay-lab` folder created above.

### macOS

```bash
cd "$HOME/rum-session-replay-lab"
brew install mkcert nss
mkcert -install
mkcert localhost 127.0.0.1 ::1
npx --yes http-server . -S -C localhost+2.pem -K localhost+2-key.pem -p 8443
```

### Linux (Debian/Ubuntu)

```bash
cd "$HOME/rum-session-replay-lab"
sudo apt-get update
sudo apt-get install -y mkcert libnss3-tools
mkcert -install
mkcert localhost 127.0.0.1 ::1
npx --yes http-server . -S -C localhost+2.pem -K localhost+2-key.pem -p 8443
```

### Windows PowerShell

```powershell
Set-Location "$env:USERPROFILE\rum-session-replay-lab"
winget install FiloSottile.mkcert
mkcert -install
mkcert localhost 127.0.0.1 ::1
npx --yes http-server . -S `
  -C .\localhost+2.pem -K .\localhost+2-key.pem -p 8443
```

Open `https://localhost:8443/index.html`. The certificate command normally creates `localhost+2.pem` and `localhost+2-key.pem`; if it reports different filenames, use those names in the server command. If Chrome still shows a certificate warning after `mkcert -install`, restart Chrome.

The `*-key.pem` file is a private key. Do not commit or share either certificate file; remove both files from the lab folder when the workshop is complete.

## Basic RUM

Basic RUM needs the browser agent and a call to `SplunkRum.init`. This captures front-end telemetry such as page loads, resource and network requests, interactions, errors, and web vitals.

```html
<script src="https://cdn.observability.splunkcloud.com/o11y-gdi-rum/v3/splunk-otel-web.js" crossorigin="anonymous"></script>
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

![Splunk RUM application overview](../images/rum-overview.png)

## Add Session Replay

Session Replay is an additional recorder. Load both scripts first, then initialize RUM and the recorder in that order:

```html
<script src="https://cdn.observability.splunkcloud.com/o11y-gdi-rum/v3/splunk-otel-web.js" crossorigin="anonymous"></script>
<script src="https://cdn.observability.splunkcloud.com/o11y-gdi-rum/v3/splunk-otel-web-session-recorder.js" crossorigin="anonymous"></script>
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

After generating a session, open **Digital Experience** > **Real User Monitoring** > **Session Search**. Filter for **Session Replay = Present**, then select the session to open the replay player.

![RUM Session Search with replay availability](../images/rum-session-search.png)

## Protect PII and other sensitive data in Session Replay

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

The safest design is to avoid placing PII in URLs, DOM identifiers, custom attributes, or user metadata in the first place. RUM does not automatically capture a named user identity, but current agents can create a persistent anonymous user ID for session and journey correlation. If that is not appropriate, explicitly set `user: { trackingMode: "noTracking" }`; only add approved user identifiers when there is a clear operational need.

{{% notice title="Exercise" style="green" icon="running" %}}

1. Open the example `index.html`, replace the placeholders, and confirm that **Basic RUM** is already enabled. Use your browser's developer tools to confirm the agent loads before the application script.
2. Serve the example on `http://localhost`, open it in a private browser window, click **Add to cart**, enter a sample email and dummy card digits, and select **Place order**.
3. Enable the Session Replay script and initialization, repeat the journey, and open the session in Splunk RUM.
4. Confirm that product names are visible, the email is masked, and the payment form is excluded from the replay.
5. Add a sample `?token=do-not-ship-this` query parameter and verify the RUM attribute sanitizer would redact it before export.

{{% /notice %}}

For current agent installation and configuration details, see [Install the Splunk RUM browser agent](https://help.splunk.com/en/splunk-observability-cloud/manage-data/instrument-front-end-applications/instrument-mobile-and-web-applications-for-splunk-real-user-monitoring-rum/instrument-browser-applications-for-splunk-rum/install-the-splunk-rum-browser-agent), [browser session configuration examples](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/real-user-monitoring/replay-user-sessions/record-browser-sessions/browser-session-configuration-examples), and [controls for sensitive data in Splunk RUM](https://help.splunk.com/en/splunk-observability-cloud/manage-data/manage-sensitive-data/use-controls-for-sensitive-data-in-splunk-rum).
