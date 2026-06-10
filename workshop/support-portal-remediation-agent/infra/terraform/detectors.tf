resource "signalfx_detector" "claims_knowledge_filesystem_pressure" {
  name = "IBOBS Claims Knowledge Cache Filesystem Pressure"

  program_text = <<-EOF
    A = data('${var.cache_utilization_metric}', filter=filter('deployment.environment', '${var.deployment_environment}') and filter('service.name', 'claims-knowledge') and filter('service.instance.id', '${var.instance}') and filter('mountpoint', '${var.cache_mountpoint}') and filter('demo.metric_source', '${var.evidence_metric_source}')).max(by=['service.name', 'service.instance.id', 'mountpoint']).publish(label='Claims Knowledge Cache Utilization')
    detect(when(A > ${var.filesystem_utilization_threshold}, lasting='2m')).publish('Claims Knowledge Cache Filesystem Pressure')
  EOF

  rule {
    detect_label  = "Claims Knowledge Cache Filesystem Pressure"
    severity      = "Critical"
    description   = "Claims knowledge cache utilization is above the lab threshold for the synthetic cache volume."
    runbook_url   = var.orchestrator_webhook_url
    notifications = local.detector_webhook_notifications
  }
}

resource "signalfx_detector" "claims_knowledge_latency" {
  name = "IBOBS Claims Knowledge APM Latency"

  program_text = <<-EOF
    A = data('${var.claim_status_latency_metric}', filter=filter('deployment.environment', '${var.deployment_environment}') and filter('service.name', 'claims-knowledge') and filter('service.instance.id', '${var.instance}') and filter('app.business_transaction', 'claim_status_response') and filter('demo.metric_source', '${var.evidence_metric_source}')).max(by=['service.name', 'service.instance.id', 'app.business_transaction']).publish(label='AI Claim Status Latency')
    detect(when(A > ${var.apm_latency_threshold_ns / 1000000}, lasting='2m')).publish('Claims Knowledge APM Latency')
  EOF

  rule {
    detect_label  = "Claims Knowledge APM Latency"
    severity      = "Major"
    description   = "AI Claim Status latency is elevated for the claims-knowledge service."
    runbook_url   = var.orchestrator_webhook_url
    notifications = local.detector_webhook_notifications
  }
}

resource "signalfx_detector" "claims_knowledge_error_rate" {
  name = "IBOBS Claims Knowledge APM Error Rate"

  program_text = <<-EOF
    A = data('service.request', filter=filter('deployment.environment', '${var.deployment_environment}') and filter('service.instance.id', '${var.instance}') and filter('sf_service', 'claims-knowledge') and filter('sf_error', 'true')).count()
    B = data('service.request', filter=filter('deployment.environment', '${var.deployment_environment}') and filter('service.instance.id', '${var.instance}') and filter('sf_service', 'claims-knowledge')).count()
    C = (A / B).publish(label='Error Rate')
    detect(when(C > ${var.apm_error_threshold}, lasting='2m')).publish('Claims Knowledge APM Error Rate')
  EOF

  rule {
    detect_label  = "Claims Knowledge APM Error Rate"
    severity      = "Major"
    description   = "Splunk APM service request error rate is elevated for the claims-knowledge service."
    runbook_url   = var.orchestrator_webhook_url
    notifications = local.detector_webhook_notifications
  }
}
