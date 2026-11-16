# Healthcare Assistant — Multi-Tenant Demo Architecture

This document describes the target architecture for running the Healthcare Assistant
demo so that **multiple presenters can deliver demos in parallel**, each with their own
agent stream and their own Agent Control configuration, from a **single shared URL**.

Read this before changing `app.py`, `agent.py`, the Agent Control wiring, or the k8s
manifests. It explains *why* the app is split the way it is — several of the constraints
below are non-obvious and easy to regress.

---

## 1. The problem we're solving

Today the demo runs as a single monolithic Streamlit pod per target:

- All traces land in one project (`Healthcare Assistant Demo`) / one agent stream
  (`default`), so presenters can't find their own traces — especially with parallel demos.
- **Agent Control is the real blocker.** The PII-removal control is attached to the agent
  stream. With everyone sharing one stream, presenter 2 toggling the control on/off
  corrupts presenter 1's demo. The current workaround (a control *condition* requiring the
  presenter's name in the prompt) is fragile.
- Three separate deployments (`standalone`, `US Splunk Show`, `EU Splunk Show`) each bake
  their target into ConfigMaps, so target choice is a deploy-time decision, not a
  launch-time one.
- The UI is bare-bones.

## 2. The load-bearing constraint

**`agent_control.init()` configures process-global state, and one OS process can be bound
to exactly one `(agent_stream, target)` at a time.**

Evidence in this repo:
- `helpers/agent_control_helpers.py` guards init with a module-level `_initialized` flag
  and `init_agent_control._last_session_key`. The `agent_control` SDK itself keeps a
  singleton client/target.
- Streamlit runs **one Python process for all browser sessions**. `st.session_state` is
  per-browser, but module globals (`_bg_loop` in `agent.py`, the `agent_control` singleton)
  are shared. Two presenters on one pod therefore share one Agent Control target.

Consequence: **isolation must happen at the process (pod) level.** Every distinct
`(agent_stream, target)` needs its own process. This is the single fact that drives the
entire design — do not try to make one process serve multiple agent streams with Agent
Control enabled.

> If someone later claims the SDK supports re-`init()` or per-call target override, verify
> it directly against the installed `agent-control-sdk` before collapsing the pod-per-stream
> model. Even then, Streamlit's shared-process model means concurrent sessions would still
> race on the singleton, so the split below remains the safe design.

## 3. Target architecture

Split the monolith into a **front-end** (always running, single public URL) and **back-end
agent services** (one per `(agent_stream, target)`, created on demand). Crucially, the
**browser only ever talks to the front-end**; the front-end calls back-ends server-side
over in-cluster HTTP. We do *not* route browser/websocket traffic to per-stream pods.

```
                         single DNS (healthcare-assistant.splunko11y.com)
                                      │  (Traefik basic auth — unchanged)
                                      ▼
┌──────────────────────────────────────────────────────────────────────┐
│  FRONT-END POD (always on)  — Streamlit UI                             │
│   • Setup screen: agent stream name + target (standalone / US / EU)    │
│   • Chat UI (the slick one, built in phase 2)                          │
│   • Holds per-browser session state: {stream, target, backend_url}     │
│   • ORCHESTRATOR: ensure a back-end exists for (stream,target),        │
│     wait for readiness, remember its in-cluster Service URL            │
│   • Forwards each chat turn: POST http://<backend-svc>:8000/query      │
└───────────────┬────────────────────────────────┬─────────────────────┘
                │ in-cluster HTTP                 │
                ▼                                 ▼
┌───────────────────────────────┐   ┌───────────────────────────────┐
│ BACK-END POD (on demand)      │   │ BACK-END POD (on demand)      │
│ stream="derek" target=US      │   │ stream="maria" target=EU      │
│  • FastAPI wrapping           │   │  • FastAPI wrapping           │
│    HealthcareAgent            │   │    HealthcareAgent            │
│  • agent_control.init() ONCE  │   │  • agent_control.init() ONCE  │
│    at startup for this stream │   │    at startup for this stream │
│  • emits traces to US stream  │   │  • emits traces to EU stream  │
│  • POST /query, GET /healthz  │   │  • POST /query, GET /healthz  │
└───────────────────────────────┘   └───────────────────────────────┘
        (shared Postgres/pgvector; RAG reads the same collection)
```

### Why this shape

