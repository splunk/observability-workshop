provider "aws" {
  profile = "default"
}

resource "aws_instance" "app-dev-instance" {
  ami           = "ami-085925f297f89fce1"
  instance_type = "t2.micro"
  key_name      = var.key_name
  user_data     = "${file("../cloud-init/k3s.yaml")}"
}
