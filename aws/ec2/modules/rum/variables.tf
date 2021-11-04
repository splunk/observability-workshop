### Workshop Variables ###
variable "wsversion" {}

variable "k9sversion" {}

variable "tfversion" {}


### SFx Variables ###
variable "access_token" {}
variable "rum_token" {}
variable "realm" {}
variable "key_name" {}
variable "private_key_path"{}
variable "instance_disk_aws" {}
variable "rum_prefix" {}

variable "ami" {
  default = []
}

variable "security_group_id" {
  default = []
}

variable "rum_master_type" {
  default = "t2.xlarge"
}

variable "rum_worker_type" {
  default = "t2.micro"
}

variable "rum_workers" {
  default = "3"
}