| Requirement                               | How it's met                                                            |
|-------------------------------------------|-------------------------------------------------------------------------|
| Single DNS for all users                  | Only the front-end has an Ingress. Back-ends are `ClusterIP`-only.      |
| Per-presenter agent stream                | One back-end process per stream; traces grouped by that stream.         |
| Agent Control with no cross-demo conflict | `agent_control.init()` runs once per back-end process → full isolation. |
| Choose target at launch                   | Orchestrator injects the chosen target's creds/URLs into the back-end pod env. |
| Front-end always up, back-end on demand   | Front-end Deployment is permanent; back-ends created per `(stream,target)`. |
| Improve UI later                          | UI (front-end) is fully decoupled from agent logic (back-end HTTP API). |

## 4. Component responsibilities

### Front-end (`app.py` + a new orchestrator module)
- Keep **Traefik basic auth at the ingress** (`password-protection/`) — that is the
  "usual username and password". Do **not** reimplement it in the app.
- Add a **setup screen** shown before chat when `st.session_state` has no `stream`/`target`:
  - text input: *Agent stream name* (validate → DNS-safe; see §6).
  - radio/select: *Target* → `standalone` | `us-splunk-show` | `eu-splunk-show`.
- On submit, call the orchestrator to **ensure-backend(stream, target)**; show a spinner
  while the pod becomes Ready (cold start — see §7); store `backend_url` in session state.
- Replace the in-process `HealthcareAgent` call in `process_input()` with an HTTP call:
  `POST {backend_url}/query` with the conversation messages; render the response.
- The front-end no longer imports `agent.py`, `rag.py`, or `agent_control`. It holds **no**
  agent/LLM/Agent-Control state. This keeps the UI light and lets us iterate on it freely.

### Back-end (new `server.py`, same image or a trimmed one)
- FastAPI service. On startup read env: `SPLUNK_AO_AGENT_STREAM`, `SPLUNK_AO_PROJECT`, and
  the target-specific creds/URLs (same env vars `setup_env.py` validates today).
- Construct one `HealthcareAgent`, start the splunk_ao session, and call
  `agent_control.init()` **exactly once** (reuse `agent.py` / `agent_control_helpers.py`
  logic — it already starts a session before init so `agent_stream_id` resolves).
- Endpoints:
  - `POST /query` → `{ "messages": [...] }` → runs `HealthcareAgent.process_query`,
    returns `{ "response": "..." }`. Preserve the existing steering/blocking behavior.
  - `GET /healthz` / `GET /ready` → readiness (RAG warmed, agent control initialized).
- `agent.py`'s shared-background-loop pattern (`_get_background_loop`) stays valid and is
  actually cleaner here: one process, few concurrent callers.

### Orchestrator (inside the front-end pod, or a tiny sidecar service)
- Given `(stream, target)`, deterministically derive a name:
  `backend-<target>-<slug(stream)>` (slug = lowercase, DNS-1123, hashed suffix for
  uniqueness/overflow — see §6).
- If a Deployment+Service with that name exists and is Ready → return its URL.
- Else create a **Deployment + ClusterIP Service** from a template, injecting:
  - `SPLUNK_AO_AGENT_STREAM = <stream>`
  - the target's ConfigMaps/Secret (standalone → `splunk-ao-config` + `splunk-ao-secret`;
    US → `*-us-splunk-show`; EU → `*-eu-splunk-show`) — these already exist in the cluster.
  - a `demo.splunk/last-used` timestamp annotation (for GC).
- Wait for `/ready`, return `http://<svc>.<ns>.svc.cluster.local:8000`.
- Uses the in-cluster ServiceAccount token + Kubernetes Python client. See §8 for RBAC.

## 5. Target selection — mapping to existing config

The three targets already exist as ConfigMaps/Secrets in the cluster; reuse them rather
than inventing new config. The orchestrator picks which to mount per back-end:

| Target UI value   | ConfigMaps                                                            | Secret                         | Auth var              |
|-------------------|-----------------------------------------------------------------------|--------------------------------|-----------------------|
| `standalone`      | `splunk-ao-config`, `splunk-agent-control-config`                     | `splunk-ao-secret`             | `SPLUNK_AO_API_KEY`   |
| `us-splunk-show`  | `splunk-ao-config-us-splunk-show`, `splunk-agent-control-config-us-splunk-show` | `splunk-ao-secret-us-splunk-show` | `SPLUNK_AO_O11Y_TOKEN` |
| `eu-splunk-show`  | `splunk-ao-config-eu-splunk-show`, `splunk-agent-control-config-eu-splunk-show` | `splunk-ao-secret-eu-splunk-show` | `SPLUNK_AO_O11Y_TOKEN` |

- `SPLUNK_AO_AGENT_STREAM` from the ConfigMap is **overridden** per back-end with the
  user-entered stream (env set directly on the pod wins over `envFrom`).
