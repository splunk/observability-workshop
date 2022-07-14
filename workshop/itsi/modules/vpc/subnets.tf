# Fetch AZs in the current region
data "aws_availability_zones" "available" {
}

# Create private subnets, each in a different AZ
resource "aws_subnet" "private_subnets" {
  cidr_block        = cidrsubnet(aws_vpc.itsi_vpc.cidr_block, 8, 1)
  vpc_id            = aws_vpc.itsi_vpc.id

  tags = {
    Name  =        join("-", [var.environment, "itsi-private"])
  }
}

# Create public subnets, each in a different AZ
resource "aws_subnet" "public_subnets" {
  cidr_block              = cidrsubnet(aws_vpc.itsi_vpc.cidr_block, 8, 2)
  vpc_id                  = aws_vpc.itsi_vpc.id
  map_public_ip_on_launch = true

  tags = {
    Name  =        join("-", [var.environment, "itsi-public"])
  }
}