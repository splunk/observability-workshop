---
title: Sharing with ngrok
weight: 6
description: Use ngrok to give attendees a public URL for an application running on a locally hosted instance.
---

## Overview

A locally hosted instance is only reachable from your own machine or network. Attendees, Splunk Synthetic Monitoring tests, and anyone outside your network cannot open `http://localhost:81` or a private address such as `http://192.168.205.185:81`.

[ngrok](https://ngrok.com/) puts a service running on your machine online at a public HTTPS URL. Share that URL with attendees and they can use the workshop application as if it were hosted in the cloud.

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

On Windows and Linux, get the agent from the [ngrok download page](https://ngrok.com/download).

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
ngrok http <instance-ip>:81
```

{{% /tab %}}
{{< /tabs >}}

ngrok prints the public URL to share with attendees. Keep the terminal open. Closing it, or pressing `Ctrl+C`, stops the tunnel.

Every ngrok account, including the free plan, has a dev domain such as `your-assigned-name.ngrok-free.app`. `ngrok http` uses it automatically and it does not change when you restart the agent, so attendees can keep using the same URL if the tunnel is restarted.

## Free plan limits

The free plan is enough for small workshops, but check its [limits](https://ngrok.com/docs/pricing-limits/free-plan-limits/) before a large session. These are the limits most likely to matter:

| Limit | Free plan |
| --- | --- |
| HTTP requests | 20,000 per month |
| Data transfer out | 1 GB per month |
| HTTP request rate | 4,000 per minute |
| Concurrent agents | 3 |

Every page load in the application makes many HTTP requests, so a large group of attendees can use up the monthly quotas quickly. Check current usage on the **Usage** page in the ngrok dashboard, and consider a paid plan for large workshops.

## Free plan browser warning

On the free plan, ngrok shows an interstitial warning page in front of all HTML browser traffic. Attendees select **Visit** to continue to the application. A cookie then hides the warning for that domain for 7 days.

The warning page can block Splunk Synthetic Monitoring browser tests. To skip it, add the request header `ngrok-skip-browser-warning` with any value to the test, or set the `User-Agent` header to a non-standard value such as `MyApp/0.0.1`. Upgrading to any paid ngrok plan removes the warning page.

## Monitor attendee traffic

Open the ngrok web inspection interface at `http://localhost:4040` on the machine running ngrok. It shows every HTTP request coming through the tunnel, including the time, duration, source IP, status, and headers. This is useful for confirming that attendees are reaching the application and for troubleshooting failed requests.

## Stop the tunnel

Press `Ctrl+C` in the terminal running ngrok. The public URL stops working.

## Troubleshooting

- **`ERR_NGROK_4018`**: The ngrok session is not authenticated. Run `ngrok config add-authtoken <your-authtoken>` with the authtoken from the dashboard.
- **`ERR_NGROK_8012`**: Traffic reached the ngrok agent, but the agent could not connect to the application. Check that `http://localhost:81` or `http://<instance-ip>:81` loads in your browser, that the port in the ngrok command is `81`, and that the application pods are running with `kubectl get pods`.
- **`ERR_NGROK_108`**: Your account has reached its limit of simultaneous agent sessions, which is 3 on the free plan. Stop other running ngrok processes.
- **`ERR_NGROK_6024`**: This is the free plan browser warning page, not a fault. Select **Visit** to continue.
