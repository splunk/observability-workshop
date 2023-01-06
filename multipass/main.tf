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
  type = string
}

variable "splunk_rum_token" {
  description = "Splunk Observability Cloud RUM Token"
  type = string
}

variable "splunk_realm" {
  description = "Splunk Observability Cloud Realm (us0, us1, us2, eu0, jp0, au0)"
  type = string
}

variable "splunk_presetup" {
  description = "Pre configure the instance? (true/false)"
  type = bool
  nullable = false
}

data "template_file" "user_data" {
  template = "${file("../workshop/aws/ec2/templates/userdata.yaml")}"
  vars = {
    access_token = "${var.splunk_access_token}"
    rum_token = "${var.splunk_rum_token}"
    realm = "${var.splunk_realm}"
    presetup = "${var.splunk_presetup}"
  }
}

resource "local_file" "user_data" {
  filename = "ubuntu-cloudinit.yml"
  content  = data.template_file.user_data.rendered
}

resource "random_string" "hostname" {
  length = 6
  lower  = true
  upper  = false
  special = false
  numeric = false
}

resource "multipass_instance" "ubuntu" {
  name = random_string.hostname.result
  memory = "8096MiB"
  disk = "32GiB"
  cpus = 4
  image  = "jammy"
  cloudinit_file = local_file.user_data.filename
}
