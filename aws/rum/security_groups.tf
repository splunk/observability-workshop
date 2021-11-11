
resource "aws_security_group" "rum" {
  name = "O11Y-Workshop-RUM-SG"

  ## Allow all traffic between group members
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    self = true
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 81
    to_port     = 81
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
