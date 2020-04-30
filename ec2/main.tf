provider "aws" {
  profile = "default"
  region  = var.aws_region
}

resource "aws_security_group" "instance" {
  name = "App-Dev-Workshop-SG"

  ingress {
    from_port   = 22
    to_port     = 22
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

resource "aws_instance" "app-dev-instance" {
  count         = var.aws_instance_count
  ami           = data.aws_ami.latest-ubuntu.id
  instance_type =  var.instance_type  
  vpc_security_group_ids  = [aws_security_group.instance.id]
  user_data     = file("../cloud-init/k3s.yaml")
  
  root_block_device {
    volume_size = "15"
  }

  tags = {
    Name = "app-dev-${count.index + 1}"
  }

}
 
