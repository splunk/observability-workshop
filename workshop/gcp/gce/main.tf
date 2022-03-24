provider "google-beta" {
  project = var.gcp_project
  region  = var.gcp_zone

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

resource "google_project_service" "cloudresourcemanager_svc" {
  provider = google-beta
  project            = "projects/${var.gcp_project}"
  service            = "cloudresourcemanager.googleapis.com"
  disable_on_destroy = false
}

resource "google_compute_firewall" "allow_ingress_traffic" {
  provider = google-beta
  name     = "allow-ingress-traffic"
  network  = "default"

  allow {
    protocol = "tcp"
    ports    = ["22", "8080", "8081", "6501"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["o11y-instance"]
}

resource "google_compute_firewall" "allow_egress_traffic" {
  provider  = google-beta
  name      = "allow-egress-traffic"
  network   = "default"
  direction = "EGRESS"

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
  }

  allow {
    protocol = "udp"
  }

  destination_ranges = ["0.0.0.0/0"]
  target_tags        = ["o11y-instance"]
}

resource "google_compute_instance" "o11y-instance" {
  provider     = google-beta
  count        = var.gcp_instance_count
  name         = "o11y-${count.index + 1}"
  machine_type = var.gcp_instance_type
  zone         = var.gcp_zone

  tags = ["o11y-instance"]

  metadata = {
    user-data = file("../../cloud-init/k3s.yaml")
  }

  labels = {
    name = "observability-${count.index + 1}"
  }

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral IP
    }
  }
}

output "ip" {
  value = google_compute_instance.o11y-instance.*.network_interface.0.access_config.0.nat_ip
}
