output "cloud-init" {
  value = "\n${data.template_cloudinit_config.config.rendered}"
}

output "ip-addresses" {
  value = aws_instance.observability-instance.*.public_ip
}