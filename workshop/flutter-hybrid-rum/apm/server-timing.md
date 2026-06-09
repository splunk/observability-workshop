# RUM-to-APM Correlation Checklist

Use this checklist when a Flutter or hybrid mobile session does not link to backend traces.

## Backend Requirements

- Backend services are instrumented with Splunk APM or OpenTelemetry.
- `service.name` and `deployment.environment` are stable and searchable.
- Gateways, proxies, and service meshes preserve W3C Trace Context headers.
- The backend response includes server timing data when browser RUM or WebView correlation depends on it.
- CORS exposes `Server-Timing` for browser and WebView requests.

## Example Headers

```text
Server-Timing: traceparent;desc="00-<trace-id>-<span-id>-01"
Access-Control-Expose-Headers: Server-Timing
```

## Troubleshooting Questions

- Does the backend trace exist in APM for the same timestamp?
- Does the request pass through a gateway that strips `traceparent` or `tracestate`?
- Does the browser or WebView response expose `Server-Timing`?
- Are RUM and APM filtered to the same `deployment.environment`?
- Does the mobile request use a client library covered by the current RUM agent?
- Can a privacy-safe `request.id` bridge the support workflow while automatic linking is improved?
