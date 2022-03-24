variable "gcp_project" {
  description = "Provide the GCP project"
}

variable "gcp_region" {
  description = "Provide the desired region (for example: us-west-2)"
}

variable "gke_num_nodes" {
  default     = 3
  description = "number of gke nodes"
}

variable "gke_username" {
  default     = "admin"
  description = "GKE username"
}

