# Rehearsal Plan

This page assumes you have about four hours until the workshop.

## Hour 1: environment readiness

Target outcome:

- dependencies installed
- `.env` prepared with a unique `INSTANCE`
- collector decision made
- app stack starts cleanly

Checklist:

1. verify Node, Python, and Docker
2. populate `.env`
3. run `npm install`
4. create the remediation agent virtual environment
5. start `npm run dev:all`
6. confirm the portal and operator console load

## Hour 2: technical validation

Target outcome:

- healthy baseline proven
- cache-pressure trigger proven
- remediation path proven

Checklist:

1. run all three portal transactions in healthy mode
2. click `Trigger Cache Pressure`
3. re-run `AI Claim Status`
4. confirm the other two journeys remain usable
5. step through the operator console
6. approve `clean_claims_knowledge_cache`
7. validate recovery

If Splunk telemetry matters for your talk, validate RUM/APM/filesystem signals in this hour.

## Hour 3: presenter rehearsal

Target outcome:

- clear narration
- no handoff confusion
- consistent Splunk-to-console transitions

Checklist:

1. rehearse the portal explanation
2. rehearse the cache-pressure trigger
3. rehearse where to click in Splunk
4. rehearse the evidence-to-action explanation
5. rehearse approval and validation

## Hour 4: stabilization

Target outcome:

- known-good terminals
- browser windows arranged
- fallback evidence text ready

Checklist:

1. restart only if necessary
2. clear stale browser tabs
3. keep one terminal on the app stack
4. keep another terminal on the collector if telemetry is part of the rehearsal
5. bookmark the fallback story if live signals drift

## Final 15-minute checklist

1. portal loads on `18080`
2. operator console loads on `18081`
3. one healthy claim status response works
4. cache pressure can still be triggered
5. presenter knows the fallback narrative

## Avoid last-minute changes

- changing ports
- changing telemetry strategy
- adding new demo scope
- refactoring non-critical code
