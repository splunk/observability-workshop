---
title: 5. Validate RUM Data
linkTitle: 5. Validate RUM
weight: 5
---

Before creating DXA projects and analyses, validate that the application is sending RUM data with the expected session and user context.

## nginx log checks

First, confirm nginx served an HTML response that contains the injected marker:

```bash
curl -s http://localhost:8088 | grep 'splunk-dxa-rum-injected'
```

Expected output:

```html
<meta name="splunk-dxa-rum-injected" content="nginx">
```

That proves nginx rewrote the HTML response. It does not prove that the browser loaded the Splunk CDN scripts.

For the local lab, the injected script sends a validation beacon to nginx after the page reaches the RUM initialization code. Open the demo page in a browser, then check the nginx container logs:

```bash
docker compose logs dxa-rum-workshop | grep '__splunk_rum_loaded'
```

Expected output includes a line similar to this:

```text
"POST /__splunk_rum_loaded?status=initialized HTTP/1.1" 204
```

Interpret the `status` value:

| Status | Meaning |
| --- | --- |
| `initialized` | The browser found `window.SplunkRum`, completed RUM initialization, and initialized Session Replay when the recorder was available. |
| `missing` | The injected initialization script ran, but `window.SplunkRum` was missing. Check CDN script loading, content blockers, and CSP. |
| `error` | The browser reached initialization, but an initialization call threw an error. Check the Chrome Console. |

{{% notice title="Important" style="info" %}}
When you load the Splunk browser agent from `cdn.observability.splunkcloud.com`, nginx does not log the CDN script downloads because the browser requests them directly from Splunk's CDN. nginx can log the HTML response and this optional validation beacon. If you self-host or proxy `splunk-otel-web.js` through nginx, nginx access logs can also show the script file requests.
{{% /notice %}}

## Browser checks

Open the application, then open DevTools.

In **Elements**, search for:

```text
splunk-dxa-rum-injected
```

In **Network**, enable **Preserve log**, reload the page, and filter for:

```text
splunk-otel-web.js
splunk-otel-web-session-recorder.js
```

Both scripts should return a successful status from:

```text
https://cdn.observability.splunkcloud.com
```

Then filter for the local validation beacon:

```text
__splunk_rum_loaded
```

You should see a request with `status=initialized`.

Then filter for your realm-specific ingest host:

```text
rum-ingest.<realm>.observability.splunkcloud.com
```

Successful requests to that host confirm the browser is attempting to send RUM telemetry to Splunk Observability Cloud.

In **Console**, confirm the RUM and Session Replay browser globals exist:

```javascript
Boolean(window.SplunkRum) && Boolean(window.SplunkSessionRecorder)
```

To inspect the active RUM session ID:

```javascript
window.SplunkRum && window.SplunkRum.getSessionId()
```

If either command returns `false`, `undefined`, or an error, check the **Console** for CSP errors such as `Refused to load the script` or content blocker errors such as `ERR_BLOCKED_BY_CLIENT`.

In **Application** > **Cookies**, look for:

```text
__splunk_rum_sid
_splunk_rum_user_anonymousId
```

`__splunk_rum_sid` links spans to a RUM session. `_splunk_rum_user_anonymousId` is the anonymous user identifier used by DXA.

## Splunk RUM checks

In Splunk Observability Cloud:

1. Open **RUM**.
2. Select the `applicationName` used in `.env`.
3. Filter by the `deploymentEnvironment`.
4. Open an example session.
5. Confirm page views, interactions, resources, JavaScript errors, and replay controls appear.

{{< tabs >}}
{{% tab title="Question" %}}
Why validate in RUM before opening DXA?
{{% /tab %}}
{{% tab title="Answer" %}}
DXA depends on RUM events. If the application name, environment, interaction spans, or anonymous user cookie are missing in RUM, DXA project setup and event definitions will either show no data or correlate events incorrectly.
{{% /tab %}}
{{< /tabs >}}

## Validate the nginx injection

Open the nginx template:

```bash
sed -n '1,240p' workshop/rum-nginx-session-replay/nginx/default.conf.template
```

The key directives are:

```nginx
sub_filter_once on;
sub_filter_types text/html;
sub_filter '<head>' '<head>...Splunk RUM snippet...';
```

`sub_filter` rewrites matching HTML responses. The sample replaces `<head>` with `<head>` plus the Splunk RUM and Session Replay scripts, which keeps the browser agent ahead of the application JavaScript.
