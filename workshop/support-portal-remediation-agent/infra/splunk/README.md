# Splunk Object Workflow

This directory is the new authoring path for demo dashboards and detectors.

## Why This Exists

- Terraform is still available under `infra/terraform` for the current deployed estate.
- Dashboard and detector changes now have a simpler spec-driven workflow that is easier to diff, test, and review.
- The Cloudflare tunnel remains unchanged for now. The rendered detector runbook URL still reads `ORCHESTRATOR_PUBLIC_WEBHOOK_URL`.

## Files

- `specs/dashboard-group.json`: dashboard group source of truth
- `specs/dashboards.json`: dashboard definitions
- `specs/detectors.json`: detector definitions
- `sync_splunk_objects.py`: renders specs and can POST them to the Splunk API
- `.object-ids.json`: local manifest of remote object IDs used for update-aware applies

## Render Payloads

```bash
python3 infra/splunk/sync_splunk_objects.py
```

Or from the repo root:

```bash
make splunk-render
```

## Apply Payloads

```bash
SPLUNK_ACCESS_TOKEN=... python3 infra/splunk/sync_splunk_objects.py --apply
```

Or from the repo root:

```bash
make splunk-apply
```

## Run Python Tests

```bash
make test-python
```

## Notes

- This script currently uses `POST` for object creation/upsert-style workflow staging. If the target org already contains the objects, add ID-aware update semantics in a follow-up.
- The script now stores remote IDs in `.object-ids.json` and switches to `PUT` on later applies when an object ID is known.
- The immediate value is that the objects are now authored from stable JSON specs and can be unit tested offline.
