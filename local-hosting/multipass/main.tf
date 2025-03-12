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
  nullable    = false
}

variable "splunk_api_token" {
  description = "Splunk Observability Cloud API Token"
  type        = string
  nullable    = false
}

variable "splunk_rum_token" {
  description = "Splunk Observability Cloud RUM Token"
  type        = string
  nullable    = false
}

variable "splunk_realm" {
  description = "Splunk Observability Cloud Realm (us0, us1, us2, eu0, jp0, au0)"
  type        = string
  default     = ""
}

variable "splunk_hec_token" {
  description = "Splunk Cloud HEC Token"
  type        = string
  nullable    = false
}

variable "splunk_hec_url" {
  description = "Splunk Cloud HEC URL"
  type        = string
  nullable    = false
}

variable "splunk_index" {
  description = "Splunk Cloud Index"
  type        = string
  default     = "splunk4rookies-workshop"
}

variable "splunk_presetup" {
  description = "Pre configure the instance? (true/false)"
  type        = bool
  default     = false
}

variable "otel_demo" {
  description = "Spin up the OpenTelemetry Astronomy Shop Demo? (true/false)"
  type        = bool
  default     = false
}

variable "splunk_diab" {
  description = "Enabled Demo-in-a-box environment? (true/false)"
  type        = bool
  default     = false
}

variable "tagging_workshop" {
  description = "Spin up the Tagging Workshop application? (true/false)"
  type        = bool
  default     = false
}

variable "wsversion" {
  description = "Workshop version"
  type        = string
  default     = "5.85"
}

variable "user_data_tpl" {
  description = "user data template filename in templates/"
  type        = string
  default     = "userdata.yaml"
}

variable "architecture" {
  description = "Architecture of the instance (amd64 or arm64)"
  type        = string
  default     = "amd64"
}

variable "instance_password" {
  default = "Splunk123!"
}

variable "pub_key" {
  description = "public key to provision on the instance"
  type        = string
  default     = ""
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
    api_token         = var.splunk_api_token
    realm             = var.splunk_realm
    hec_token         = var.splunk_hec_token
    hec_url           = var.splunk_hec_url
    index             = var.splunk_index
    presetup          = var.splunk_presetup
    otel_demo         = var.otel_demo
    tagging_workshop  = var.tagging_workshop
    diab              = var.splunk_diab
    instance_name     = "${random_string.hostname.result}"
    wsversion         = var.wsversion
    architecture      = var.architecture
    instance_password = var.instance_password
    pub_key           = var.pub_key
  }
}

resource "local_file" "user_data" {
  filename = "ubuntu-cloudinit.yml"
  content  = templatefile("templates/${var.user_data_tpl}", merge(local.template_vars))
}

data "multipass_instance" "ubuntu" {
  name = random_string.hostname.result
  depends_on = [
    multipass_instance.ubuntu
  ]
}

resource "multipass_instance" "ubuntu" {
  name           = random_string.hostname.result
  cpus           = 4
  memory         = "8G"
  disk           = "32G"
  image          = "jammy"
  cloudinit_file = local_file.user_data.filename

  lifecycle {
    precondition {
      # if splunk_presetup=true, tokens and realm cannot be empty
      condition     = var.splunk_presetup ? try(var.splunk_access_token, "") != "" && try(var.splunk_realm, "") != "" && try(var.splunk_rum_token, "") != "" : true
      error_message = "When requesting a pre-setup instance, splunk_realm, splunk_access_token and splunk_rum_token are required and cannot be null/empty"
    }
    precondition {
      # if access_token and realm cannot be empty.
      condition     = var.splunk_access_token != "" && var.splunk_realm != ""
      error_message = "splunk_realm and splunk_access_token are required and cannot be null/empty."
    }
  }
}
