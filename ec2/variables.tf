variable "aws_instance_count" {
  description = "Instance Count"
}
 
variable "ami" {
  type = map

  default = {
    "us-east-1"         = "ami-085925f297f89fce1"
    "us-west-1"         = "ami-0f56279347d2fa43e"
    "eu-central-1"      = "ami-0e342d72b12109f91"
    "eu-west-1"         = "ami-0dad359ff462124ca"
    "ap-southeast-1"    = "ami-0dad359ff462124ca"
  }
}

variable "aws_region" {
 description = "Region (us-east-1, us-west-1, eu-central-1, eu-west-1, ap-southeast-1)" 
}

variable "instance_type" {
  default = "t2.large"
}

variable "key_name" {
  description = "Provide a valid key name for the region "
}