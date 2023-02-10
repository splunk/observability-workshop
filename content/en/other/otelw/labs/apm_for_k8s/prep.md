# Log in to your Splunk Observability account to identify token/realm

For individuals and groups- allow 30-45 minutes of prep time to identify account credentials and prepare a lab environment. When running as a group we recommend doing a separate prep meeting before running the workshop together.

Check your [Splunk Observability Account](https://app.us1.signalfx.com/o11y/#/home) (your welcome email has this link) and identify your **TOKEN** and **REALM** - these are available in the profile menu in your Splunk Observability account. Note that the realm component i.e. `us1` may be different for your account based on how you signed up.

How to find realm:

`Splunk Observability Menu -> Your Name -> Account Settings`

![Realm](../../images/01-realm.png)

How to find token:  
![Token](../../images/02-token.png)

## Create Lab Environment  

Splunk Observability is for **server environments**. This workshop uses **Ubuntu Linux** as the lab server environment. You can use any Ubuntu platform - bare metal, VM, or cloud VM.

### Recommended Environment

For optimal learning we recommend that you use a fresh cloud VM running Ubuntu with minimum 12GB RAM and 20GB disk space.  

If you chose your own Ubuntu machine, you can set it up with the Workshop software with this command:

```bash
bash <(curl -s https://raw.githubusercontent.com/signalfx/otelworkshop/master/setup-tools/ubuntu.sh)
```

### Local Environment

If you cannot procure a cloud VM, you can create an Ubuntu Linux environment on a Mac or PC and install the necessary software components:

### Mac OS

Install [Homebrew](https://brew.sh):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Make sure Homebrew is fully upgraded:

```bash
brew upgrade
```

Results should be at least 1.5:

```bash
brew --version
```

We will use [Multipass](https://multipass.run) as a hypervisor for Mac:

```bash
brew cask install multipass
```

If needed, further instructions are [here](https://multipass.run/docs/installing-on-macos). Do one final brew upgrade before spinning up VM:

```bash
brew upgrade
```

### Windows

Follow Multipass Windows installation [instructions](https://multipass.run/docs/installing-on-windows)

### Launch Multipass Ubuntu VM

Create your VM called "primary":

```bash
multipass launch -n primary -d 20G -m 12G
```

This will download Ubuntu and may take a few minutes the first time.

Basic multipass commands:

- Shell into VM: `multipass shell primary`  
- Exit VM: `exit`

To manage multipass VM:

- `multipass stop primary` stops the VM
- `multipass delete primary` deletes the VM from the hypervisor  
- `multipass purge` purges created images but leaves the ubuntu template intace  

### Install OTel Workshop

A bootstrap script will install everything needed and clone this repo.  
This will take up to 10 minutes to execute- leave it running until complete.  

```bash
multipass shell primary
```

Once in your Multipass Ubuntu VM:

```bash
bash <(curl -s https://raw.githubusercontent.com/signalfx/otelworkshop/master/setup-tools/ubuntu.sh)
```

## Key OTel APM concepts

Moving parts that make APM happen in OpenTelemetry:

- **Application Spans:** OpenTelemetry instrumentation causes spans to be emitted by your applications OpenTelmetry auto-instrumentation (no code changes) for most languages is availabile but you can use any framework/library that emits spans in formats accepted by the Otel Collector i.e zipkin, OpenTracing, or [OpenTelemetry](https://opentelemtry.io). The spans are received by the OpenTelemetry Collector which both doubles as an infrastructure metrics collection agent and a telemetry processor. The Collector then forwards all telemetry (metrics/traces/logs) to Splunk Observability Cloud.  
- **Instructructure metrics:** Infrastructure metrics are collected by your OpenTelemetry Collector which is observing the application's host or container cluster. The infrastructure agent is lightweight, open source, real-time, and designed for microservices, containers, and cloud as well as on premise servers or cloud virtual machines.
- Application spans will be sent to the OpenTelemetry Collector running on a host or k8s pod to correlate APM with host/cluster metrics. The Collector then relays the spans to Splunk Observability Cloud APM where they will be assembled into traces.  
- The APM spans flow in real time and there is no sampling. Pre-made default Service Dashboards with application metrics for each app will appear once spans are received by Splunk APM. The APM view has directed troubleshooting.  
- Environment variables control the setup of APM. These names vary based on instrumentation but they always include:  
      - **Endpoint**: destination to send spans  
      - **Service name**: the name of the application as you want it to appear in a service map  
      - **Environment**: a value for segmenting betwen dev/prod etc. Can be set with instrumentation and not necessarily as part of an ENV variable.
