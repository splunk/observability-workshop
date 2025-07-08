variable "o11y_access_token" {
  description = "Splunk Observability Cloud :: Access Token"
  type        = string
}

variable "o11y_realm" {
  description = "Splunk Observability Cloud :: Realm"
  type        = string
}

variable "otel_lambda_layer" {
  description = "Splunk OpenTelemetry Lambda Layer"
  type        = list(string)
}

variable "prefix" {
  description = "Unique string for customiing resource names"
  type        = string
}
