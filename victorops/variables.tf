variable "access_token" {
  description = "SignalFx Access Token"
}

variable "realm" {
  description = "SignalFx Realm"
}

variable "sfx_prefix" {
  type        = string
  description = "Detector Prefix"
  default     = "[SFx]"
}

variable "sfx_vo_id" {
  type        = string
  description = "SignalFx VictorOps Integration ID"
}

variable "routing_key" {
  type        = string
  description = "VictorOps Routing Key"
}