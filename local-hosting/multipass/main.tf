provider "multipass" {}

terraform {
  required_providers {
    multipass = {
      source  = "larstobi/multipass"
      version = "~> 1.4.1"
    }
    http = {
      source  = "hashicorp/http"
      version = "~> 3.4.0"
    }
  }
}

variable "swipe_id" {
  description = "Splunk Swipe ID"
  type        = string
  default     = ""
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
  default     = "5.94"
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

# Fetch tokens from Splunk Swipe API
data "http" "swipe_tokens" {
  url = "https://swipe.splunk.show/api?id=${var.swipe_id}"

  request_headers = {
    "Content-Type" = "application/json"
  }
}

locals {
  # Process API response
  swipe_data = try(jsondecode(data.http.swipe_tokens.response_body), {})
  
  # Extract values from API response
  access_token = try(local.swipe_data.INGEST, "")
  api_token    = try(local.swipe_data.API, "")
  rum_token    = try(local.swipe_data.RUM, "")
  realm        = try(local.swipe_data.REALM, "")
  hec_token    = try(local.swipe_data.HEC_TOKEN, "")
  hec_url      = try(local.swipe_data.HEC_URL, "")
  
  template_vars = {
    access_token      = local.access_token
    rum_token         = local.rum_token
    api_token         = local.api_token
    realm             = local.realm
    hec_token         = local.hec_token
    hec_url           = local.hec_url
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
      condition = try(local.swipe_data.message, "") != "Workshop ID not found"
      error_message = "SWiPE ID not found. Please check the ID and try again."
    }
    # precondition {
    #   # if splunk_presetup=true, tokens and realm cannot be empty
    #   condition     = var.splunk_presetup ? try(local.access_token, "") != "" && try(local.realm, "") != "" && try(local.rum_token, "") != "" : true
    #   error_message = "When requesting a pre-setup instance, REALM, ACCESS_TOKEN and RUM_TOKEN are required and cannot be null/empty"
    # }
    # precondition {
    #   # if access_token and realm cannot be empty.
    #   condition     = local.access_token != "" && local.realm != ""
    #   error_message = "REALM and ACCESS_TOKEN are required and cannot be null/empty."
    # }
  }
}
