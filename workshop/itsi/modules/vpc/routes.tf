resource "aws_route" "itsi_vpc_route" {
  route_table_id            = aws_vpc.itsi_vpc.main_route_table_id
  destination_cidr_block    = "0.0.0.0/0"
  gateway_id                = aws_internet_gateway.itsi_vpc_igw.id
}