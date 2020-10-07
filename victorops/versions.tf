terraform {
  required_version = ">= 0.13"
  required_providers {
    signalfx = {
      source = "splunk-terraform/signalfx"
    }
  }
}