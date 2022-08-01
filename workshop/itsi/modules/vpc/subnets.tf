# Fetch AZs in the current region
data "aws_availability_zones" "available" {
}

# Create ITSI Public Subnet
resource "aws_subnet" "itsi_public_subnet" {
  cidr_block              = cidrsubnet(aws_vpc.itsi_vpc.cidr_block, 8, 1)
  vpc_id                  = aws_vpc.itsi_vpc.id
  map_public_ip_on_launch = true

  tags = {
    Name  =        join("-", [var.workshop_name, "itsi-public"])
  }
}