- `setup_env.py`'s standalone-vs-O11y detection (`SPLUNK_AO_O11Y_VARS` vs
  `SPLUNK_AO_STANDALONE_VARS`) continues to work unchanged inside the back-end pod.
- The current three `k8s-demo-o11y-*` / `k8s-demo-standalone.yaml` Deployments become
  obsolete as *standing* deployments; their env wiring is the template the orchestrator
  reuses. Keep them around until the new model is proven.

## 6. Agent stream naming (DNS safety)

Stream names become part of k8s object names and must be DNS-1123 compliant
(`[a-z0-9-]`, ≤63 chars, no leading/trailing `-`). In the setup screen:
- Lowercase, replace non-alphanumerics with `-`, collapse repeats, trim.
- Append a short hash of the original string to avoid collisions after slugging and to
  keep a stable name when the same presenter returns.
- Keep the **original** (unslugged) stream name as the value passed to
  `SPLUNK_AO_AGENT_STREAM` so the Observability UI shows the human-friendly name; only the
  **k8s object name** uses the slug.

## 7. Cold start — the main UX risk

A brand-new back-end must: schedule → pull image → start → warm RAG (pgvector connection +
embeddings) → `agent_control.init()`. This is **not instant**. Mitigations, in order of
preference:
1. **Readiness gating + spinner** in the setup screen ("Provisioning your demo
   environment…"). Simplest; always needed regardless of other mitigations.
2. **Pre-pulled image** on nodes (`imagePullPolicy: IfNotPresent` once a known tag is
   cached) to cut the biggest chunk of latency.
3. **Warm standby (optional):** keep one idle back-end per target that gets "claimed" and
   relabeled on first use, provisioning its replacement in the background. Adds complexity;
   only do this if the spinner wait proves too long in practice.

Reuse across a presenter's session is automatic: the orchestrator returns the existing
back-end for a `(stream, target)` it already created, so only the *first* query pays the
cold-start cost.

## 8. Orchestration mechanics & RBAC

- Front-end pod runs under a dedicated **ServiceAccount** with a namespaced **Role**:
  `create/get/list/watch/update/patch/delete` on `deployments` (apps) and
  `create/get/list/delete` on `services` (core), scoped to the demo namespace only. This is
  a real privilege — keep it namespace-scoped; never grant cluster-wide. `update`/`patch`
  are required for reconcile and the last-used annotation (below). The back-end shares this
  ServiceAccount so it can stamp its annotation and self-delete.
- Prefer **Deployment+Service per back-end** over bare Pods (self-healing, stable DNS via
  the Service). One replica each.
- **Garbage collection** (prevents pod sprawl across many demos):
  - Each back-end stamps a `demo.splunk/last-used` epoch annotation on its own Deployment
    from its idle-watcher loop (every 60s) — no per-query API overhead. The orchestrator
    stamps it once at creation too.
  - Back-ends **self-terminate** when idle past `BACKEND_IDLE_TTL_SECONDS` (delete own
    Service+Deployment, then exit). See §12 / §13.
- **Idempotency / concurrency:** the back-end name is derived deterministically from
  `(stream, target)`, so "ensure" is naturally idempotent: an existing Deployment is
  *patched* to the desired spec (rolling update only if the template changed), and a 409 on
  the Service is treated as reuse. Races (two presenters, same stream name) collapse onto
  the same object.

## 9. Build & deploy notes

- **One image, two entrypoints** is simplest: the same image runs either
  `streamlit run app.py` (front-end) or `uvicorn server:app` (back-end), chosen by the
  Deployment's `command`. Avoids image drift between the two roles.
- Postgres/pgvector (`postgres.yaml`) and the vector-DB setup job (`setup-job.yaml`) stay
  shared and unchanged — RAG is read-mostly and identical across streams/targets.
- Keep the existing `ghcr.io/splunk/healthcare-assistant` repo; bump the tag.

## 10. Build order (incremental, each step demoable)

1. **Extract the back-end API.** Add `server.py` (FastAPI) wrapping the *existing*
   `HealthcareAgent`; `agent_control.init()` once at startup from env. Verify one back-end
   pod works end-to-end (traces + Agent Control) for a single hard-coded stream/target.
   *No orchestration yet.*
2. **Thin the front-end.** Change `app.py` to call the back-end over HTTP instead of
   importing the agent. Add the setup screen (stream + target). Point it at a manually
   created back-end to validate the UI/HTTP contract.
3. **Add the orchestrator + RBAC.** Front-end creates/reuses back-ends on demand; readiness
   spinner; deterministic naming; `AlreadyExists` handling.
4. **Add GC** (TTL annotation + reaper).
5. **Polish the UI** once the plumbing is proven — this is now isolated to the front-end
   and can't regress agent/Agent-Control behavior.

## 11. Invariants — don't regress these

- A back-end process is bound to **one** `(agent_stream, target)` for its whole life.
  Never call `agent_control.init()` more than once per process, and never reuse a back-end
  for a different stream.
- `agent.py` starts the splunk_ao **session before** `agent_control.init()` so
  `agent_stream_id` (the Agent Control `target_id`) resolves. Preserve that ordering in
  `server.py` startup.
- The front-end carries **no** agent/LLM/Agent-Control state and does not import `agent.py`.
- Only the front-end is exposed via Ingress; back-ends are `ClusterIP` only. Single DNS is
  an outcome of this — don't add per-stream Ingresses.
- Keep basic auth at the Traefik ingress; don't move it into the app.
- `SPLUNK_AO_AGENT_STREAM` env on the pod must be the **user-entered** stream, overriding
  the ConfigMap default; the k8s object name uses the slug, the trace stream uses the
  original name.

## 12. Decisions (confirmed 2026-10-06)

- **Orchestrator location:** embedded in the front-end pod. (Revisit only if it complicates
  the UI.)
- **Cold start:** readiness spinner only for v1 — no warm standby.
- **GC owner:** back-end **self-terminates on idle**. It tracks its own last-activity and,
  past the idle TTL, deletes its own Service + Deployment via the k8s API (so there is no
  restart) and exits. A CronJob backstop can be added later if needed.

### Resource requirements (tuned down from the monolith)

The monolith's `requests 512Mi/250m, limits 2Gi/1000m` is overkill. Starting points —
observe real usage and tune:

| Pod       | requests        | limits          | Rationale                                            |
|-----------|-----------------|-----------------|------------------------------------------------------|
| front-end | `128Mi` / `100m`| `512Mi` / `500m`| Streamlit UI + HTTP client + k8s calls; no LLM/RAG.  |
| back-end  | `256Mi` / `100m`| `1Gi` / `500m`  | LangGraph + pgvector client; LLM/embeddings are network-bound, not CPU-bound. |

## 13. Capacity & concurrency (single-node EC2/k3d)

The pod-per-stream model is **memory-bound** on a single node — each back-end carries a
heavy Python/langchain working set (~0.5–0.75 GiB resident), while LLM calls are
network-bound so CPU stays mostly idle.

**Rough parallel-back-end capacity** (after ~1.5 GiB system + ~0.75 GiB Postgres +
~0.3 GiB front-end):

| Instance    | vCPU / RAM  | ~Parallel back-ends |
|-------------|-------------|---------------------|
| t3.large    | 2 / 8 GiB   | ~6–8                |
| t3.xlarge   | 4 / 16 GiB  | ~16–18              |
| t3.2xlarge  | 8 / 32 GiB  | ~35–40              |

Caveats: t3 is **burstable** — a packed room can exhaust CPU credits; prefer `m6i`/`m7i`
for heavy workshops. The back-end memory *request* (`256Mi`) under-counts real usage, so
do **not** rely on the scheduler alone to bound the node — it would overcommit and OOM-kill.
Hence the explicit app-level cap below.

**Cap + eviction (implemented):**
- `MAX_BACKEND_PODS` (env on the front-end, `0` = unlimited) bounds concurrent back-ends.
  Set it **explicitly per instance** using:
  `MAX_BACKEND_PODS = floor((NODE_RAM − 2.5 GiB overhead) / 0.75 GiB)` →
  t3.large ≈ 6, t3.xlarge ≈ 16, t3.2xlarge ≈ 35.
- When a **new** stream would exceed the cap, the orchestrator evicts the
  **least-recently-used** back-end (oldest `demo.splunk/last-used`, falling back to
  creation time) to make room — so a new presenter can always start. Reconciling an
  *existing* stream never triggers eviction.
- `BACKEND_IDLE_TTL_SECONDS` is set aggressively (20 min) to keep the steady-state pool
  lean; LRU eviction is the hard ceiling for bursts.

**Trade-off:** under genuine over-subscription, LRU eviction can reclaim a back-end from a
presenter who paused briefly. The aggressive TTL minimizes this; raising the instance size
(or `MAX_BACKEND_PODS`) is the real fix. For large-scale/elastic needs, a managed cluster
(EKS + cluster-autoscaler) scales horizontally beyond a single node — out of scope here.
