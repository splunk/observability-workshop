output "cluster_name" {
  description = "EKS cluster name."
  value       = aws_eks_cluster.this.name
}

output "aws_region" {
  description = "AWS region."
  value       = var.aws_region
}

output "kubeconfig_command" {
  description = "Command to configure kubectl for the lab cluster."
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${aws_eks_cluster.this.name}"
}

output "vpc_id" {
  description = "Lab VPC ID."
  value       = aws_vpc.this.id
}

output "private_subnet_ids" {
  description = "Private subnet IDs used by EKS and GPU nodes."
  value       = aws_subnet.private[*].id
}

output "public_subnet_ids" {
  description = "Public subnet IDs."
  value       = aws_subnet.public[*].id
}

output "student_namespaces" {
  description = "Generated student namespaces."
  value       = local.student_namespaces
}

output "ecr_repository_urls" {
  description = "ECR repository URLs for lab images."
  value = {
    for name, repo in aws_ecr_repository.lab : name => repo.repository_url
  }
}
