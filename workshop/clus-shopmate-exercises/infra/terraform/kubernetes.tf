resource "kubernetes_namespace_v1" "platform" {
  for_each = var.manage_kubernetes_baseline ? local.platform_namespaces : toset([])

  metadata {
    name = each.key

    labels = {
      "app.kubernetes.io/part-of" = var.project_name
      "lab.splunk.com/owner"      = "instructor"
    }
  }

  depends_on = [aws_eks_node_group.gpu]
}

resource "kubernetes_namespace_v1" "student" {
  for_each = var.manage_kubernetes_baseline ? toset(local.student_namespaces) : toset([])

  metadata {
    name = each.key

    labels = {
      "app.kubernetes.io/part-of" = var.project_name
      "lab.splunk.com/student-id" = each.key
    }
  }

  depends_on = [aws_eks_node_group.gpu]
}

resource "kubernetes_service_account_v1" "student" {
  for_each = kubernetes_namespace_v1.student

  metadata {
    name      = "student"
    namespace = each.value.metadata[0].name

    labels = {
      "app.kubernetes.io/part-of" = var.project_name
      "lab.splunk.com/student-id" = each.key
    }
  }
}

resource "kubernetes_role_v1" "student" {
  for_each = kubernetes_namespace_v1.student

  metadata {
    name      = "student-workshop"
    namespace = each.value.metadata[0].name
  }

  rule {
    api_groups = [""]
    resources  = ["configmaps", "pods", "pods/log", "secrets", "services"]
    verbs      = ["get", "list", "watch", "create", "update", "patch", "delete"]
  }

  rule {
    api_groups = [""]
    resources  = ["pods/portforward"]
    verbs      = ["create"]
  }

  rule {
    api_groups = [""]
    resources  = ["endpoints"]
    verbs      = ["get", "list", "watch"]
  }

  rule {
    api_groups = ["discovery.k8s.io"]
    resources  = ["endpointslices"]
    verbs      = ["get", "list", "watch"]
  }

  rule {
    api_groups = ["apps"]
    resources  = ["deployments", "replicasets"]
    verbs      = ["get", "list", "watch", "create", "update", "patch", "delete"]
  }

  rule {
    api_groups = ["batch"]
    resources  = ["jobs"]
    verbs      = ["get", "list", "watch", "create", "update", "patch", "delete"]
  }

  rule {
    api_groups = ["networking.k8s.io"]
    resources  = ["ingresses"]
    verbs      = ["get", "list", "watch", "create", "update", "patch", "delete"]
  }
}

resource "kubernetes_role_binding_v1" "student" {
  for_each = kubernetes_namespace_v1.student

  metadata {
    name      = "student-workshop"
    namespace = each.value.metadata[0].name
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Role"
    name      = kubernetes_role_v1.student[each.key].metadata[0].name
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account_v1.student[each.key].metadata[0].name
    namespace = each.value.metadata[0].name
  }
}
