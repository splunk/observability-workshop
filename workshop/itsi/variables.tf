### AWS Variables ###
variable "profile" {
  default = []
}
variable "aws_access_key_id" {
  default = []
}
variable "aws_secret_access_key" {
  default = []
}
variable "vpc_cidr_block" {
  default = []
}
variable "key_name" {
  default = []
}
variable "private_key_path" {
  default = []
}

## Ubuntu AMI ##
data "aws_ami" "latest-ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # This is the owner id of Canonical who owns the official aws ubuntu images

  filter {
    name = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

variable "region" {
  description = "Select region (1:eu-west-1, 2:eu-west-3, 3:eu-central-1, 4:us-east-1, 5:us-east-2, 6:us-west-1, 7:us-west-2, 8:ap-southeast-1, 9:ap-southeast-2, 10:sa-east-1 )"
}

variable "aws_region" {
  description = "Provide the desired region"
  default = {
    "1"  = "eu-west-1"
    "2"  = "eu-west-3"
    "3"  = "eu-central-1"
    "4"  = "us-east-1"
    "5"  = "us-east-2"
    "6"  = "us-west-1"
    "7"  = "us-west-2"
    "8"  = "ap-southeast-1"
    "9"  = "ap-southeast-2"
    "10" = "sa-east-1"
  }
}


### Splunk ITSI Variables ###

variable "splunk_itsi_filename" {
  default = "splunk-8.2.3-cd0848707637-linux-2.6-amd64.deb"
}
variable "splunk_itsi_version" {
  default = "8.2.3"
}
variable "splunk_itsi_inst_type" {
  default = "t3.xlarge"
}
variable "splunk_app_for_content_packs_filename" {
  default = "splunk-app-for-content-packs_140.spl"
}
variable "splunk_it_service_intelligence_filename" {
  default = "splunk-it-service-intelligence_4113.spl"
}
variable "splunk_synthetic_monitoring_add_on_filename" {
  default = "splunk-synthetic-monitoring-add-on_107.tgz"
}
variable "splunk_infrastructure_monitoring_add_on_filename" {
  default = "splunk-infrastructure-monitoring-add-on_121.tgz"
}

variable "splunk_itsi_count" {
  default = []
}
variable "splunk_itsi_files_local_path" {
  default = {}
}
variable "splunk_itsi_license_filename" {
  default = {}
}
variable "workshop_name" {
  default = {}
}
