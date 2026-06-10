#!/bin/zsh
set -euo pipefail

ROOT="/Users/mkuglerr/code2/codex_projects/ai-pods"
OUT_DIR="$ROOT/deliverables"
KEY_FILE="$OUT_DIR/CLUS-LTROBS-2001.key"
PPTX_FILE="$OUT_DIR/CLUS-LTROBS-2001.pptx"

osascript <<'APPLESCRIPT'
on add_bullets(theSlide, slideTitle, bulletList)
  tell theSlide
    set object text of default title item to slideTitle
    set object text of default body item to bulletList
  end tell
end add_bullets

tell application "Keynote"
  activate
  set theDoc to make new document with properties {document theme:theme "White"}

  tell theDoc
    my add_bullets(current slide, "CLUS-LTROBS-2001", "From Deployment to Deep Insights: Mastering AI/ML with Cisco AI Pods & Splunk" & return & "Cisco Live 4-hour instructor-led lab" & return & "Workshop-based delivery model with shared AWS EKS infrastructure")

    set s2 to make new slide
    my add_bullets(s2, "Lab Goal", "Teach students how to instrument AI workloads and collect telemetry" & return & "Show how to configure Splunk OpenTelemetry collectors in Kubernetes on EKS" & return & "Explore GPU, platform, and AI workload views in Splunk Observability Cloud" & return & "Use a hands-on workflow instead of a product overview")

    set s3 to make new slide
    my add_bullets(s3, "Why Build on EKS", "The lab uses one shared AWS EKS cluster with GPU-backed AI services" & return & "It includes EKS, NVIDIA GPU Operator, NIM, and dashboard review flows" & return & "Students perform real setup tasks in their own namespace" & return & "Terraform keeps the event environment repeatable across dry runs and delivery")

    set s4 to make new slide
    my add_bullets(s4, "40-Student Lab Architecture", "One shared AWS EKS cluster with GPU-backed shared services" & return & "Student laptops connect with namespace-scoped Kubernetes access" & return & "One Kubernetes identity and one namespace per student" & return & "One namespace-scoped collector and app workflow per student" & return & "One shared Splunk Observability Cloud organization")

    set s5 to make new slide
    my add_bullets(s5, "What Is Shared", "AWS EKS cluster and operators" & return & "GPU nodes and shared AI services" & return & "NIM models and shared platform services" & return & "Cluster-level infrastructure monitoring components" & return & "Splunk organization and core dashboards")

    set s6 to make new slide
    my add_bullets(s6, "What Each Student Does", "Connect to EKS with assigned namespace-scoped Kubernetes credentials" & return & "Work inside a dedicated namespace" & return & "Deploy or update their own Splunk OTel Collector" & return & "Configure receivers, processors, and exporters" & return & "Validate data in Splunk and explore dashboards" & return & "Investigate a bounded agent-loop token burn scenario")

    set s7 to make new slide
    my add_bullets(s7, "What Students Learn", "Difference between infrastructure telemetry and application telemetry" & return & "How Prometheus scrape and OTLP ingest work together" & return & "How metadata and dimensions affect dashboards and filtering" & return & "How GPU, application, and platform signals correlate" & return & "How repeated agent calls can burn tokens before guardrails stop them" & return & "How to move from symptom to root-cause hypothesis")

    set s8 to make new slide
    my add_bullets(s8, "4-Hour Agenda", "20 min: Architecture, objectives, and environment orientation" & return & "45 min: Access lab environment and verify namespace resources" & return & "60 min: Deploy and configure the Splunk OTel Collector" & return & "45 min: Review GPU, AI POD, and supporting dashboards" & return & "40 min: Instrument or validate app telemetry and traces" & return & "30 min: Agent-loop token burn, chargeback debrief, and Q&A")

    set s9 to make new slide
    my add_bullets(s9, "Instructor Prep", "Pre-create student identities, namespaces, credentials, and quotas" & return & "Pre-stage cluster services, models, and shared backends" & return & "Validate kubectl, Helm, kubeconfig, and workshop files before delivery" & return & "Validate Splunk tokens, realm, and dashboard access" & return & "Run a scale test for 40 collectors before the event")

    set s10 to make new slide
    my add_bullets(s10, "What We Should Improve", "Add a Cisco Live specific intro and learning objective slide" & return & "Add a clear architecture diagram before hands-on steps" & return & "Add explicit checkpoints after each major exercise" & return & "Add troubleshooting prompts for token surge, agent-loop token burn, and chargeback gaps" & return & "Add a final production-readiness and takeaways section")

    set s11 to make new slide
    my add_bullets(s11, "Recommended Positioning", "Present this as a Cisco Live lab built on a shared Cisco AI Pods-style environment" & return & "Emphasize hands-on instrumentation, collection, and analysis" & return & "Be explicit about what is shared platform setup versus student-owned work" & return & "Keep the story operational: collect, validate, analyze, troubleshoot")

    set s12 to make new slide
    my add_bullets(s12, "Next Steps", "Finalize the 40-student namespace and credential model" & return & "Adapt the workshop guide into Cisco Live instructor and attendee guides" & return & "Build an architecture diagram and event runbook" & return & "Dry-run the lab with full concurrency before conference delivery")

    save in POSIX file "/Users/mkuglerr/code2/codex_projects/ai-pods/deliverables/CLUS-LTROBS-2001.key"
    export to POSIX file "/Users/mkuglerr/code2/codex_projects/ai-pods/deliverables/CLUS-LTROBS-2001.pptx" as Microsoft PowerPoint
    close saving no
  end tell
end tell
APPLESCRIPT

echo "Generated:"
echo "$KEY_FILE"
echo "$PPTX_FILE"
