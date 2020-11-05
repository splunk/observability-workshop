variable "gcp_project" {
  description = "Provide the GCP project"
}

variable "gcp_instance_count" {
  description = "Instance Count (usually 1)"
}

variable "gcp_region" {
  description = "Provide the desired region (for example: us-west-2)"
}

variable "gcp_instance_type" {
  description = "Select instance type required"
  default     = "f1-micro"
}

variable "signalfx_api_access_token" {
  description = "SignalFx User API access token."
}

variable "signalfx_realm" {
  description = "SignalFx realm."
}

variable "signalfx_gcp_integration_name" {
  description = "Name of the AWS integration that shows up in SignalFx integrations UI."
}

variable "signalfx_gcp_integration_enabled" {
  description = "Fake boolean to control rollout of AWS integration. Set to 0 to disable"
  default     = 1
}
