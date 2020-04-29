provider "aws" {
  profile = "default"
  region  = var.aws_region
}

resource "aws_instance" "app-dev-instance" {
  count         = var.aws_instance_count
  ami           = lookup(var.ami,var.aws_region)
  instance_type = var.instance_type
  key_name      = var.key_name
  user_data     = file("../cloud-init/k3s.yaml")
  
  root_block_device {
    volume_size           = "15"
  }

  tags = {
    Name = "app-dev-${count.index + 1}"
  }

}
