variable "workshop_user_name" {
  description = "Name of the IAM user used to deploy the workshop Lambda resources"
  type        = string
  default     = "lambda_workshop_user"
}