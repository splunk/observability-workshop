/*output "user_data" {
  value = templatefile("${path.module}/templates/userdata.yaml",
    {
     access_token = "${var.splunk_access_token}" 
     rum_token = "${var.splunk_rum_token}" 
     realm = "${var.splunk_realm}" 
     presetup = "${var.splunk_presetup}"
    } )
}*/

output "ip-addresses" {
  value = aws_instance.observability-instance.*.public_ip
}