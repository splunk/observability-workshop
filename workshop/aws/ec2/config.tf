 /* data "template_file" "user_data" {
  templatefile = "${file("${path.module}/templates/userdata.yaml")}"
  vars = {
    access_token = "${var.splunk_access_token}"
    rum_token = "${var.splunk_rum_token}"
    realm = "${var.splunk_realm}"
    presetup = "${var.splunk_presetup}"
  }
}  */

/* data "template_cloudinit_config" "config" {
  gzip          = false
  base64_encode = false
  part {
    content_type = "text/cloud-config"
    content      = data.template_file.user_data.rendered
  }
} */
