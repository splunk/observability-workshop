variable "aws_profile" {
  description = "AWS profile to use for the AWS provider."
}

variable "aws_region" {
  description = "Provide the desired region (for example: us-west-2)"
}

variable "signalfx_api_access_token" {
  description = "Observability Cloud User API access token."
}

variable "signalfx_realm" {
  description = "Observability Cloud realm."
}

variable "signalfx_aws_integration_name" {
  description = "Name of the AWS integration that shows up in Observability Cloud integrations UI."
}

