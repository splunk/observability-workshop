variable "cloud_init_print" {
  description = "Show rendered cloud_init output"
  type        = bool
  default     = false
}

variable "user_data_tpl" {
  description = "user data template filename in templates/"
  type        = string
  default     = "userdata.yaml"
}

variable "aws_instance_count" {
  description = "Instance Count (Usually 1)"
  nullable    = false
}

variable "subnet_count" {
  description = "Subnet Count (Usually 1 for small workshops, but can be 2 or 3 for larger one, but never 4 and be aware some regions only support 2 due to limited flavour availabiity)"
  nullable    = false
  default     = "2"
}

variable "public_subnet_ids" {
  default = []
}

variable "aws_region" {
  description = "AWS Region (for example: us-west-2)"
  type        = string
  nullable    = false
}

variable "slug" {
  description = "Short name/tag, e.g. acme. Used to derive project and hostnames, AWS tags and terraform workspace"
  type        = string
}

variable "splunk_access_token" {
  description = "Splunk Oberservability Cloud Access Token"
  type        = string
  nullable    = false
}

variable "splunk_api_token" {
  description = "Splunk Oberservability Cloud API Token"
  type        = string
  nullable    = false
}

variable "splunk_rum_token" {
  description = "Splunk Oberservability Cloud RUM Token"
  type        = string
  nullable    = false
}

variable "splunk_realm" {
  description = "Splunk Oberservability Cloud Realm (us0, us1, us2, eu0, jp0, au0)"
  type        = string
  nullable    = false
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

variable "splunk_presetup" {
  description = "Presetup the instance? (true/false)"
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
  default     = "5.66"
}

data "aws_ami" "latest-ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # This is the owner id of Canonical who owns the official aws ubuntu images

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

variable "pub_key" {
  description = "public key to provision on the instance"
  type        = string
  default     = ""
}

variable "aws_instance_type" {
  default = "t2.xlarge"
}

variable "instance_disk_aws" {
  default = "40"
}
