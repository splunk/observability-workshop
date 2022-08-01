output "vpc_id" {
    value = aws_vpc.itsi_vpc.id
}

output "itsi_public_subnet_id" {
    value = aws_subnet.itsi_public_subnet.id
}
