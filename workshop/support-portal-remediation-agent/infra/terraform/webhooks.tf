locals {
  webhook_notifications_enabled = var.enable_webhook_integration && var.public_orchestrator_webhook_url != ""
  detector_webhook_notifications = local.webhook_notifications_enabled ? [
    "Webhook,${signalfx_webhook_integration.orchestrator[0].id},,"
  ] : var.existing_webhook_credential_id != "" ? [
    "Webhook,${var.existing_webhook_credential_id},,"
  ] : []
}

resource "signalfx_webhook_integration" "orchestrator" {
  count   = local.webhook_notifications_enabled ? 1 : 0
  enabled = true
  name    = "IBOBS Orchestrator Webhook"
  method  = "POST"
  url     = var.public_orchestrator_webhook_url

  dynamic "headers" {
    for_each = var.splunk_webhook_shared_secret != "" ? [1] : []
    content {
      header_key   = "x-ibobs-webhook-secret"
      header_value = var.splunk_webhook_shared_secret
    }
  }
}
