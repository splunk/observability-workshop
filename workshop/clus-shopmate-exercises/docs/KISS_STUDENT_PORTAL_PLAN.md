# KISS Student Portal Plan

## Summary

Build a very small student portal for the Cisco Live lab. The portal does not create cloud infrastructure during class. It only lets a student claim one prepared lab workspace from a pool that was created before the event.

Event model:

- 20 normal student workspaces: `student-01` through `student-20`
- 5 instructor-controlled ttyd fallback workspaces: `web-01` through `web-05`
- one shared class password for student claims
- one instructor admin password for reset/support tasks
- no student accounts
- no database server
- no live Terraform provisioning

The goal is to make event-day access simple without adding meaningful cost or operational risk.

## Design Principles

- Keep provisioning out of the portal.
- Prepare namespaces, RBAC, secrets, kubeconfigs, apps, and access values before class.
- Let the portal assign prepared seats atomically.
- Use one small SQLite file for state.
- Run one portal replica to avoid SQLite write contention.
- Keep real kubeconfigs, passwords, and Splunk tokens out of git.
- Reuse the existing EKS cluster and ingress.

## Student Flow

1. Student opens the lab portal URL.
2. Student enters the class password.
3. Portal assigns the first available `student-*` workspace.
4. Portal sets a signed browser cookie for the claim.
5. Portal shows the workspace page with:
   - student ID
   - namespace
   - team, department, cost center, and chargeback values
   - Splunk URL and realm
   - Splunk lab ingest token or token Secret name, depending on final token handling
   - ShopMate app URL
   - workshop guide URL
   - kubeconfig download
   - `lab.env` download
   - quick validation commands

If the student refreshes the page, the signed cookie returns them to the same workspace.

## What Provisioning Means

For this portal, provisioning means:

- claim a prepared workspace
- mark that workspace as unavailable for other students
- serve that workspace's access bundle

Provisioning does not mean:

- creating Kubernetes namespaces live
- running Terraform
- creating IAM resources
- creating Splunk users
- creating NVIDIA/NIM access
- creating load balancers

## Portal Components

Add a new `lab-portal/` service with:

- `app.py`: routes and SQLite claim logic
- `admin.py`: simple instructor CLI for list/reset/support
- `templates/`: minimal HTML
- `static/`: minimal CSS
- `Dockerfile`
- `README.md`
- `sample-seats.csv`: fake sample data only

Do not commit real seat files, kubeconfigs, Splunk tokens, or passwords.

Recommended runtime:

- Python standard library or a small Flask app
- SQLite mounted on a small persistent volume
- one pod replica
- `ClusterIP` service
- shared ingress path such as `/portal`

## Data Model

Use one SQLite table for seats.

Suggested columns:

```text
seat_id
seat_type
namespace
student_id
team
department
cost_center
chargeback_account
splunk_url
splunk_realm
splunk_token_ref
shopmate_url
workshop_url
kubeconfig_path
lab_env_path
claimed_at
claim_token_hash
admin_note
```

Seat types:

```text
student
fallback_ttyd
```

Only `student` seats are claimable from the student page.

`fallback_ttyd` seats are visible only to instructor/admin tooling.

## Student Endpoints

```text
GET  /
POST /claim
GET  /workspace
GET  /workspace/kubeconfig
GET  /workspace/lab.env
POST /logout-local
```

Endpoint behavior:

- `GET /`: show class password form.
- `POST /claim`: validate class password and atomically claim one unclaimed `student` seat.
- `GET /workspace`: show the claimed workspace based on signed cookie.
- `GET /workspace/kubeconfig`: download only the claimed seat's kubeconfig.
- `GET /workspace/lab.env`: download only the claimed seat's environment file.
- `POST /logout-local`: clear only the local browser cookie; it does not release the seat.

Do not automatically release seats from the student UI. Seat release should be instructor-controlled.

## Instructor Reset Path

An admin reset path is useful, but it should stay tiny.

Primary support path:

```bash
python lab-portal/admin.py list
python lab-portal/admin.py reset student-07
python lab-portal/admin.py note student-07 "Moved to web-02"
```

