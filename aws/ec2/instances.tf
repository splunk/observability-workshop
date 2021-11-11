resource "random_string" "o11y_instance_password" {
  count   = var.aws_instance_count
  length  = 12
  special = false #not using special characters to allow double click copy and paste from g-sheet
}

resource "random_string" "o11y_instance_prefix" {
  count   = var.aws_instance_count
  length  = 4
  lower   = true
  upper   = false
  number  = false
  special = false
}

resource "aws_instance" "observability-instance" {
  count                  = var.aws_instance_count
  ami                    = data.aws_ami.latest-ubuntu.id
  instance_type          = var.aws_instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.instance.id]

  root_block_device {
    volume_size = var.instance_disk_aws
  }

  tags = {
    Name  = "${random_string.o11y_instance_prefix[count.index].result}"
    Role  = "O11Y Instance"
  }

  provisioner "file" {
    source      = "${path.module}/motd"
    destination = "/tmp/motd"
  }

  provisioner "file" {
    source      = "${path.module}/profile"
    destination = "~/.profile"
  }

  provisioner "file" {
    source      = "${path.module}/shellinabox"
    destination = "~/.shellinabox"
  }

  provisioner "remote-exec" {
    inline = [
      ## Set Hostname
      "sudo sed -i 's/127.0.0.1.*/127.0.0.1 ${self.tags.Name}.local ${self.tags.Name} localhost/' /etc/hosts",
      "sudo hostnamectl set-hostname ${self.tags.Name}",

      # Download and Install the Latest Updates for the OS - NOTE the two entries of apt-get update are there by design
      "sudo apt-get update",
      "sudo apt-get update",
      "sudo apt-get upgrade -y",
      "sudo apt-get install -y unzip shellinabox lynx w3m",
    
      # Install K3s
      # "curl -sfL https://get.k3s.io | sh -",
      "curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE=\"644\" sh -s -",

      #Install Helm
      "curl -s https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash",

      # Install K9s (Kubernetes UI)
      "curl -s -OL https://github.com/derailed/k9s/releases/download/${var.k9sversion}/k9s_Linux_x86_64.tar.gz",
      "tar xfz k9s_Linux_x86_64.tar.gz",
      "sudo mv k9s /usr/local/bin/",

      # Download Workshop
      "export WSARCHIVE=$([ ${var.wsversion} = \"master\" ] && echo \"master\" || echo v${var.wsversion})",
      "curl -s -OL https://github.com/signalfx/observability-workshop/archive/$WSARCHIVE.zip",
      "unzip -qq $WSARCHIVE.zip -d /home/ubuntu/",
      "mv /home/ubuntu/observability-workshop-${var.wsversion} /home/ubuntu/workshop",

      # Install Terraform
      "curl -s -OL https://releases.hashicorp.com/terraform/${var.tfversion}/terraform_${var.tfversion}_linux_amd64.zip",
      "unzip -qq terraform_${var.tfversion}_linux_amd64.zip",
      "sudo mv terraform /usr/local/bin/",

      # fix shellinabox port and ssl then restart
      "mv /tmp/shellinabox /etc/default/shellinabox",
      "sudo chown root:root /etc/default/shellinabox",
      "sudo service shellinabox restart",

      # Create kube config and set correct permissions on ubuntu user home directory
      "mkdir /home/ubuntu/.kube && sudo kubectl config view --raw > /home/ubuntu/.kube/config",
      "chmod 400 /home/ubuntu/.kube/config",
      "chown -R ubuntu:ubuntu /home/ubuntu",

      # fix shellinabox port and ssl then restart
      "mv /tmp/shellinabox /etc/default/shellinabox",
      "sudo chown root:root /etc/default/shellinabox",
      "sudo service shellinabox restart",
     
      ## Move and set permissions on message of the day
      "sudo mv /tmp/motd /etc/motd",
      "sudo chmod -x /etc/update-motd.d/*",

      ## Set Password for Ubuntu
      "echo ubuntu:${random_string.o11y_instance_password[count.index].result} | sudo chpasswd",
    ]
  }

  connection {
    host = self.public_ip
    type = "ssh"
    user = "ubuntu"
    private_key = file(var.private_key_path)
    agent = "true"
  }
}

output "Instance_Details" {
  value =  formatlist(
    "%s, %s, %s", 
    aws_instance.observability-instance.*.tags.Name,
    aws_instance.observability-instance.*.public_ip,
    random_string.o11y_instance_password.*.result,
  )
}
