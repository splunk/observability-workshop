terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
    signalfx = {
      source = "splunk-terraform/signalfx"
    }
  }
  required_version = ">= 0.13"
}
