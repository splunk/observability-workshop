resource "aws_security_group" "mysql" {
  name        = "Mysql"
  description = "MySQL inbound traffic"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    self = true
    security_groups = [aws_security_group.web.id]
  }
}
