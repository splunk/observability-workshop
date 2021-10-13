output "ip" {
  value = aws_instance.observability-instance.*.public_ip
}