resource "aws_internet_gateway" "main_vpc_igw" {
  vpc_id = aws_vpc.main_vpc.id

  tags = {
    Name = "icw_${var.environment}"
  }
}