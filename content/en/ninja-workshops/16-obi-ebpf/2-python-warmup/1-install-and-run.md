---
title: 1. Install and Run the App
weight: 1
---

## Set Up the Python Environment

Navigate to the Phase 0 directory and create a virtual environment:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
cd ~/workshop/obi/01-obi-python
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
Collecting flask>=3.0,<4.0
  Downloading ...
Successfully installed flask-3.x.x ...
```

{{% /tab %}}
{{< /tabs >}}

## Set Your Splunk Credentials

Export your credentials as environment variables. Replace each placeholder with your actual values:

{{% notice title="Exercise" style="green" icon="running" %}}

``` bash
export SPLUNK_INGEST_TOKEN="<YOUR_TOKEN>"
export SPLUNK_REALM="<YOUR_REALM>"
export WORKSHOP_HOST_NAME="<YOUR_NAME>"
```

Replace:

* `<YOUR_TOKEN>` with your Splunk ingest token
* `<YOUR_REALM>` with your realm (e.g. `us0`, `us1`, `eu0`)
* `<YOUR_NAME>` with a unique identifier (e.g. `jsmith-laptop`)

{{% /notice %}}

## Run the App

Start the Flask app in the background:

``` bash
nohup python3 app.py &
```

On startup the app sends a single `app.heartbeat` metric directly to the Splunk Ingest API. You should see:

``` text
Heartbeat sent to Splunk (200)
 * Running on http://0.0.0.0:5150
```

Hit the endpoint to confirm it's working:

``` bash
curl http://localhost:5150/hello
```

You should get back:

``` json
{
  "host": "<YOUR_NAME>",
  "message": "Hello from the OBI Workshop warm-up!"
}
```

## Verify in Splunk

1. Open [Metric Finder](https://app.signalfx.com/#/metrics) and search for `app.heartbeat`.
2. You should see the metric with `host.name` matching the value you set.

{{% notice title="Note" style="info" %}}
At this point you have a running app and proof that Splunk can receive your data. But there are **zero traces** -- APM is empty. The app has no instrumentation code whatsoever.
{{% /notice %}}
