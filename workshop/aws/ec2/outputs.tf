#output "ip_addresses" {
#  value = aws_instance.observability-instance.*.public_ip
#}

#output "instance_names" {
#  value = aws_instance.observability-instance[*].tags["Instance"]
#}

#output "public_subnet_ids" {
#  value = aws_subnet.o11y_ws_subnets.*.id
#}

#output "instance_password" {
#  value = random_string.password.result
#}
