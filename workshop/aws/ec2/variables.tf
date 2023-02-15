variable "cloud_init_print" {
  description = "Show rendered cloud_init output"
  type  = bool
  default = false
}

variable "splunk_presetup" {
  description = "Presetup the instance? (true/false)"
  type = bool
  default = false
}

variable "splunk_jdk" {
  description = "Enabled Java Development environment? (true/false)"
  type = bool
  default = false
}

variable "aws_instance_count" {
  description = "Instance Count (Usually 1)"
  nullable = false
}

variable "subnet_count" {
  description = "Subnet Count (Usually 1 for small workshops, but can be 2 or 3 for larger one, but never 4 and be aware some regions only support 2 due to limited flavor availabiity)"
  nullable = false
  default = "2"
}

variable "public_subnet_ids" {
  default = []
}

variable "aws_region" {
  description = "AWS Region (for example: us-west-2)"
  nullable = false
}

variable "slug" {
  description = "Short name/tag, e.g. acme. Used to derive project and host names, aws tags and terraform workspace."
}

variable "splunk_access_token" {
  description = "Splunk Oberservability Cloud Access Token"
  default     = ""
}

variable "splunk_rum_token" {
  description = "Splunk Oberservability Cloud RUM Token"
  default     = ""
}

variable "splunk_realm" {
  description = "Splunk Oberservability Cloud Realm (us0, us1, us2, eu0, jp0, au0)"
  default     = ""
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

variable "aws_instance_type" {
  default = "t2.xlarge"
}

variable "instance_disk_aws" {
  default = "40"
}
