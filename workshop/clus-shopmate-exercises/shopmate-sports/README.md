# ShopMate Sports

Standalone fictional retail app for the AI Pods workshop.

Students use the storefront and chat assistant like shoppers. The app is
instrumented with Splunk-supported zero-code OpenAI and OpenAI Agents
instrumentation when it is started with `opentelemetry-instrument`. It also
adds a small set of custom workflow spans so the multi-agent trace is easier to
read.

## Run Locally

```bash
python3 shopmate-sports/server.py
```

Open:

```text
http://127.0.0.1:8080/
```

## Build Container Image

Students do not build this image during the lab. The instructor or build team should publish the image before class and update the Kubernetes manifests if the image URI changes.

From a fresh machine:

```bash
git clone <repo-url> ai-pods
cd ai-pods
```

Build the image:

```bash
docker build -t shopmate-ai:lab-stable shopmate-sports
```

For ECR, use the repository created by Terraform:

```bash
export AWS_REGION="$(terraform -chdir=infra/terraform output -raw aws_region)"
export SHOPMATE_REPO="$(terraform -chdir=infra/terraform output -json ecr_repository_urls | jq -r '.["shopmate-ai"]')"
export SHOPMATE_IMAGE="${SHOPMATE_REPO}:lab-stable"
export ECR_REGISTRY="$(printf "%s\n" "$SHOPMATE_REPO" | cut -d/ -f1)"

aws ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS --password-stdin "$ECR_REGISTRY"

docker build --platform linux/amd64 -t "$SHOPMATE_IMAGE" shopmate-sports
docker push "$SHOPMATE_IMAGE"
```

If you are not using Terraform-managed ECR, set `SHOPMATE_IMAGE` to your registry URI before building. Then update the `image:` field in:

- `infra/k8s/shopmate-ai.yaml`
- `workshop/lab-files/shopmate-ai.yaml`

## NIM Mode

The chat assistant requires a NIM OpenAI-compatible endpoint. If NIM is not
configured or the Agents SDK call fails, `/api/chat` returns an error instead of
substituting a local deterministic response.

To call a NIM OpenAI-compatible endpoint through the OpenAI Agents SDK:

```bash
python3 -m pip install -r shopmate-sports/requirements.txt
export NIM_BASE_URL="https://your-nim-endpoint/v1"
export NIM_API_KEY="..."
export NIM_MODEL="your-model-name"
python3 shopmate-sports/server.py
```

Use `NIM_BASE_URL=https://.../v1` because the OpenAI Agents SDK expects an
OpenAI-compatible base URL.

Optional:

```bash
export SHOPMATE_PORT=8080
export SHOPMATE_HOST=0.0.0.0
export SHOPMATE_AGENT_MAX_TURNS=6
```

## Splunk Zero-Code OpenAI Instrumentation

Run the app with Splunk zero-code instrumentation so OpenAI Agents SDK and
OpenAI-compatible NIM calls emit GenAI traces and metrics:

```bash
python3 -m pip install -r shopmate-sports/requirements.txt

export OTEL_SERVICE_NAME=shopmate-ai
export OTEL_EXPORTER_OTLP_ENDPOINT=http://student-collector:4318
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
export OTEL_INSTRUMENTATION_GENAI_EMITTERS=span_metric
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_ONLY
export OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta
export OTEL_RESOURCE_ATTRIBUTES="deployment.environment=student-01"

export NIM_BASE_URL="http://nim-service.nim-system.svc.cluster.local:8000/v1"
export NIM_API_KEY="..."
export NIM_MODEL="meta/llama-3.2-1b-instruct"

opentelemetry-instrument python shopmate-sports/server.py
```

The app disables OpenAI Agents SDK native tracing by default to avoid sending
traces to OpenAI when NIM is the backend. Splunk/OpenTelemetry zero-code
instrumentation still wraps the OpenAI and OpenAI Agents libraries. To change
that behavior:

```bash
export SHOPMATE_DISABLE_OPENAI_AGENT_TRACING=false
```

## Monitoring Model

Splunk Observability data comes from two layers:

- OpenAI Agents SDK activity from `splunk-otel-instrumentation-openai-agents`.
- OpenAI-compatible NIM calls from `splunk-otel-instrumentation-openai`.
- Custom `shopmate.workflow` and `shopmate.agent.*` spans that describe the app-owned workflow.
- The standard `deployment.environment` filter from `OTEL_RESOURCE_ATTRIBUTES`.

The custom spans are intentionally simple. They add workflow names, agent names,
short safe previews, and estimated response size. They do not emit custom
metrics, JSONL telemetry, or real customer data.

The custom spans use `shopmate.*` attributes instead of `gen_ai.*` agent
attributes. Zero-code OpenAI Agents SDK instrumentation owns the Agent Flow; the
custom spans provide app context without duplicating AI agent nodes.

The response still includes approximate token counts for the storefront token
meter. Those values are UI feedback, not the monitoring source of truth.

## Product Asset Generation

The checked-in PNG product images are generated from local SVG templates:

```bash
python3 shopmate-sports/tools/generate_product_assets.py
```

If `rsvg-convert` is available, PNGs are generated. Otherwise the SVG files are
still written and the app can be adjusted to use them directly.