Optional web admin page:

```text
GET  /admin
POST /admin/reset/<seat_id>
POST /admin/note/<seat_id>
```

The web admin page should only provide:

- list seats
- show available/claimed status
- show claim timestamp
- reset a mistaken claim
- add a support note

No roles, no user management, no complex audit UI.

Protect admin access with one instructor admin password.

## ttyd Fallback Integration

Keep ttyd fallback seats separate from the default student flow.

The portal admin view or CLI may show:

```text
web-01 -> https://<lab-host>/shell/web-01
web-02 -> https://<lab-host>/shell/web-02
web-03 -> https://<lab-host>/shell/web-03
web-04 -> https://<lab-host>/shell/web-04
web-05 -> https://<lab-host>/shell/web-05
```

Do not show ttyd fallback links on the normal student workspace page.

If a student needs a browser shell:

1. Instructor assigns the next available `web-*` fallback.
2. Instructor gives that student the private ttyd URL/password.
3. Instructor records a note in the portal CLI/admin page.

## Secrets And Generated Files

Keep these out of git:

- real `seats.csv` or `seats.json`
- SQLite runtime database
- kubeconfig files
- generated `lab.env` files
- class password
- admin password
- cookie signing key
- Splunk ingest token
- ttyd shell passwords

Recommended gitignore patterns when implementation starts:

```text
lab-portal/data/
lab-portal/runtime/
lab-portal/*.db
lab-portal/seats.csv
lab-portal/seats.json
```

## Event Setup

Before class:

1. Create the EKS cluster and platform services.
2. Create 20 student namespaces and RBAC.
3. Create 5 ttyd fallback namespaces and RBAC.
4. Preload required namespace secrets.
5. Deploy or validate ShopMate and collector baseline resources.
6. Generate kubeconfigs and `lab.env` files.
7. Generate the real seat inventory file outside git.
8. Start the portal with the seat inventory mounted.
9. Test several student claims.
10. Test admin reset.
11. Test all ttyd fallback shells privately.

During class:

1. Share the portal URL and class password.
2. Students claim normal workspaces.
3. Instructor uses CLI/admin reset only for mistakes.
4. Instructor assigns ttyd fallback seats only when laptop setup fails.

After class:

1. Export or save claim notes if needed.
2. Delete generated kubeconfigs and `lab.env` files.
3. Rotate/delete Splunk lab tokens.
4. Delete or rotate ttyd passwords.
5. Destroy or scale down lab infrastructure.

## Cost Control

Expected incremental cost is near zero if:

- the portal runs in the existing EKS cluster
- the portal reuses existing ingress
- the portal uses SQLite instead of a managed database
- there is only one portal replica
- ttyd shells reuse the existing ingress and nodes

Avoid:

- managed database
- new ALB only for the portal
- one `LoadBalancer` per shell
- live Terraform from the portal
- per-student portal accounts

## Test Plan

Local tests:

- import fake sample seats
- class password required
- one browser claims one seat
- refresh returns to the same workspace
- two simultaneous claims do not receive the same seat
- kubeconfig download is limited to the claimed seat
- `lab.env` download is limited to the claimed seat
- admin CLI can list seats
- admin CLI can reset a seat
- reset seat can be claimed again

Dry-run tests:

- load 20 real student seats
- simulate all 20 claims
- confirm every claim gets a unique namespace
- confirm no `fallback_ttyd` seat is student-claimable
- validate a sample kubeconfig with `kubectl auth can-i`
- confirm cross-namespace access fails
- confirm admin can reset a bad claim in under 1 minute

## Acceptance Criteria

- Students can claim prepared workspaces from one URL.
- No student account creation is required.
- The portal does not create Kubernetes or AWS resources live.
- A claimed workspace cannot be claimed by another student.
- Instructor can reset a mistaken claim.
- ttyd fallback seats remain instructor-controlled.
- No real secrets are committed to git.
- Incremental cost stays near zero by reusing existing EKS and ingress.
