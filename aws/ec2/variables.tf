variable "aws_instance_count" {
  description = "Instance Count (Usually 1)"
}

variable "aws_region" {
  description = "Provide the desired region (for example: us-west-2)"
}

variable "slug" {
  description = "Project name slug. Will be used to tag aws resources"
}

data "aws_ami" "latest-ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # This is the owner id of Canonical who owns the official aws ubuntu images

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-hirsute-21.04-amd64-server-*"]
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
