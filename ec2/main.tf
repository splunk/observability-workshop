provider "aws" {
  profile = "default"
  region  = var.region
}

resource "aws_instance" "app-dev-instance" {
  count         = var.instance_count
  ami           = "ami-085925f297f89fce1"
  instance_type = "t2.micro"
  user_data     = file("../cloud-init/k3s.yaml")
  tags = {
    Name = "app-dev-${count.index + 1}"
  }
}

