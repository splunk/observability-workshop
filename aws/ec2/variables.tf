### Workshop Variables ###
variable "wsversion" {
  default = "2.42" # only set to master for testing should normally be a specific version such as 2.42
}
variable "k9sversion" {
  default = "v0.24.14"
}
variable "tfversion" {
  default = "1.0.3"
}

variable "aws_instance_count" {
  description = "Instance Count (Usually 1)"
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
