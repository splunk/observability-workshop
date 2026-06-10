variable "splunk_access_token" {
  type      = string
  sensitive = true
}

variable "splunk_realm" {
  type    = string
  default = "us1"
}

variable "deployment_environment" {
  type    = string
  default = "demo"
}

variable "instance" {
  type    = string
  default = "student-001"
}

variable "orchestrator_webhook_url" {
  type = string
}

variable "public_orchestrator_webhook_url" {
  type    = string
  default = ""
}

variable "enable_webhook_integration" {
  type    = bool
  default = false
}

variable "splunk_webhook_shared_secret" {
  type      = string
  sensitive = true
  default   = ""
}

variable "existing_webhook_credential_id" {
  type    = string
  default = ""
}

variable "filesystem_utilization_threshold" {
  type    = number
  default = 85
}

variable "cache_mountpoint" {
  type    = string
  default = "/var/cache/claims-knowledge"
}

variable "evidence_metric_source" {
  type    = string
  default = "claims-knowledge-evidence"
}

variable "cache_utilization_metric" {
  type    = string
  default = "claims_knowledge.cache.utilization"
}

variable "claim_status_latency_metric" {
  type    = string
  default = "claims_knowledge.claim_status.latency_ms"
}

variable "apm_latency_threshold_ns" {
  type    = number
  default = 1800000000
}

variable "apm_error_threshold" {
  type    = number
  default = 0.05
}
