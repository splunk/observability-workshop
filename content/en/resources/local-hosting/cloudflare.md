---
title: Sharing with Cloudflare Quick Tunnels
weight: 7
description: Use a Cloudflare Quick Tunnel to give attendees a public URL for an application running on a locally hosted instance, without an account.
---

## Overview

A locally hosted instance is only reachable from your own machine or network. Attendees, Splunk Synthetic Monitoring tests, and anyone outside your network cannot open `http://localhost:81` or a private address such as `http://192.168.205.185:81`.

[Cloudflare Quick Tunnels](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) create a temporary public `trycloudflare.com` URL that forwards to a port on your machine. No Cloudflare account or domain is required.

The workshop application listens on port `81` on every local hosting option:

| Hosting option | Application address from your machine |
| --- | --- |
| [Docker](../docker) | `http://localhost:81` |
| [Multipass](../multipass) | `http://<instance-ip>:81` |
| [OrbStack](../orbstack) | `http://<instance-ip>:81` |
| [Proxmox](../proxmox) | `http://<vm-ip>:81` |

{{% notice warning %}}
Anyone with the Quick Tunnel URL can reach the application for as long as the tunnel is running. Only share it with attendees, and stop the tunnel when the workshop ends.
{{% /notice %}}

## Install cloudflared

Install `cloudflared` on the machine that runs the instance. On a Mac:

```bash
brew install cloudflared
```

On Windows and Linux, download the latest release from the [cloudflared downloads page](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/downloads/).

## Start the tunnel

Confirm the application loads in your own browser first, then start the tunnel against the same address.

{{< tabs >}}
{{% tab title="Docker" %}}

```bash
cloudflared tunnel --url http://localhost:81
```

{{% /tab %}}
{{% tab title="Multipass, OrbStack or Proxmox" %}}

Replace `<instance-ip>` with the IP address of your instance:

```bash
cloudflared tunnel --url http://<instance-ip>:81
```

{{% /tab %}}
{{< /tabs >}}

`cloudflared` prints a `trycloudflare.com` URL. Open it to confirm the application loads, then share it with attendees.

Keep the terminal open. Closing it, or pressing `Ctrl+C`, stops the tunnel and the URL stops working.

{{% notice info %}}
The hostname changes every time a Quick Tunnel is created. If you restart the tunnel, send attendees the new URL. For a stable hostname, use [ngrok](../ngrok), whose dev domain stays the same across restarts, or create a [Cloudflare Tunnel](https://developers.cloudflare.com/tunnel/).
{{% /notice %}}

## Restrict access by email

Add `--allowed-mail` to require visitors to verify their email address with a one-time PIN before they reach the application. Visitors do not need a Cloudflare account.

Allow every address from an email domain. Quote wildcard values so the shell does not expand them:

```bash
cloudflared tunnel --url http://localhost:81 --allowed-mail '*@example.com'
```

Allow specific addresses by repeating the flag or using a comma-separated list:

```bash
cloudflared tunnel --url http://localhost:81 \
  --allowed-mail 'alice@example.com,bob@example.com'
```

To change who has access, stop `cloudflared` and start a new Quick Tunnel, which has a new URL. Access ends for everyone when the process stops.

{{% notice warning %}}
Email authentication needs an interactive browser session. Splunk Synthetic Monitoring tests and other automated clients cannot pass it, so leave `--allowed-mail` off if the workshop uses synthetic tests against the application.
{{% /notice %}}

## Limitations

Quick Tunnels are intended for testing and development:

- There is no uptime guarantee.
- Each tunnel supports up to 200 in-flight requests. Additional requests return a `429` response. This is enough for a typical workshop, but avoid pointing heavy load generators at the tunnel URL.
- Server-Sent Events (SSE) are not supported.
- The hostname changes each time the tunnel is created.

## Stop the tunnel

Press `Ctrl+C` in the terminal running `cloudflared`. The public URL stops working immediately for everyone.

## Troubleshooting

- **Tunnel URL shows an error instead of the application**: Check that `http://localhost:81` or `http://<instance-ip>:81` loads in your own browser, that the address passed to `--url` matches it, and that the application pods are running with `kubectl get pods`. Read the `cloudflared` terminal output for connection errors.
- **Attendees receive `429` responses**: The tunnel has reached 200 in-flight requests. Reduce load, or use [ngrok](../ngrok) instead.
- **Synthetic tests fail at an email prompt**: The tunnel was started with `--allowed-mail`, which does not support non-interactive clients. Restart it without the flag.
