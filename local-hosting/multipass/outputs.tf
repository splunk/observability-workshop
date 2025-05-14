output "instance_details" {
  value = data.multipass_instance.ubuntu.*
}

# Outputs for debugging purposes
output "swipe_id" {
  description = "SWiPE ID"
  value       = var.swipe_id
  sensitive   = false
}
output "swipe_data" {
  description = "Complete response from Swipe API"
  value       = local.swipe_data
  sensitive   = false
}