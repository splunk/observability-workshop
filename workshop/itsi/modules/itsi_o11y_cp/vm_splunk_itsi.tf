resource "random_string" "splunk_itsi_password" {
  length           = 12
  special          = false
}

resource "aws_instance" "splunk_itsi" {
  count                     = var.splunk_itsi_count
  ami                       = var.ami
  instance_type             = var.splunk_itsi_inst_type
  subnet_id                 = var.itsi_public_subnet_id
    root_block_device {
    volume_size = 32
    volume_type = "gp3"
  }
  key_name                  = var.key_name
  vpc_security_group_ids    = [
    aws_security_group.itsi_sg.id
  ]

  tags = {
    Component = "itsi-for-${var.workshop_name}"
    Name = lower(join("-",[var.workshop_name,"itsi",count.index + 1]))
    Role = "ITSI Server"
  }

  provisioner "file" {
     source      = "${path.module}/scripts/install_ITSI_Content_Pack.sh"
     destination = "/tmp/install_ITSI_Content_Pack.sh"
   }

  provisioner "file" {
     source      = join("/",[var.splunk_itsi_files_local_path,var.splunk_itsi_license_filename])
     destination = join("/",["/tmp",var.splunk_itsi_license_filename])
   }

  provisioner "remote-exec" {
    inline = [
      "sudo sed -i 's/127.0.0.1.*/127.0.0.1 ${self.tags.Name}.local ${self.tags.Name} localhost/' /etc/hosts",
      "sudo hostnamectl set-hostname ${self.tags.Name}",
      "sudo apt-get update",
      "sudo apt-get upgrade -y",
     
    ## Create Splunk Ent Vars
      "SPLUNK_ITSI_PASSWORD=${random_string.splunk_itsi_password.result}",
      "SPLUNK_ITSI_VERSION=${var.splunk_itsi_version}",
      "SPLUNK_ITSI_FILENAME=${var.splunk_itsi_filename}",
      "SPLUNK_ITSI_LICENSE_FILE=${var.splunk_itsi_license_filename}",
      "SPLUNK_APP_FOR_CONTENT_PACKS_FILE=${var.splunk_app_for_content_packs_filename}",
      "SPLUNK_IT_SERVICE_INTELLIGENCE_FILE=${var.splunk_it_service_intelligence_filename}",
      "SPLUNK_SYNTHETIC_MONITORING_ADD_ON_FILE=${var.splunk_synthetic_monitoring_add_on_filename}",
      "SPLUNK_INFRASTRUCTURE_MONITORING_ADD_ON_FILE=${var.splunk_infrastructure_monitoring_add_on_filename}",
      
    ## Write env vars to file (used for debugging)
      "echo $SPLUNK_ITSI_PASSWORD > /tmp/splunk_itsi_password",
      "echo $SPLUNK_ITSI_VERSION > /tmp/splunk_itsi_version",
      "echo $SPLUNK_ITSI_FILENAME > /tmp/splunk_itsi_filename",
      "echo $SPLUNK_ITSI_LICENSE_FILE > /tmp/splunk_itsi_license_file",
      "echo $SPLUNK_APP_FOR_CONTENT_PACKS_FILE > /tmp/splunk_app_for_content_packs_filename",
      "echo $SPLUNK_IT_SERVICE_INTELLIGENCE_FILE > /tmp/splunk_it_service_intelligence_filename",
      "echo $SPLUNK_SYNTHETIC_MONITORING_ADD_ON_FILE > /tmp/splunk_synthetic_monitoring_add_on_file",
      "echo $SPLUNK_INFRASTRUCTURE_MONITORING_ADD_ON_FILE > /tmp/splunk_infrastructure_monitoring_add_on_file",

    ## Install Splunk + ITSI + O11y Content Pack
      "sudo chmod +x /tmp/install_ITSI_Content_Pack.sh",
      "sudo /tmp/install_ITSI_Content_Pack.sh $SPLUNK_ITSI_PASSWORD $SPLUNK_ITSI_VERSION $SPLUNK_ITSI_FILENAME $SPLUNK_ITSI_LICENSE_FILE $SPLUNK_APP_FOR_CONTENT_PACKS_FILE $SPLUNK_IT_SERVICE_INTELLIGENCE_FILE $SPLUNK_SYNTHETIC_MONITORING_ADD_ON_FILE $SPLUNK_INFRASTRUCTURE_MONITORING_ADD_ON_FILE",
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

output "splunk_itsi_details" {
  value =  formatlist(
    "%s, %s", 
    aws_instance.splunk_itsi.*.tags.Name,
    aws_instance.splunk_itsi.*.public_ip,
  )
}

output "splunk_itsi_urls" {
  value =  formatlist(
    "%s%s:%s", 
    "http://",
    aws_instance.splunk_itsi.*.public_ip,
    "8000",
  )
}

output "splunk_itsi_password" {
  value = random_string.splunk_itsi_password.result
}
