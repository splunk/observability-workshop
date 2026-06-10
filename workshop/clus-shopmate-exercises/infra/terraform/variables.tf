variable "aws_region" {
  description = "AWS region for the EKS lab stack."
  type        = string
  default     = "us-east-2"
}

variable "project_name" {
  description = "Project tag and cluster-name prefix."
  type        = string
  default     = "clus-ltrobs-2001"
}

variable "environment" {
  description = "Environment name, for example dev, dry-run, or event."
  type        = string
  default     = "dev"
}

variable "cluster_name" {
  description = "Optional explicit EKS cluster name. Defaults to project-environment."
  type        = string
  default     = ""
}

variable "owner" {
  description = "Owner tag for lab resources."
  type        = string
}

variable "expires_at" {
  description = "Expiration timestamp tag for lab resources."
  type        = string
}

variable "tags" {
  description = "Additional tags applied to AWS resources."
  type        = map(string)
  default     = {}
}

variable "vpc_cidr" {
  description = "CIDR block for the lab VPC."
  type        = string
  default     = "10.42.0.0/16"
}

variable "az_count" {
  description = "Number of availability zones to use."
  type        = number
  default     = 3

  validation {
    condition     = var.az_count >= 2 && var.az_count <= 4
    error_message = "az_count must be between 2 and 4."
  }
}

variable "enable_nat_gateway" {
  description = "Create a single NAT gateway for private subnet egress."
  type        = bool
  default     = true
}

variable "kubernetes_version" {
  description = "EKS Kubernetes version."
  type        = string
  default     = "1.30"
}

variable "cluster_endpoint_public_access" {
  description = "Allow public access to the EKS control plane endpoint."
  type        = bool
  default     = true
}

variable "cluster_endpoint_private_access" {
  description = "Allow private access to the EKS control plane endpoint."
  type        = bool
  default     = true
}

variable "gpu_instance_type" {
  description = "GPU worker node instance type."
  type        = string
  default     = "g5.4xlarge"
}

variable "gpu_node_ami_type" {
  description = "Managed node group AMI type for GPU nodes."
  type        = string
  default     = "AL2023_x86_64_NVIDIA"
}

variable "gpu_desired_size" {
  description = "Desired GPU node count."
  type        = number
  default     = 2
}

variable "gpu_min_size" {
  description = "Minimum GPU node count."
  type        = number
  default     = 0
}

variable "gpu_max_size" {
  description = "Maximum GPU node count."
  type        = number
  default     = 2
}

variable "gpu_node_disk_size_gb" {
  description = "Root disk size for GPU nodes."
  type        = number
  default     = 200
}

variable "gpu_node_taint_enabled" {
  description = "Apply a NoSchedule taint to GPU nodes."
  type        = bool
  default     = false
}

variable "student_count" {
  description = "Number of student namespaces and RBAC sets to create."
  type        = number
  default     = 20

  validation {
    condition     = var.student_count >= 1 && var.student_count <= 60
    error_message = "student_count must be between 1 and 60."
  }
}

variable "student_namespace_prefix" {
  description = "Prefix for generated student namespaces."
  type        = string
  default     = "student"
}

variable "manage_kubernetes_baseline" {
  description = "Create platform and student Kubernetes namespaces and RBAC."
  type        = bool
  default     = true
}

variable "install_gpu_operator" {
  description = "Install NVIDIA GPU Operator with Helm."
  type        = bool
  default     = true
}

variable "gpu_operator_chart_version" {
  description = "Optional NVIDIA GPU Operator chart version. Empty uses the chart repository default."
  type        = string
  default     = ""
}

variable "enable_ebs_csi_driver" {
  description = "Install the AWS EBS CSI Driver EKS add-on with IRSA."
  type        = bool
  default     = true
}

variable "ecr_repositories" {
  description = "ECR repositories to create for lab images."
  type        = list(string)
  default     = ["shopmate-ai", "loadgen"]
}
