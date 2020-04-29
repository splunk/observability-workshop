provider "aws" {
  profile = "default"
  region  = var.region
}

resource "aws_instance" "app-dev-instance" {
  count         = "${var.instance_count)"
  ami           = "${lookup(var.ami,var.aws_region)}"
  instance_type = "${var.instance_type}"
  user_data     = file("../cloud-init/k3s.yaml")
  tags = {
    Name = "app-dev-${count.index + 1}"
  }
}
