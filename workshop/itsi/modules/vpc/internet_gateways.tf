resource "aws_internet_gateway" "itsi_vpc_igw" {
  vpc_id = aws_vpc.itsi_vpc.id

  tags = {
    Name = "icw_${var.workshop_name}"
  }
}
