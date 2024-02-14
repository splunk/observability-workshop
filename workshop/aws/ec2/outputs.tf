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

output "login_details" {
  value = formatlist(
    "%s, ssh -p 2222 splunk@%s, %s",
    aws_instance.observability-instance[*].tags["Instance"],
    aws_instance.observability-instance.*.public_ip,
    local.template_vars.instance_password
  )
}

resource "local_file" "ssh_details" {
  filename        = "ssh-${var.slug}.csv"
  file_permission = "600"
  content = templatefile("${path.module}/templates/ssh_csv.tpl",
    {
      ips : aws_instance.observability-instance[*].public_ip
      names : aws_instance.observability-instance[*].tags["Instance"]
      password: local.template_vars.instance_password
  })
}