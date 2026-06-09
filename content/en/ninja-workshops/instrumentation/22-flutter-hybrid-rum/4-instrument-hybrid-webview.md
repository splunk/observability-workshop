---
title: 4. Instrument a Hybrid WebView Layer
weight: 4
---

Hybrid apps often combine a native or Flutter shell with web content in a WebView. In this workshop, the WebView represents a checkout, promo, help, identity, or terms step owned by a web team.

The WebView executes JavaScript, so the web layer should usually use the browser RUM agent. The Flutter shell still uses Flutter RUM for shell-owned work. The native shell should use mobile RUM only for native behavior you need to observe.

```text
Flutter cart screen
  -> opens WebView checkout
       -> browser RUM captures web route, clicks, JS errors, resources, web API calls
  -> returns to Flutter confirmation screen
```

## Add Browser RUM to the Web Bundle

Use the Splunk browser instrumentation guided setup to generate the current snippet for your realm, token, and application. Then add hybrid-specific metadata so WebView traffic is easy to distinguish from desktop browser traffic.

This instrumentation goes into the web bundle loaded by the WebView. It does not go into `main.dart`.

{{% notice title="Exercise" style="green" icon="running" %}}

Open `workshop/flutter-hybrid-rum/hybrid/rum-bootstrap.js` and adapt the values:

```js
SplunkRum.init({
  realm: window.__RUM_CONFIG__.realm,
  rumAccessToken: window.__RUM_CONFIG__.rumAccessToken,
  applicationName: window.__RUM_CONFIG__.applicationName,
  deploymentEnvironment: window.__RUM_CONFIG__.environment,
  version: window.__RUM_CONFIG__.appVersion,
  globalAttributes: {
    'app.platform': 'hybrid-webview',
    'app.shell': window.__RUM_CONFIG__.shell,
    'app.webview': 'true'
  }
});
```

Build the web bundle and open the WebView screen in the mobile app.

{{% /notice %}}

## Pass Shell Context into the WebView

Hybrid teams often know release, tenant, feature flag, and native build context in the shell. Pass only the fields the web layer needs.

{{% notice title="Exercise" style="green" icon="running" %}}

Inject a small configuration object before loading the page:

```html
<script>
  window.__RUM_CONFIG__ = {
    realm: "us1",
    rumAccessToken: "replace-with-rum-token",
    applicationName: "mobile-checkout-webview",
    environment: "workshop",
    appVersion: "1.0.0",
    shell: "flutter"
  };
</script>
```

If your WebView loads remote content, prefer server-rendered configuration or a signed bootstrap endpoint over string-building JavaScript in native code.

{{% /notice %}}

## Avoid Double Counting

If both the shell and WebView make the same API call, you can create duplicate-looking telemetry. That is a data modeling problem, not just a code problem.

| Pattern | Recommended handling |
| ------- | -------------------- |
| Flutter screen owns the API call | Let Flutter RUM capture the mobile network request. Do not add browser RUM around a nonexistent web request. |
| WebView owns the API call | Let browser RUM capture the web request. Add `app.shell=flutter` or `app.shell=capacitor` so the session is clearly embedded. |
| Shell calls API and passes data into WebView | Capture the shell network request with mobile RUM and add a custom WebView event for the user-facing web milestone. |
| WebView calls native bridge method | Add a custom event on the web side and a custom event or span on the native side if bridge latency matters. |

{{< tabs >}}
{{% tab title="Question" %}}
**Why should the WebView application name usually differ from the Flutter shell application name?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Separate names make it clear which runtime emitted the data while shared attributes still let you correlate the complete mobile experience.**
{{% /tab %}}
{{< /tabs >}}
