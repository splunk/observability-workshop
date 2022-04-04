resource "aws_security_group" "collectors" {
  name        = "Collectors"
  description = "Collector traffic"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 55679
    to_port     = 55680
    protocol    = "tcp"
    cidr_blocks = [
      var.vpc_cidr_block
    ]
  }
  ingress {
    from_port   = 9411
    to_port     = 9411
    protocol    = "tcp"
    cidr_blocks = [
      var.vpc_cidr_block
    ]
  }
  ingress {
    from_port   = 9943
    to_port     = 9943
    protocol    = "tcp"
    cidr_blocks = [
      var.vpc_cidr_block
    ]
  }
  ingress {
    from_port   = 6060
    to_port     = 6060
    protocol    = "tcp"
    cidr_blocks = [
      var.vpc_cidr_block
    ]
  }
  ingress {
    from_port   = 7276
    to_port     = 7276
    protocol    = "tcp"
    cidr_blocks = [
      var.vpc_cidr_block
    ]
  }
  ingress {
    from_port   = 13133
    to_port     = 13133
    protocol    = "tcp"
    cidr_blocks = [
      var.vpc_cidr_block
    ]
  }
}
