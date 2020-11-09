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

