output "workshop_user_name" {
  description = "IAM user used to deploy workshop Lambda resources"
  value       = aws_iam_user.workshop.name
}

output "workshop_access_key_id" {
  description = "Access key ID for the workshop IAM user"
  value       = aws_iam_access_key.workshop.id
}

output "workshop_secret_access_key" {
  description = "Secret access key for the workshop IAM user"
  value       = aws_iam_access_key.workshop.secret
  sensitive   = true
}
