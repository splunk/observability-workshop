variable "aws_instance_count" {
  description = "Instance Count"
}

variable "aws_region" {
  description = "Provide the desired region (for example: us-west-2)"
}

data "aws_ami" "latest-ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # This is the owner id of Canonical who owns the official aws ubuntu images

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
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
  default = "16"
}


## RUM Variables
variable "rum_instances_enabled" {
  description = "Deploy RUM Instances? 0=No, 1=Yes"
}
variable "rum_prefix" {
  description = "Enter a prefix for the RUM Master to ensure it is unique in the event there are multiple workshops running"
}
variable "access_token" {}
variable "rum_token" {}
variable "realm" {}
variable "key_name" {}
variable "private_key_path"{}

### Workshop Variables ###
variable "wsversion" {
  default = "master" # only set to master for testing should normally be a specific version such as 2.42
}

variable "k9sversion" {
  default = "v0.24.14"
}

variable "tfversion" {
  default = "1.0.3"
}