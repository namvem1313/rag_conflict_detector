resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = { Name = "rag-vpc" }
}

resource "aws_subnet" "public" {
  count = 2
  cidr_block = "10.0.${count.index}.0/24"
  map_public_ip_on_launch = true
  vpc_id = aws_vpc.main.id
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
  tags = { Name = "rag-public-subnet-${count.index}" }
}

resource "aws_subnet" "private" {
  count = 2
  cidr_block = "10.0.${count.index + 10}.0/24"
  vpc_id = aws_vpc.main.id
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
  tags = { Name = "rag-private-subnet-${count.index}" }
}
