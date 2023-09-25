terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      #version = "3.74.1"
    }

    signalfx = {
      source = "splunk-terraform/signalfx"
      version = "9.0.0"
    }

    tls = {
      source  = "hashicorp/tls"
      version = "4.0.4"
    }

    local = {
      source  = "hashicorp/local"
      version = "2.4.0"
    }
  }
  required_version = ">= 1.3.7"
}
