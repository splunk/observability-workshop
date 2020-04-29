variable "instance_count" {
  description = "Instance Count"
}

variable "region" {
  d
  

  variable "ami" {
  type = "map"

  default = {
    "us-east-1"         = "ami-085925f297f89fce1"
    "us-west-1"         = "ami-0f56279347d2fa43e"
    "eu-central-1"      = "ami-0e342d72b12109f91"
    "eu-west-1"         = "ami-0dad359ff462124ca"
    "ap-southeast-1"    = "ami-0f7719e8b7ba25c61"
  }
}

variable "instance_count" {
  }

variable "instance_type" {
   instance_type = "t2.micro"
}

variable "aws_region" {
  
}
