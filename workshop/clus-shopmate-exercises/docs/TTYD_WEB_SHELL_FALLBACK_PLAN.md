# ttyd Web-Shell Fallback Plan

## Summary

This plan adds a small emergency browser-shell option to the Cisco Live lab without changing the default student workflow.

Default model:

- 20 students use their own laptops and local terminal tools.
- 5 instructor-controlled web-shell seats are prepared as fallback capacity.
- Web shells are assigned only when a student cannot get their laptop environment working.

The selected web-shell tool is `ttyd` because it is a lightweight terminal server that can expose a shell over the browser with basic authentication, writable terminal mode, custom command support, and reverse-proxy base path support.

Reference:

- `ttyd`: https://github.com/tsl0922/ttyd

## Goals

- Keep the lab cheap and laptop-first.
- Avoid a full signup portal, user database, or per-student account workflow.
- Provide a reliable rescue path for up to 5 students.
- Reuse the existing EKS cluster and shared ingress.
- Avoid one load balancer per shell.
- Avoid adding a CPU node group unless dry-run testing proves it is required.

## Seat Model

Normal student seats:

```text
student-01
student-02
...
student-20
```

Fallback web-shell seats:

```text
web-01
web-02
web-03
web-04
web-05
```

Each fallback seat should have:

- its own Kubernetes namespace
- its own service account
- namespace-scoped Role and RoleBinding
- namespace-scoped kubeconfig
- its own ttyd deployment
- its own instructor-held shell password
- its own access package

Fallback identities may appear in Splunk as `web-01` through `web-05`. The instructor should keep an event-day mapping from fallback identity to actual student.

## Kubernetes Design

Use one namespace per fallback seat:

```text
web-01
web-02
web-03
web-04
web-05
```

Use the same namespaced permissions as a regular student:

- get/list/watch pods
- read pod logs
- create/update/delete deployments
- create/update/delete configmaps
- create/update/delete services
- create/update/delete secrets if the lab keeps that permission for students
- create/update/delete jobs if used by lab exercises
- create/update/delete ingresses if used by lab exercises

Do not grant:

- cluster-admin
- access to other student namespaces
- node or node group permissions
- cluster role modification
- GPU Operator modification
- instructor collector modification
- NIM platform modification

## ttyd Runtime Design

Run one ttyd deployment per fallback seat.

Each deployment should:

- run in the matching `web-0x` namespace
- use the matching namespace service account
- set low CPU and memory requests
- request no GPU
- mount or include the lab files
- load the matching kubeconfig by default
- start in the lab working directory
- run an interactive shell

Recommended ttyd command shape:

```bash
ttyd -W -c "$TTYD_USER:$TTYD_PASSWORD" -b "/shell/web-01" bash
```

Flags:

- `-W`: allow terminal write input because ttyd terminals are read-only by default.
- `-c`: enable simple username/password authentication.
- `-b`: set the base path for reverse-proxy routing.

Use one password per shell seat. Store passwords outside git.

## Tooling Image

Use a small tooling image that includes:

- `ttyd`
- `bash`
- `kubectl`
- `helm`
- `curl`
- `jq`
- CA certificates
- optional Git client if students need to inspect the repo

The image should not contain event secrets at build time.

Runtime secrets should be mounted from Kubernetes Secrets or injected by the event setup process.

## Ingress Design

Expose all fallback shells through one shared HTTPS ingress.

Example paths:

```text
https://<lab-host>/shell/web-01
https://<lab-host>/shell/web-02
https://<lab-host>/shell/web-03
https://<lab-host>/shell/web-04
https://<lab-host>/shell/web-05
```

Do not create one `LoadBalancer` service per shell.

Use `ClusterIP` services behind the shared ingress.

Ingress must support WebSocket traffic.

## Cost Control

Expected incremental cost is near zero if:

- the shell pods run on existing EKS nodes
- the shared ingress/load balancer is reused
- no new CPU node group is created
- no separate load balancers are created for individual shells

Do not add a CPU node group in v1. Add one only if dry-run testing shows the existing nodes cannot reliably schedule the shell pods.

## Instructor Runbook

Before the event:

1. Generate 20 normal student access packages.
2. Generate 5 fallback web-shell access packages.
3. Create or validate the 5 fallback namespaces.
4. Deploy and test all 5 ttyd shells.
5. Store shell URLs and passwords in an instructor-only roster.
6. Keep fallback shell links private.

During the event:

1. Start with laptop-first instructions.
2. Give students a short troubleshooting window if local setup fails.
3. Assign the next available fallback shell only when needed.
4. Record the student's name or email, assigned fallback seat, and reason.
5. Remind the student that their Splunk identity may appear as `web-0x`.

After the event:

1. Delete or rotate shell passwords.
2. Delete fallback kubeconfigs and access packages.
3. Rotate or delete lab-scoped Splunk ingest tokens.
4. Scale fallback ttyd deployments to zero or destroy them.
5. Remove any event-local files that contain secrets.

## Validation Checklist

Validate each fallback shell before the event:

```bash
kubectl config current-context
kubectl auth can-i get pods -n web-01
kubectl auth can-i get pods -n student-01
helm version
curl --version
jq --version
```

Expected results:

- Browser opens the shell URL.
- Password authentication works.
- Shell opens in the lab working directory.
- `kubectl config current-context` is set to the fallback seat.
- `kubectl auth can-i get pods -n web-01` returns `yes` from `web-01`.
- `kubectl auth can-i get pods -n student-01` returns `no` from `web-01`.
- `helm`, `curl`, and `jq` are available.
- All 5 shells can run at the same time.
- No extra load balancers are created.
- Shell pods do not request GPU resources.

## Acceptance Criteria

- 20 normal student seats remain the default lab path.
- 5 fallback web-shell seats are available but not advertised as the default.
- Each fallback shell is isolated to its own namespace.
- All fallback shells route through one shared ingress.
- No per-shell `LoadBalancer` services exist.
- No new CPU node group is required for v1 unless dry-run testing proves otherwise.
- Instructor can assign a fallback shell in less than 2 minutes during class.

## Open Implementation Notes

- The exact ingress annotations depend on the ingress controller selected for the event environment.
- The exact image build path should match the existing lab image publishing workflow.
- The fallback seat roster and passwords must remain outside source control.
