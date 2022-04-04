resource "aws_security_group" "itsi_sg" {
  name          = "${var.environment}_Splunk ITSI SG"
  description   = "Allow ingress traffic to ITSI and Egress to Internet"
  vpc_id        = var.vpc_id

  ## Allow SSH - Required for Terraform & remote access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ## Allow access to ITSI UI
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ## Allow all egress traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }
}