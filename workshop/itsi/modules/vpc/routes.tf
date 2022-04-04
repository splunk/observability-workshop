resource "aws_route" "main_vpc_route" {
  route_table_id            = aws_vpc.main_vpc.main_route_table_id
  destination_cidr_block    = "0.0.0.0/0"
  gateway_id                = aws_internet_gateway.main_vpc_igw.id
}