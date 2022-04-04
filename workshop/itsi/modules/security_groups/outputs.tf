output "sg_allow_all_id" {
  value       = aws_security_group.allow_all.id
  description = "ID of the Allow All Security Group"
}

output "sg_allow_egress_id" {
  value       = aws_security_group.allow_egress.id
  description = "ID of the Allow Egress Security Group"
}

output "sg_web_id" {
  value       = aws_security_group.web.id
  description = "ID of the Allow Web Security Group"
}

output "sg_allow_ssh_id" {
  value       = aws_security_group.allow_ssh.id
  description = "ID of the Allow SSH Security Group"
}

output "sg_mysql_id" {
  value       = aws_security_group.mysql.id
  description = "ID of the Allow mysql Security Group"
}

output "sg_collectors_id" {
  value       = aws_security_group.collectors.id
  description = "ID of the Allow Collectors Security Group"
}
