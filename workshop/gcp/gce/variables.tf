variable "gcp_project" {
  description = "Provide the GCP project"
}

variable "gcp_instance_count" {
  description = "Instance Count (usually 1)"
}

variable "gcp_zone" {
  description = "Provide the desired zone (for example: europe-west3-a)"
}

variable "gcp_instance_type" {
  description = "Select instance type required"
  default     = "n2-highcpu-4"
}

