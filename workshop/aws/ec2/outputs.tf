output "ip_addresses" {
  value = aws_instance.observability-instance[*].public_ip
}

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
    aws_instance.observability-instance[*].tags["instance"],
    aws_instance.observability-instance[*].public_ip,
    local.template_vars.instance_password
  )
}

resource "local_file" "ssh_details" {
  filename        = "ssh-${var.slug}.csv"
  file_permission = "600"
  content = templatefile("${path.module}/templates/ssh_csv.tpl",
    {
      ips : aws_instance.observability-instance[*].public_ip
      names : aws_instance.observability-instance[*].tags["instance"]
      password: local.template_vars.instance_password
  })
}
output "ssh_priv_key" {
  value = tls_private_key.pk.private_key_openssh
  sensitive = true
}

output "ssh_args" {
  value = format("%s",
    join(" ", [
      format("-o IdentityFile=%s", local.ssh_priv_key),
      "-F /dev/null",
      "-o IdentitiesOnly=yes",
      "-o PasswordAuthentication=no",
      "-o PubkeyAuthentication=yes",
      "-o ChallengeResponseAuthentication=no",
      "-o CanonicalizeHostname=yes",
      "-o StrictHostKeyChecking=accept-new",
      "-o ForwardAgent=no",
      "-l ubuntu"
    ]))
}
