resource "signalfx_detector" "cpu_greater_90" {
  name         = "${var.sfx_prefix} CPU greater than 90%"
  description  = "Alerts when CPU usage is greater than 90%"
  program_text = <<-EOF
    from signalfx.detectors.against_recent import against_recent
    A = data('cpu.utilization', filter=filter('host', '${var.sfx_prefix}*')).publish(label='A')
    detect(when(A > threshold(90))).publish('CPU utilization is greater than 90%')
  EOF
  rule {
    detect_label          = "CPU utilization is greater than 90%"
    notifications         = ["VictorOps,${var.sfx_vo_id},${var.routing_key}"]
    parameterized_subject = "{{ruleSeverity}} Alert: {{{ruleName}}} ({{{detectorName}}})"
    severity              = "Critical"
    parameterized_body    = var.message_body
  }
}