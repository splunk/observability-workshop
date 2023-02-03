variable "access_token" {
  description = "Splunk Access Token"
}

variable "realm" {
  description = "Splunk Realm"
}

variable "sfx_prefix" {
  description = "Detector Prefix"
}

variable "sfx_vo_id" {
  description = "Splunk On-Call Integration ID"
}

variable "routing_key" {
  description = "Splunk On-Call Routing Key"
}

variable "message_body" {
  default = <<-EOF
    {{#if anomalous}}
        Rule "{{{ruleName}}}" in detector "{{{detectorName}}}" triggered at {{timestamp}}.
    {{else}}
        Rule "{{{ruleName}}}" in detector "{{{detectorName}}}" cleared at {{timestamp}}.
    {{/if}}

    {{#if anomalous}}
      Triggering condition: {{{readableRule}}}
    {{/if}}

    {{#if anomalous}}
      Signal value: {{inputs.A.value}}
    {{else}}
      Current signal value: {{inputs.A.value}}
    {{/if}}

    {{#notEmpty dimensions}}
      Signal details: {{{dimensions}}}
    {{/notEmpty}}

    {{#if anomalous}}
      {{#if runbookUrl}}
        Runbook: {{{runbookUrl}}}
      {{/if}}
      {{#if tip}}
        Tip: {{{tip}}}
      {{/if}}
    {{/if}}
  EOF
}
