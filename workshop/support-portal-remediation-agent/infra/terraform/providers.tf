terraform {
  required_version = ">= 1.8.0"

  required_providers {
    signalfx = {
      source = "splunk-terraform/signalfx"
    }
  }
}

provider "signalfx" {
  auth_token = var.splunk_access_token
  api_url    = "https://api.${var.splunk_realm}.signalfx.com"
}
