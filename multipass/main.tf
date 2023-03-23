provider "multipass" {}

terraform {
  required_providers {
    multipass = {
      source  = "larstobi/multipass"
      version = "~> 1.4.1"
    }
  }
}

variable "splunk_access_token" {
  description = "Splunk Observability Cloud Access Token"
  type        = string
  default     = ""
}

variable "splunk_rum_token" {
  description = "Splunk Observability Cloud RUM Token"
  type        = string
  default     = ""
}

variable "splunk_realm" {
  description = "Splunk Observability Cloud Realm (us0, us1, us2, eu0, jp0, au0)"
  type        = string
  default     = ""
}

variable "splunk_presetup" {
  description = "Pre configure the instance? (true/false)"
  type        = bool
  default     = false
}

variable "splunk_jdk" {
  description = "Enabled Java Development environment? (true/false)"
  type        = bool
  default     = false
}

variable "otel_demo" {
  description = "Spin up the OpenTelemetry Astronomy Shop Demo? (true/false)"
  type        = bool
  default     = false
}

variable "instance_password" {
  default = ""
}

resource "random_string" "hostname" {
  length  = 4
  lower   = true
  upper   = false
  special = false
  numeric = false
}

locals {
  template_vars = {
    access_token      = var.splunk_access_token
    rum_token         = var.splunk_rum_token
    realm             = var.splunk_realm
    presetup          = var.splunk_presetup
    jdk               = var.splunk_jdk
    otel_demo         = var.otel_demo
    instance_name     = "${random_string.hostname.result}"
    instance_password = var.instance_password
  }
}

data "template_file" "user_data" {
  template = templatefile("../workshop/aws/ec2/templates/userdata.yaml", merge(local.template_vars))
}

resource "local_file" "user_data" {
  filename = "ubuntu-cloudinit.yml"
  content  = data.template_file.user_data.rendered
}

resource "multipass_instance" "ubuntu" {
  name           = random_string.hostname.result
  memory         = "8G"
  disk           = "32G"
  cpus           = 4
  image          = "jammy"
  cloudinit_file = local_file.user_data.filename

  lifecycle {
    precondition {
      # if splunk_presetup=true, tokens and realm cannot be empty
      condition     = var.splunk_presetup ? try(var.splunk_access_token, "") != "" && try(var.splunk_realm, "") != "" && try(var.splunk_rum_token, "") != "" : true
      error_message = "When requesting a pre-setup instance, splunk_realm, splunk_access_token and splunk_rum_token are required and cannot be null/empty"
    }
  }
}
