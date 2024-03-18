variable "signalfx_key" {
  type = string
}

variable "api_url" {
  type = string
}

terraform {
  required_providers {
    signalfx = {
      source = "splunk-terraform/signalfx"
      version = "9.1.1"
    }
  }
}

provider "signalfx" {
  auth_token = var.signalfx_key
  api_url = var.api_url
}

resource "signalfx_detector" "cpu_detector" {
  name        = "OAC - CPU over 90% for 1 minute"
  description = ""
  max_delay   = 30
  tags        = ["prod"]

  program_text = <<-EOF
  signal = data('cpu.utilization').publish()
  detect(when(signal > 90, '1m')).publish('CPU over 90% for 1 min')
  EOF
  rule {
    description   = "CPU over 90% for 1 min"
    severity      = "Critical"
    detect_label  = "CPU over 90% for 1 min"
    notifications = ["Email,foo-alerts@bar.com"]
  }
}

resource "signalfx_time_chart" "mychart0" {
    name = "CPU Utilization"
    description = "Very cool CPU chart"

    program_text = <<-EOF
    A=data("cpu.utilization").publish()
    B = alerts(detector_id="${signalfx_detector.cpu_detector.id}").publish(label="B");
    EOF
}

resource "signalfx_dashboard_group" "mydashgroup0" {
  name = "OAC Demo Dashboard Group"
}

resource "signalfx_dashboard" "mydashboard0" {
  name = "OAC Demo Dashboard"
  dashboard_group = signalfx_dashboard_group.mydashgroup0.id

  chart {
    chart_id = signalfx_time_chart.mychart0.id
    width = 12
    height = 1
    row = 0
  }
}
