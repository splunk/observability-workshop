# Digital Experience Analytics with Splunk RUM Workshop

This sample runs a small nginx-hosted commerce journey and injects the Splunk RUM browser agent plus Session Replay by rewriting the opening `<head>` tag.

The sample is designed for the workshop at:

```text
content/en/ninja-workshops/instrumentation/20-rum-nginx-session-replay/
```

## Quick start

```bash
cp .env.example .env
# Edit .env with your realm and RUM token.
docker compose up -d
curl -s http://localhost:8088 | grep 'splunk-dxa-rum-injected'
```

Open:

```text
http://localhost:8088
```

After opening the page, confirm the browser reached the RUM initialization code:

```bash
docker compose logs dxa-rum-workshop | grep '__splunk_rum_loaded'
```

Expected output includes:

```text
"POST /__splunk_rum_loaded?status=initialized HTTP/1.1" 204
```

The Splunk CDN script downloads do not appear in nginx logs unless you self-host or proxy those JavaScript files through nginx.

## What the sample demonstrates

- Loading the Splunk RUM browser agent from the current Splunk Observability Cloud CDN domain.
- Setting `user.trackingMode` to `anonymousTracking` for DXA user/session correlation.
- Capturing click, submit, change, page load, route-change, resource, and error activity.
- Adding custom workflow spans for product view, cart, recommendations, checkout, and demo error actions.
- Keeping RUM privacy and Session Replay masking restrictive by default.
- Marking selected demo text as safe with `data-rum-allow-text`.
- Excluding sensitive regions with `data-rum-exclude`.

## Files

- `docker-compose.yml`: starts nginx and passes RUM settings through environment variables.
- `nginx/default.conf.template`: nginx config template rendered by the official nginx Docker entrypoint, including the RUM injection and validation beacon.
- `site/index.html`: demo page with a product-to-checkout journey for RUM and DXA.

## Production notes

- Serve production applications over HTTPS.
- Prefer app-native RUM instrumentation when the frontend team owns the application build.
- For proxied upstream apps, set `proxy_set_header Accept-Encoding "";` so nginx can rewrite uncompressed HTML.
- Use RUM browser agent version 2.0.0 or later for DXA.
- Keep anonymous tracking enabled unless privacy policy requires otherwise.
- Keep Session Replay masking restrictive by default, then unmask only approved selectors.
- Update CSP to allow `cdn.observability.splunkcloud.com` and `rum-ingest.<realm>.observability.splunkcloud.com`.
- Use the `/__splunk_rum_loaded` beacon only as a rollout validation aid, or replace it with your standard frontend health telemetry.
