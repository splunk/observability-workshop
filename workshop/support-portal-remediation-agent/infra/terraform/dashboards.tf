resource "signalfx_dashboard" "executive_story" {
  name            = "IBOBS Executive Story"
  dashboard_group = signalfx_dashboard_group.ibobs_demo.id

  time_range = "-30m"

  chart {
    chart_id = signalfx_time_chart.apm_service_duration.id
    width    = 6
    height   = 1
    row      = 0
    column   = 0
  }

  chart {
    chart_id = signalfx_single_value_chart.student_filesystem_utilization.id
    width    = 6
    height   = 1
    row      = 0
    column   = 6
  }
}

resource "signalfx_time_chart" "apm_service_duration" {
  name = "Claims Portal Request Duration"

  program_text = <<-EOF
    A = data('service.request.duration.ns', filter=filter('deployment.environment', '${var.deployment_environment}') and filter('service.instance.id', '${var.instance}')).percentile(pct=95, by=['sf_service']).publish(label='P95 Duration')
  EOF
}

resource "signalfx_single_value_chart" "student_filesystem_utilization" {
  name = "Claims Knowledge Cache Filesystem Utilization"

  program_text = <<-EOF
    A = data('${var.cache_utilization_metric}', filter=filter('deployment.environment', '${var.deployment_environment}') and filter('service.name', 'claims-knowledge') and filter('service.instance.id', '${var.instance}') and filter('mountpoint', '${var.cache_mountpoint}') and filter('demo.metric_source', '${var.evidence_metric_source}')).max(by=['service.name', 'service.instance.id', 'mountpoint']).publish(label='Claims Knowledge Cache Utilization')
  EOF
}

resource "signalfx_dashboard" "business_transactions" {
  name            = "IBOBS APM Service Requests"
  dashboard_group = signalfx_dashboard_group.ibobs_demo.id

  time_range = "-30m"

  chart {
    chart_id = signalfx_time_chart.apm_request_count.id
    width    = 12
    height   = 1
    row      = 0
    column   = 0
  }
}

resource "signalfx_time_chart" "apm_request_count" {
  name = "Request Count by Service"

  program_text = <<-EOF
    A = data('service.request', filter=filter('deployment.environment', '${var.deployment_environment}') and filter('service.instance.id', '${var.instance}')).count(by=['sf_service']).publish(label='Requests')
  EOF
}

resource "signalfx_dashboard" "digital_experience" {
  name            = "IBOBS Digital Experience"
  dashboard_group = signalfx_dashboard_group.ibobs_demo.id

  time_range = "-30m"

  chart {
    chart_id = signalfx_time_chart.frontend_transaction_spans.id
    width    = 12
    height   = 1
    row      = 0
    column   = 0
  }
}

resource "signalfx_time_chart" "frontend_transaction_spans" {
  name = "Frontend Transaction Spans"

  program_text = <<-EOF
    A = data('service.request', filter=filter('deployment.environment', '${var.deployment_environment}') and filter('sf_service', 'ibobs-claims-portal')).count(by=['app.business_transaction']).publish(label='Transactions')
  EOF
}

resource "signalfx_dashboard" "service_health" {
  name            = "IBOBS Service Health"
  dashboard_group = signalfx_dashboard_group.ibobs_demo.id

  time_range = "-30m"

  chart {
    chart_id = signalfx_time_chart.apm_error_rate.id
    width    = 6
    height   = 1
    row      = 0
    column   = 0
  }

  chart {
    chart_id = signalfx_time_chart.host_filesystem_utilization.id
    width    = 6
    height   = 1
    row      = 0
    column   = 6
  }
}

resource "signalfx_time_chart" "apm_error_rate" {
  name = "APM Error Rate by Service"

  program_text = <<-EOF
    A = data('service.request', filter=filter('deployment.environment', '${var.deployment_environment}') and filter('service.instance.id', '${var.instance}') and filter('sf_error', 'true')).count(by=['sf_service'])
    B = data('service.request', filter=filter('deployment.environment', '${var.deployment_environment}') and filter('service.instance.id', '${var.instance}')).count(by=['sf_service'])
    C = (A / B).publish(label='Error Rate')
  EOF
}

resource "signalfx_time_chart" "host_filesystem_utilization" {
  name = "Claims Knowledge Cache Filesystem Utilization"

  program_text = <<-EOF
    A = data('${var.cache_utilization_metric}', filter=filter('deployment.environment', '${var.deployment_environment}') and filter('service.name', 'claims-knowledge') and filter('service.instance.id', '${var.instance}') and filter('mountpoint', '${var.cache_mountpoint}') and filter('demo.metric_source', '${var.evidence_metric_source}')).max(by=['service.name', 'service.instance.id', 'mountpoint']).publish(label='Claims Knowledge Cache Utilization')
  EOF
}

resource "signalfx_dashboard" "operator_remediation" {
  name            = "IBOBS Remediation Operations"
  dashboard_group = signalfx_dashboard_group.ibobs_demo.id

  time_range = "-30m"

  chart {
    chart_id = signalfx_time_chart.orchestrator_duration.id
    width    = 6
    height   = 1
    row      = 0
    column   = 0
  }

  chart {
    chart_id = signalfx_time_chart.agent_duration.id
    width    = 6
    height   = 1
    row      = 0
    column   = 6
  }
}

resource "signalfx_time_chart" "orchestrator_duration" {
  name = "Orchestrator Request Duration"

  program_text = <<-EOF
    A = data('service.request.duration.ns', filter=filter('deployment.environment', '${var.deployment_environment}') and filter('service.instance.id', '${var.instance}') and filter('sf_service', 'remediation-orchestrator')).percentile(pct=95).publish(label='P95 Duration')
  EOF
}

resource "signalfx_time_chart" "agent_duration" {
  name = "Remediation Agent Request Duration"

  program_text = <<-EOF
    A = data('service.request.duration.ns', filter=filter('deployment.environment', '${var.deployment_environment}') and filter('service.instance.id', '${var.instance}') and filter('sf_service', 'remediation-agent')).percentile(pct=95).publish(label='P95 Duration')
  EOF
}
