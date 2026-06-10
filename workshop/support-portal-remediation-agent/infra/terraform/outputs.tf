output "dashboard_group" {
  value = {
    id   = signalfx_dashboard_group.ibobs_demo.id
    name = signalfx_dashboard_group.ibobs_demo.name
  }
}

output "dashboards" {
  value = {
    executive_story = {
      id   = signalfx_dashboard.executive_story.id
      name = signalfx_dashboard.executive_story.name
      url  = signalfx_dashboard.executive_story.url
    }
    business_transactions = {
      id   = signalfx_dashboard.business_transactions.id
      name = signalfx_dashboard.business_transactions.name
      url  = signalfx_dashboard.business_transactions.url
    }
    digital_experience = {
      id   = signalfx_dashboard.digital_experience.id
      name = signalfx_dashboard.digital_experience.name
      url  = signalfx_dashboard.digital_experience.url
    }
    service_health = {
      id   = signalfx_dashboard.service_health.id
      name = signalfx_dashboard.service_health.name
      url  = signalfx_dashboard.service_health.url
    }
    operator_remediation = {
      id   = signalfx_dashboard.operator_remediation.id
      name = signalfx_dashboard.operator_remediation.name
      url  = signalfx_dashboard.operator_remediation.url
    }
  }
}

output "detectors" {
  value = {
    claims_knowledge_filesystem_pressure = {
      id   = signalfx_detector.claims_knowledge_filesystem_pressure.id
      name = signalfx_detector.claims_knowledge_filesystem_pressure.name
      url  = signalfx_detector.claims_knowledge_filesystem_pressure.url
    }
    claims_knowledge_latency = {
      id   = signalfx_detector.claims_knowledge_latency.id
      name = signalfx_detector.claims_knowledge_latency.name
      url  = signalfx_detector.claims_knowledge_latency.url
    }
    claims_knowledge_error_rate = {
      id   = signalfx_detector.claims_knowledge_error_rate.id
      name = signalfx_detector.claims_knowledge_error_rate.name
      url  = signalfx_detector.claims_knowledge_error_rate.url
    }
  }
}
