provider "signalfx" {
  auth_token = var.signalfx_api_access_token
  api_url    = "https://api.${var.signalfx_realm}.signalfx.com"
}

resource "random_id" "random_suffix" {
  byte_length = 8
}

resource "google_project_iam_custom_role" "signalfx_role" {
  provider = google-beta
  role_id     = "signalfxRole_${random_id.random_suffix.hex}"
  title       = "SignalFx Role"
  description = "Role used for monitoring with SignalFx"
  permissions = [
    "monitoring.metricDescriptors.get",
    "monitoring.metricDescriptors.list",
    "monitoring.timeSeries.list",
    "resourcemanager.projects.get",
    "compute.instances.list",
    "compute.machineTypes.list",
    "spanner.instances.list",
    "storage.buckets.list"
  ]
}

resource "google_service_account" "signalfx_sa" {
  provider = google-beta
  account_id   = "signalfx-${var.gcp_project}-sa"
  display_name = "SignalFx Service Account for ${var.gcp_project} managed by terraform"
}

resource "google_service_account_key" "signalfx_sa_key" {
  provider = google-beta
  service_account_id = google_service_account.signalfx_sa.name
}

resource "google_project_iam_member" "signalfx_sa_has_signalfx_role" {
  provider = google-beta
  role   = "projects/${var.gcp_project}/roles/${google_project_iam_custom_role.signalfx_role.role_id}"
  member = "serviceAccount:${google_service_account.signalfx_sa.email}"
}

resource "signalfx_gcp_integration" "signalfx_o11y4gcp" {
  count = var.signalfx_gcp_integration_enabled
  name      = var.signalfx_gcp_integration_name
  enabled   = true
  poll_rate = 60
  project_service_keys {
    project_id  = var.gcp_project
    project_key = base64decode(google_service_account_key.signalfx_sa_key.private_key)
  }
}

