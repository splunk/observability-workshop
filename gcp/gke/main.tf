provider "google-beta" {
  project = var.gcp_project
  region  = var.gcp_region

  scopes = [
    # Default scopes
    "https://www.googleapis.com/auth/compute",
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/ndev.clouddns.readwrite",
    "https://www.googleapis.com/auth/devstorage.full_control",

    # Required for google_client_openid_userinfo
    "https://www.googleapis.com/auth/userinfo.email",
  ]
}

resource "google_project_service" "container_svc" {
  provider = google-beta
  project            = "projects/${var.gcp_project}"
  service            = "container.googleapis.com"
  disable_on_destroy = false
}

resource "random_password" "gke_password" {
  length = 16
  special = false
}

resource "google_compute_network" "vpc" {
  provider = google-beta
  name                    = "${var.gcp_project}-vpc"
  auto_create_subnetworks = "false"
}

# Subnet
resource "google_compute_subnetwork" "subnet" {
  provider = google-beta
  name          = "${var.gcp_project}-subnet"
  region        = var.gcp_region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.10.0.0/24"

}

resource "google_container_cluster" "o11y-gke" {
  provider = google-beta
  name     = "${var.gcp_project}-gke"
  location = var.gcp_region

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  master_auth {
    username = var.gke_username
    password = random_password.gke_password.result

    client_certificate_config {
      issue_client_certificate = false
    }
  }
}

resource "google_container_node_pool" "primary_nodes" {
  provider = google-beta
  name       = "${google_container_cluster.o11y-gke.name}-node-pool"
  location   = var.gcp_region
  cluster    = google_container_cluster.o11y-gke.name
  node_count = var.gke_num_nodes

  node_config {
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]

    labels = {
      env = var.gcp_project
    }

    # preemptible  = true
    machine_type = "n1-standard-1"
    tags         = ["gke-node", "${var.gcp_project}-gke"]
    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}

output "kubernetes_cluster_name" {
  value       = google_container_cluster.o11y-gke.name
  description = "GKE Cluster Name"
}

output "gke_password" {
  value       = random_password.gke_password.result
  description = "GKE Password for 'admin' user"
}

output "gke_region" {
  value       = var.gcp_region
  description = "GKE cluster region"
}
