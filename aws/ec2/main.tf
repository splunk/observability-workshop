provider "aws" {
  profile = "default"
  region  = var.aws_region
}

module "rum" {
  source                  = "./modules/rum"
  count                   = var.rum_instances_enabled ? 1 : 0
  access_token            = var.access_token
  rum_token               = var.rum_token
  realm                   = var.realm
  key_name                = var.key_name
  private_key_path        = var.private_key_path
  ami                     = data.aws_ami.latest-ubuntu.id
  rum_master_type         = var.rum_master_type
  rum_worker_type         = var.rum_worker_type
  rum_workers             = var.rum_workers
  instance_disk_aws       = var.instance_disk_aws
  wsversion               = var.wsversion
  k9sversion              = var.k9sversion
  security_group_id       = [aws_security_group.instance.id]
}

output "RUM_Master" {
  value = var.rum_instances_enabled ? module.rum.*.rum_master_details : null
}

output "No_RUM" {
  value = var.rum_instances_enabled ? module.rum.*.no_rum_details : null
}

output "RUM_Online_Boutique_URL" {
  value = var.rum_instances_enabled ? module.rum.*.online_boutique_details : null
}

output "No_RUM_Online_Boutique_URL" {
  value = var.rum_instances_enabled ? module.rum.*.no_rum_online_boutique_details : null
}

output "RUM_Workers" {
  value = var.rum_instances_enabled ? module.rum.*.rum_worker_details : null
}
