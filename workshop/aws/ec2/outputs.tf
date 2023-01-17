output "ip_addresses" {
  value = aws_instance.observability-instance.*.public_ip
}

output "instance_names" {
  value = aws_instance.observability-instance[*].tags["Instance"]
}
