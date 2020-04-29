variable "instance_count" {
  description = "Instance Count"
}
 
  variable "ami" {
  type = "map"

  default = {
    "us-east-1"         = "ami-085925f297f89fce1"
    "us-west-1"         = "ami-0f56279347d2fa43e"
    "eu-central-1"      = "ami-0e342d72b12109f91"
    "eu-west-1"         = "ami-0dad359ff462124ca"
    "ap-southeast-1"    = "ami-0dad359ff462124ca"
  }
}

variable "region" {
 description = "Please provide region :(us-west-1)) " 
}

variable "instance_type" {
  default = "t2.large"
}
