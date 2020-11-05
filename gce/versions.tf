terraform {
  required_providers {
    signalfx = {
      source = "splunk-terraform/signalfx"
    }
    google = {
      source = "hashicorp/google"
    }
    random = {
      source = "hashicorp/random"
    }
  }
  required_version = ">= 0.13"
}
