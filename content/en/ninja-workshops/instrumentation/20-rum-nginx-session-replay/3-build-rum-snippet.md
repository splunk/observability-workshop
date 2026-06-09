---
title: 3. Configure RUM for DXA
linkTitle: 3. Configure RUM
weight: 3
---

DXA starts with RUM instrumentation. The browser agent must load early, identify the RUM application consistently, and attach an anonymous user identifier so DXA can build user and session-level analyses.

This is the readable version of the core RUM snippet used by the nginx sample:

```html
<script
  src="https://cdn.observability.splunkcloud.com/o11y-gdi-rum/v3/splunk-otel-web.js"
  crossorigin="anonymous"></script>
<script
  src="https://cdn.observability.splunkcloud.com/o11y-gdi-rum/v3/splunk-otel-web-session-recorder.js"
  crossorigin="anonymous"></script>
<script>
  (function () {
    if (!window.SplunkRum) {
      return;
    }

    SplunkRum.init({
      realm: "us1",
      rumAccessToken: "replace-with-your-rum-token",
      applicationName: "dxa-rum-workshop",
      version: "1.0.0",
      deploymentEnvironment: "workshop",
      ignoreUrls: [/\/healthz$/, /\/readyz$/, /\/__splunk_rum_loaded/],
      user: {
        trackingMode: "anonymousTracking"
      },
      instrumentations: {
        visibility: true,
        interactions: {
          eventNames: SplunkRum.DEFAULT_AUTO_INSTRUMENTED_EVENT_NAMES.concat([
            "change",
            "submit"
          ])
        }
      },
      spaMetrics: true,
      privacy: {
        maskAllText: true,
        sensitivityRules: [
          { rule: "unmask", selector: "[data-rum-allow-text]" },
          { rule: "exclude", selector: "[data-rum-exclude]" }
        ]
      },
      exporter: {
        onAttributesSerializing: function (attrs) {
          var url = attrs["http.url"];
          if (typeof url === "string") {
            attrs["http.url"] = url.replace(
              /([?&](?:token|secret|password|email)=)[^&]*/gi,
              function (_, key) {
                return key + "[redacted]";
              }
            );
          }
          return attrs;
        }
      }
    });

    if (window.SplunkSessionRecorder) {
      SplunkSessionRecorder.init({
        realm: "us1",
        rumAccessToken: "replace-with-your-rum-token",
        recorder: "splunk",
        maskAllInputs: true,
        maskAllText: true,
        sensitivityRules: [
          { type: "unmask", selector: "[data-rum-allow-text]" },
          { type: "exclude", selector: "[data-rum-exclude]" }
        ]
      });
    }
  }());
</script>
```

## Why these settings matter

- `realm` and `rumAccessToken` route browser telemetry to your Splunk Observability Cloud organization.
- `applicationName`, `version`, and `deploymentEnvironment` make RUM and DXA data filterable by application, release, and environment.
- `user.trackingMode: "anonymousTracking"` creates the anonymous user ID DXA uses for behavior analysis.
- `ignoreUrls` keeps health checks, readiness probes, and the local validation beacon out of RUM views.
- `instrumentations.interactions` captures user actions that can become DXA event definitions.
- `spaMetrics` improves route-change timing for single-page application patterns.
- `privacy` keeps click text masked by default and unmasks only approved selectors.
- `exporter.onAttributesSerializing` redacts sensitive query parameters before export.
- Session Replay is optional, but useful when a DXA funnel or time series points to affected sessions.

The lab nginx template also includes a small validation beacon to `/__splunk_rum_loaded`. That request is only for workshop verification so nginx access logs can confirm that the browser reached the RUM initialization code.

{{% notice title="Best practice" style="tip" %}}
Do not start by unmasking all text or inputs. Begin with the default masked posture, identify the few UI elements that are safe and useful for analysis, and unmask those elements with explicit selectors.
{{% /notice %}}

## App-native pattern

If the frontend team owns the build, put the same `SplunkRum.init()` settings in the first JavaScript loaded by the application. For an npm-based app, install `@splunk/otel-web`, create a small instrumentation module, and import it before the rest of the app code.
