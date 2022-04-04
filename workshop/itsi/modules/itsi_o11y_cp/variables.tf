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
variable "public_subnet_ids" {
  default = {}
}
variable "key_name" {
  default = []
}
variable "private_key_path"{
  default = []
}
variable "instance_type" {
  default = []
}
variable "collector_instance_type" {
  default = []
}
variable "ami" {
  default = {}
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
variable "otelcol_version" {
  default = []
}
variable "ballast" {
  default = []
}
variable "environment" {
  default = []
}

### Splunk ITSI Variables ###
variable "splunk_itsi_count" {
  default = {}
}
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