variable "cloud_init_print" {
  description = "Show rendered cloud_init output"
  type        = bool
  default     = false
}

variable "splunk_presetup" {
  description = "Presetup the instance? (true/false)"
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

variable "wsversion" {
  description = "Workshop version"
  type        = string
  default     = "5.0"
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
  nullable    = false
}

variable "slug" {
  description = "Short name/tag, e.g. acme. Used to derive project and hostnames, AWS tags and terraform workspace"
}

variable "splunk_access_token" {
  description = "Splunk Oberservability Cloud Access Token"
  nullable    = false
}

variable "splunk_rum_token" {
  description = "Splunk Oberservability Cloud RUM Token"
  nullable    = false
}

variable "splunk_realm" {
  description = "Splunk Oberservability Cloud Realm (us0, us1, us2, eu0, jp0, au0)"
  nullable    = false
}

variable "splunk_hec_token" {
  description = "Splunk Cloud HEC Token"
  nullable    = false
}

variable "splunk_hec_url" {
  description = "Splunk Cloud HEC URL"
  nullable    = false
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
  nullable    = false
}

variable "aws_instance_type" {
  default = "t2.xlarge"
}

variable "instance_disk_aws" {
  default = "40"
}
