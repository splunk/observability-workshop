### Workshop Variables ###
variable "wsversion" {}
variable "k9sversion" {}

### AWS Variables ###
variable "key_name" {}
variable "private_key_path"{}
variable "instance_disk_aws" {}
variable "rum_master_type" {}
variable "rum_worker_type" {}
variable "rum_workers" {}
variable "ami" {
  default = []
}
variable "security_group_id" {
  default = []
}

### SFx Variables ###
variable "access_token" {}
variable "rum_token" {}
variable "realm" {}
