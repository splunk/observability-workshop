terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
    signalfx = {
      source = "splunk-terraform/signalfx"
    }
  }
  required_version = ">= 0.13"
}

