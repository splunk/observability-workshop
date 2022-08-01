### AWS Variables ###
variable "region" {
  default = {}
}
variable "vpc_id" {
  default = []
}
variable "vpc_cidr_block" {
  default = []
}
variable "itsi_public_subnet_id" {
  default = {}
}
variable "key_name" {
  default = []
}
variable "private_key_path"{
  default = []
}
variable "ami" {
  default = {}
}

### Splunk ITSI Variables ###
variable "splunk_itsi_ids" {
  default = []
}
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
variable "splunk_itsi_count" {
  default = {}
}
variable "workshop_name" {
  default = []
}
