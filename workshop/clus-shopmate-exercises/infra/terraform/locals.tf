locals {
  cluster_name = var.cluster_name != "" ? var.cluster_name : "${var.project_name}-${var.environment}"

  required_tags = {
    Project     = var.project_name
    Environment = var.environment
    Stack       = local.cluster_name
    Owner       = var.owner
    ExpiresAt   = var.expires_at
    ManagedBy   = "terraform"
  }

  tags = merge(local.required_tags, var.tags)

  student_namespaces = [
    for index in range(var.student_count) :
    format("%s-%02d", var.student_namespace_prefix, index + 1)
  ]

  platform_namespaces = toset([
    "gpu-operator",
    "nim-system",
    "observability",
  ])
}
