provider "aws" {
  profile = "default"
  region  = var.aws_region
}

resource "aws_instance" "observability-instance" {
  count                  = var.aws_instance_count
  ami                    = data.aws_ami.latest-ubuntu.id
  instance_type          = var.aws_instance_type
  vpc_security_group_ids = [aws_security_group.instance.id]
  user_data              = file("../../cloud-init/k3s.yaml")

  root_block_device {
    volume_size = var.instance_disk_aws
  }

  tags = {
    Name = "observability-${count.index + 1}"
  }
}

module "rum" {
  source                  = "./modules/rum"
  count                   = var.rum_instances_enabled ? 1 : 0
  access_token            = var.access_token
  rum_token               = var.rum_token
  realm                   = var.realm
  key_name                = var.key_name
  private_key_path        = var.private_key_path
  rum_prefix              = var.rum_prefix
  ami                     = data.aws_ami.latest-ubuntu.id
  instance_disk_aws       = var.instance_disk_aws
  wsversion               = var.wsversion
  k9sversion              = var.k9sversion
  tfversion               = var.tfversion
  security_group_id       = [aws_security_group.instance.id]
}

output "RUM_Master" {
  value = var.rum_instances_enabled ? module.rum.*.rum_master_details : null
}

output "Online_Boutique_URL" {
  value = var.rum_instances_enabled ? module.rum.*.online_boutique_details : null
}

output "RUM_Workers" {
  value = var.rum_instances_enabled ? module.rum.*.rum_worker_details : null
}

output "ip" {
  value = aws_instance.observability-instance.*.public_ip
}

# resource "aws_security_group" "instance" {
#   name = "Observability-Workshop-SG"

#   ingress {
#     from_port   = 22
#     to_port     = 22
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#   ingress {
#     from_port   = 81
#     to_port     = 81
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   ingress {
#     from_port   = 82
#     to_port     = 82
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   ingress {
#     from_port   = 8080
#     to_port     = 8080
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   ingress {
#     from_port   = 8081
#     to_port     = 8081
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   ingress {
#     from_port   = 8082
#     to_port     = 8082
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   ingress {
#     from_port   = 55679
#     to_port     = 55679
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   ingress {
#     from_port   = 6501
#     to_port     = 6501
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }

