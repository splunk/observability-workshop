---
title: Sharing with ngrok
weight: 6
description: Use ngrok to give attendees a public URL for an application running on a locally hosted instance.
---

## Overview

A locally hosted instance is only reachable from your own machine or network. Attendees, Splunk Synthetic Monitoring tests, and anyone outside your network cannot open `http://localhost:81` or a private address such as `http://192.168.205.185:81`.

[ngrok](https://ngrok.com/) creates a secure tunnel from a public HTTPS URL to a port on your machine. Share that URL with attendees and they can use the workshop application as if it were hosted in the cloud.

The workshop application listens on port `81` on every local hosting option:

| Hosting option | Application address from your machine |
| --- | --- |
| [Docker](../docker) | `http://localhost:81` |
| [Multipass](../multipass) | `http://<instance-ip>:81` |
| [OrbStack](../orbstack) | `http://<instance-ip>:81` |
| [Proxmox](../proxmox) | `http://<vm-ip>:81` |

{{% notice warning %}}
Anyone with the ngrok URL can reach the application for as long as the tunnel is running. Only share it with attendees, and stop the tunnel when the workshop ends.
{{% /notice %}}

## Prerequisites

- A free [ngrok account](https://dashboard.ngrok.com/signup)
- Your ngrok authtoken from the [ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)
- A running workshop instance with the application deployed on port `81`

## Install ngrok

Install ngrok on the machine that runs the instance. On a Mac:

```bash
brew install ngrok
```

On Windows:

```bash
winget install ngrok -s msstore
```

On Linux, follow the [ngrok installation instructions](https://ngrok.com/downloads/linux).

Add your authtoken. This only needs to be done once:

```bash
ngrok config add-authtoken <your-authtoken>
```

## Start the tunnel

Confirm the application loads in your own browser first, then start the tunnel against the same address.

{{< tabs >}}
{{% tab title="Docker" %}}

```bash
ngrok http 81
```

{{% /tab %}}
{{% tab title="Multipass, OrbStack or Proxmox" %}}

Replace `<instance-ip>` with the IP address of your instance:

```bash
ngrok http http://<instance-ip>:81
```

{{% /tab %}}
{{< /tabs >}}

ngrok displays a session summary. The `Forwarding` line contains the public URL to share with attendees:

```text
Session Status                online
Account                       Workshop Host (Plan: Free)
Region                        Europe (eu)
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://a1b2-203-0-113-10.ngrok-free.app -> http://192.168.205.185:81
```

Keep the terminal open. Closing it, or pressing `Ctrl+C`, stops the tunnel.

## Use a fixed URL

By default, ngrok assigns a new random URL each time the tunnel starts. To avoid sending attendees a new link after a restart, claim the free static domain in the ngrok dashboard under **Universal Gateway → Domains**, then start the tunnel with it:

```bash
ngrok http 81 --url https://<your-domain>.ngrok-free.app
```

## Free plan browser warning

On the free plan, ngrok shows a warning page the first time a browser visits the URL. Attendees select **Visit Site** to continue to the application.

The warning page can interfere with Splunk Synthetic Monitoring browser tests and RUM sessions recorded by the tests. To skip it, add the request header `ngrok-skip-browser-warning` with any value to the test. A paid ngrok plan removes the warning page.

## Monitor attendee traffic

Open the ngrok web interface at `http://127.0.0.1:4040` to see every request coming through the tunnel. It is useful for confirming that attendees are reaching the application and for troubleshooting failed requests.

## Stop the tunnel

Press `Ctrl+C` in the terminal running ngrok. The public URL stops working immediately.

## Troubleshooting

- **`ERR_NGROK_4018` or authentication failed**: The authtoken is missing or wrong. Run `ngrok config add-authtoken <your-authtoken>` again.
- **`ERR_NGROK_8012` or a 502 Bad Gateway page**: ngrok cannot reach the application. Check that `http://localhost:81` or `http://<instance-ip>:81` loads in your browser, and that the application pods are running with `kubectl get pods`.
- **Tunnel will not start**: VPNs and proxies such as ZScaler or Cisco AnyConnect can block ngrok. Disconnect them and try again.
- **`ERR_NGROK_108` or session limit reached**: The free plan allows one agent session at a time. Stop any other running ngrok process.
- **Attendees see a new URL**: The tunnel was restarted without a static domain. Use a [fixed URL](#use-a-fixed-url).
