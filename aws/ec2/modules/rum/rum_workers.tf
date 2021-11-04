resource "random_string" "rum_worker_password" {
  # count   = lookup(var.rum_instances_workers, var.rum_instances)
  count   = var.rum_workers
  length  = 12
  special = false #not using special characters to allow double click copy and paste from g-sheet
}

resource "aws_instance" "rum_worker" {
  # count                  = lookup(var.rum_instances_workers, var.rum_instances)
  count                  = var.rum_workers
  # ami                    = data.aws_ami.latest-ubuntu.id
  ami                    = var.ami
  instance_type          = var.rum_worker_type
  key_name               = var.key_name
  vpc_security_group_ids = var.security_group_id

  root_block_device {
    volume_size = var.instance_disk_aws
  }

  tags = {
    Name = "${format("rum-worker-%01d", count.index + 1)}"
    Role  = "Workshop"
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

  provisioner "file" {
    source      = "${path.module}/splunk_worker.service"
    destination = "/tmp/splunk_worker.service"
  }

  provisioner "file" {
    source      = "${path.module}/go.sh"
    destination = "/tmp/go.sh"
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
      "sudo apt-get install -y unzip shellinabox",

      # Download Workshop
      "export WSARCHIVE=$([ ${var.wsversion} = \"master\" ] && echo \"master\" || echo v${var.wsversion})",
      "curl -s -OL https://github.com/signalfx/observability-workshop/archive/$WSARCHIVE.zip",
      "unzip -qq $WSARCHIVE.zip -d /home/ubuntu/",
      "mv /home/ubuntu/observability-workshop-${var.wsversion} /home/ubuntu/workshop",

      # fix shellinabox port and ssl then restart
      "mv /tmp/shellinabox /etc/default/shellinabox",
      "sudo chown root:root /etc/default/shellinabox",
      "sudo service shellinabox restart",

      #Setup Puppeteer for getnerating load
      "sudo apt install -y libgbm-dev gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget",
      "curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -",
      "sudo apt-get install -y nodejs",
      "npm install -s puppeteer",

      ## Update touchwesite.js and go.sh
      "sed -i -e 's/localhost/${aws_instance.rum_master.public_ip}/g' /home/ubuntu/workshop/apm/microservices-demo/k8s/touchwebsite.js",
      "sudo mv /tmp/go.sh /home/ubuntu/workshop/apm/microservices-demo/k8s/go.sh",
      "sudo chmod +x /home/ubuntu/workshop/apm/microservices-demo/k8s/go.sh",

      ## Create rum_workers service
      "sudo mv /tmp/splunk_worker.service /etc/systemd/system/splunk_worker.service",
      "sudo chown root:root /etc/systemd/system/splunk_worker.service",
      "sudo systemctl daemon-reload",
      "sudo systemctl enable splunk_worker.service",
      "sudo service splunk_worker start",
            
      ## Move and set permissions on message of the day
      "sudo mv /tmp/motd /etc/motd",
      "sudo chmod -x /etc/update-motd.d/*",

      ## Set Password for Ubuntu
      "echo ubuntu:${random_string.rum_worker_password[count.index].result} | sudo chpasswd",
    ]
  }

  connection {
    host = self.public_ip
    type = "ssh"
    user = "ubuntu"
    private_key = file("~/.ssh/id_rsa")
    agent = "true"
  }
}

  output "rum_worker_details" {
    value =  formatlist(
      "%s, %s, %s", 
      aws_instance.rum_worker.*.tags.Name,
      aws_instance.rum_worker.*.public_ip,
      random_string.rum_worker_password.*.result,
    )
  }
