## Enable/Disable Modules - Values are set in quantity.auto.tfvars ###
variable "itsi_o11y_cp_enabled" {
  default = []
}

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
variable "vpc_id" {
  default = []
}
variable "vpc_name" {
  default = []
}
variable "vpc_cidr_block" {
  default = []
}
variable "public_subnet_ids" {
  default = {}
}
variable "private_subnet_ids" {
  default = {}
}
variable "subnet_count" {
  default = {}
}
variable "key_name" {
  default = []
}
variable "private_key_path" {
  default = []
}
variable "instance_type" {
  default = []
}
variable "collector_instance_type" {
  default = []
}

## Ubuntu AMI ##
data "aws_ami" "latest-ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # This is the owner id of Canonical who owns the official aws ubuntu images

  filter {
    name = "name"
    # values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

### Instance Count Variables ###
variable "splunk_itsi_count" {
  default = {}
}
variable "splunk_itsi_ids" {
  default = []
}
# variable "xxx _count" {
#   default = {}
# }
# variable "xxx _ids" {
#   type = list(string)
#   default = []
# }

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

### SignalFX Variables ###
variable "access_token" {
  default = []
}
variable "api_url" {
  default = []
}
variable "realm" {
  default = []
}
variable "environment" {
  default = []
}

### Splunk ITSI Variables ###
variable "splunk_itsi_filename" {
  default = {}
}
variable "splunk_itsi_version" {
  default = {}
}
variable "splunk_itsi_inst_type" {
  default = {}
}
variable "splunk_itsi_files_local_path" {
  default = {}
}
variable "splunk_itsi_license_filename" {
  default = {}
}
variable "splunk_app_for_content_packs_filename" {
  default = {}
}
variable "splunk_it_service_intelligence_filename" {
  default = {}
}
variable "splunk_synthetic_monitoring_add_on_filename" {
  default = {}
}
variable "splunk_infrastructure_monitoring_add_on_filename" {
  default = {}
}