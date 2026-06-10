# Before You Start

## What You Need

You do not need an AWS account, NVIDIA account, cluster-admin permissions, or Cisco AI POD hardware access.

You also do not need to clone this Git repository, install Docker, build container images, or log in to a container registry. The lab guide provides the files you edit, and Kubernetes pulls the prebuilt `shopmate-ai` image.

You do need:

- a browser
- a terminal
- `kubectl`
- `helm`
- `curl`
- `jq`
- your Splunk Observability Cloud login
- your assigned Kubernetes namespace
- your assigned student identity values

## Install Local Tools

=== "macOS"

    ```bash
    brew install kubectl helm curl jq
    ```

=== "Linux"

    ```bash
    sudo apt-get update
    sudo apt-get install -y curl jq
    # Install kubectl and helm with your approved package method.
    ```

=== "Windows"

    ```powershell
    winget install Kubernetes.kubectl
    winget install Helm.Helm
    winget install jqlang.jq
    ```

    Use Windows Terminal with PowerShell, Git Bash, or WSL Ubuntu. WSL Ubuntu or Git Bash is the closest match for the lab command blocks because the rest of this guide uses Bash-style environment variables and line continuations.

!!! tip "Windows shell choice"
    If you use native PowerShell, replace Bash variables such as `$STUDENT_NAMESPACE` with `$env:STUDENT_NAMESPACE`, and replace Bash line continuations (`\`) with PowerShell backticks or run the command on one line.

## Set Your Lab Variables

Replace the placeholder values with the values assigned to you before running these commands.

=== "macOS / Linux / WSL / Git Bash"

    ```bash
    export STUDENT_ID="<STUDENT-ID>"
    export STUDENT_NAMESPACE="<STUDENT-NAMESPACE>"
    export SPLUNK_REALM="<SPLUNK-REALM>"
    export SPLUNK_ACCESS_TOKEN_SECRET="splunk-observability-token"
    export LOGICAL_CLUSTER_NAME="clus-ltrobs-2001-<STUDENT-ID>"
    export COLLECTOR_CHART=splunk-otel-collector-chart/splunk-otel-collector
    ```

=== "Windows PowerShell"

    ```powershell
    $env:STUDENT_ID = "<STUDENT-ID>"
    $env:STUDENT_NAMESPACE = "<STUDENT-NAMESPACE>"
    $env:SPLUNK_REALM = "<SPLUNK-REALM>"
    $env:SPLUNK_ACCESS_TOKEN_SECRET = "splunk-observability-token"
    $env:LOGICAL_CLUSTER_NAME = "clus-ltrobs-2001-<STUDENT-ID>"
    $env:COLLECTOR_CHART = "splunk-otel-collector-chart/splunk-otel-collector"
    ```

!!! warning "Replace placeholders first"
    Do not run this block with literal placeholder values. Your namespace, Splunk realm, and environment filter must match your lab handout.

!!! info "Preloaded Splunk token Secret"
    The instructor preloads `splunk-observability-token` in every student namespace before class. `SPLUNK_ACCESS_TOKEN_SECRET` is only the Kubernetes Secret name, not the Splunk access token. Do not export, paste, print, or share the actual Splunk token value.

## Download Lab Files

Download these files from the lab guide before starting the modules:

| File | Used for |
| --- | --- |
| [student-kubeconfig.yaml](lab-files/student-kubeconfig.yaml) | Kubernetes access to the workshop cluster |
| [shopmate-ai.yaml](lab-files/shopmate-ai.yaml) | Kubernetes manifest for the ShopMate Sports app |
| [collector-observability-snippet.yaml](lab-files/collector-observability-snippet.yaml) | Reference sections for the Module 3 GPU/NIM collector-file change |
| [student-collector-values-gpu-nim-reference.yaml](lab-files/student-collector-values-gpu-nim-reference.yaml) | Complete reference collector values after the Module 3 GPU/NIM collector-file change |

Keep the filenames unchanged when you use the module commands. You will create `student-collector-values.yaml` yourself in Module 1 from the full copy/paste block, using the lab variables you set above.

!!! warning "Instructor check"
    If `student-kubeconfig.yaml` contains `REPLACE_WITH_...` values, the instructor has not published the real workshop access file yet. Do not continue until you have the real kubeconfig.

## Configure Kubernetes Access

Download [student-kubeconfig.yaml](lab-files/student-kubeconfig.yaml), then point `kubectl` at it.

=== "macOS / Linux / WSL / Git Bash"

    ```bash
    export KUBECONFIG="$PWD/student-kubeconfig.yaml"
    kubectl config get-contexts
    kubectl config use-context "$STUDENT_ID"
    ```

=== "Windows PowerShell"

    ```powershell
    $env:KUBECONFIG = (Resolve-Path .\student-kubeconfig.yaml)
    kubectl config get-contexts
    kubectl config use-context $env:STUDENT_ID
    ```

Expected result:

- contexts are named for student IDs, such as `student-01`
- your current context matches your assigned `STUDENT_ID`
- the context namespace matches your assigned `STUDENT_NAMESPACE`

!!! tip "Keep the file local"
    The kubeconfig is a lab access file. Keep it on your workstation, do not paste it into chat, and do not commit it to your own repositories.

## How These Variables Map To Splunk

These variables become OpenTelemetry resource attributes, span attributes, metric dimensions, or Kubernetes selectors. You will use them repeatedly in Splunk Observability Cloud.

| Variable | Telemetry attribute or use | Where you use it in Splunk |
| --- | --- | --- |
| `STUDENT_ID` | `deployment.environment` | Filter your traces, metrics, dashboards, and tokenomics views |
| `STUDENT_NAMESPACE` | `k8s.namespace.name` | Correlate your app traces with shared Kubernetes views |
| `SPLUNK_REALM` | Collector exporter endpoint selection | Determines the Splunk ingest endpoint used by the collector |
| `SPLUNK_ACCESS_TOKEN_SECRET` | Preloaded Kubernetes Secret name, `splunk-observability-token` | Lets the collector read the lab-scoped ingest token without pasting it into files |
| `LOGICAL_CLUSTER_NAME` | `k8s.cluster.name` | Separates your logical lab view from other students in shared infrastructure |
| `COLLECTOR_CHART` | Helm chart reference | Deploy the student collector |

Reference:

- Splunk explains that OpenTelemetry attributes can be attached at instrumentation time or in the Collector, and that `deployment.environment` is important for related content in Splunk Observability Cloud: [Use tags or attributes in OpenTelemetry](https://help.splunk.com/splunk-observability-cloud/manage-data/splunk-distribution-of-the-opentelemetry-collector/get-started-with-the-splunk-distribution-of-the-opentelemetry-collector/get-started-understand-and-use-the-collector/use-tags-or-attributes-in-opentelemetry).
- OpenTelemetry defines the environment variable behavior for SDK configuration: [Environment Variable Specification](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/).

## Confirm Kubernetes Access

Run:

=== "macOS / Linux / WSL / Git Bash"

    ```bash
    kubectl config current-context
    kubectl get pods -n "$STUDENT_NAMESPACE"
    kubectl auth can-i get pods -n "$STUDENT_NAMESPACE"
    kubectl auth can-i create deployments -n "$STUDENT_NAMESPACE"
    kubectl auth can-i create configmaps -n "$STUDENT_NAMESPACE"
    kubectl auth can-i create services -n "$STUDENT_NAMESPACE"
    ```

=== "Windows PowerShell"

    ```powershell
    kubectl config current-context
    kubectl get pods -n $env:STUDENT_NAMESPACE
    kubectl auth can-i get pods -n $env:STUDENT_NAMESPACE
    kubectl auth can-i create deployments -n $env:STUDENT_NAMESPACE
    kubectl auth can-i create configmaps -n $env:STUDENT_NAMESPACE
    kubectl auth can-i create services -n $env:STUDENT_NAMESPACE
    ```

Expected result:

- You can access your namespace.
- You can create normal namespaced resources.
- You do not need cluster-admin access.

Quick debug commands:

=== "macOS / Linux / WSL / Git Bash"

    ```bash
    kubectl get all -n "$STUDENT_NAMESPACE"
    kubectl logs deploy/student-collector -n "$STUDENT_NAMESPACE" --tail=50
    ```

=== "Windows PowerShell"

    ```powershell
    kubectl get all -n $env:STUDENT_NAMESPACE
    kubectl logs deploy/student-collector -n $env:STUDENT_NAMESPACE --tail=50
    ```

If a command fails, check that your kubeconfig context is correct and that `STUDENT_NAMESPACE` matches your assigned namespace.

## Prepare The Collector Chart

Add the Splunk OpenTelemetry Collector chart repo:

=== "macOS / Linux / WSL / Git Bash"

    ```bash
    helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
    helm repo update
    helm search repo "$COLLECTOR_CHART"
    ```

=== "Windows PowerShell"

    ```powershell
    helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
    helm repo update
    helm search repo $env:COLLECTOR_CHART
    ```

Expected result:

- Helm can find the collector chart named by `COLLECTOR_CHART`

If the instructor provides a packaged chart or a different chart path, use the value from the lab handout.

## Confirm Splunk Access

Open Splunk Observability Cloud in your browser and sign in.

Record the values you will use later:

```text
Splunk URL=<provided in lab handout>
Splunk realm=<provided in lab handout>
```

The ingest token is already stored in your namespace as the preloaded Kubernetes Secret named `splunk-observability-token`. You will verify that the Secret exists in Module 1, but you will not inspect or print the token value.

## Prompt Capture Safety

This lab captures synthetic retail prompt and response content so you can inspect agent flow.

Do not enter:

- real customer names
- payment data
- health data
- secrets
- confidential business data
- personal information

Use only fictional retail prompts.

!!! warning "Safety Rule"
    Treat every prompt as observable lab data.

## Knowledge Check

??? question "Why do you have a namespace instead of cluster-admin access?"
    The lab teaches app and AI observability without making every student operate the shared platform. Namespace access is enough for your collector, app configuration, traces, and GPU/NIM scrape exercise.

??? question "What field will you use most often to filter your own telemetry?"
    `deployment.environment`, along with `k8s.namespace.name` and `service.name`.
