---
title: Splunk Show release notes
build:
  list: never
  render: never
---

# Splunk Show release notes — Observability Cloud (2026)

Instructor / Splunk Show only. This file is not published (`build.list` / `build.render` never) so it does not become a page under the workshop hero.

Copy the block below into Slack.

---

*o11y-rookies-26 1.0.0 — Splunk Show launch*

New modular rookies workshop. Lab app is Astronomy Shop (OTel Demo), not Online Boutique. English only. Do not use the deprecated 1h/2h workshops for new Show sessions.

*Live modules (what Hugo shows attendees)*
• Introduction to Observability Cloud — 60 min (shop, login, RUM, APM, logs, Synthetics)
• Finding the needle in the Logs — 45 min (log-first triage)
• Application Security — 45 min
• Digital Experience Analytics — 45–60 min

*Not ready — do not schedule*
AI, APM deep-dive, DEM, DB-mon, and Pathways (still hidden). IM is a **draft** (`hugo server -D` only) — four Flagd K8s scenarios, still needs Astronomy Shop **2.0.9+** with `k8s-scenario-controller` and a screenshot pass.

*Show operators*
• Boot the Show instance ~30 min early (EC2 build after boot)
• Feature flags: current rec is for *Intro* — on `/Feature`, disable all demos except paymentFailure @ 50%
• Other modules may need a different Feature config — check the Presenter notes at the start of each workshop
• IM (when scheduled on 2.0.9+): enable `S-*` flags **in order**, one per scenario; leave S-TEST-shelltester off. Cluster filter is `[NAME OF WORKSHOP]-k3d-cluster`
• Logs Scenario 2 is still TBD in the nav — stop after Scenario 1

*Presenter mode (needed to see those notes)*
Three ways to toggle, after unlock:
1. Append `?presenter=1` to the URL once — unlocks presenter controls in this browser and turns presenter mode on
2. Click the pill — after unlock, use the floating “Presenter” button bottom-right on pages with notes
3. Press P twice quickly — after unlock, same effect with no mouse

Unlock + mode persist in localStorage for that browser profile as you navigate.
