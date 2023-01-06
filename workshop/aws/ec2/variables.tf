variable "splunk_presetup" {
  description = "Presetup the instance? (true/false)"
  type = bool
}
variable "aws_instance_count" {
  description = "Instance Count (Usually 1)"
  nullable = false
}

variable "aws_region" {
  description = "AWS Region (for example: us-west-2)"
  nullable = false
}

variable "slug" {
  description = "Project name slug that will be used to tag aws resources"
}

variable "splunk_access_token" {
  description = "Splunk Oberservability Cloud Access Token"
}

variable "splunk_rum_token" {
  description = "Splunk Oberservability Cloud RUM Token"
}

variable "splunk_realm" {
  description = "Splunk Oberservability Cloud Realm (us0, us1, us2, eu0, jp0, au0)"
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
