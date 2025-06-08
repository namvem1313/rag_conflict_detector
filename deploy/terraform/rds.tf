resource "aws_db_instance" "postgres" {
  identifier = "ragdb-instance"
  allocated_storage = 20
  engine = "postgres"
  engine_version = "14.1"
  instance_class = "db.t3.micro"
  name = var.db_name
  username = var.db_user
  password = var.db_password
  skip_final_snapshot = true
  publicly_accessible = false
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name = aws_db_subnet_group.rds_subnets.name
}

resource "aws_db_subnet_group" "rds_subnets" {
  name = "rag-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id
}

resource "aws_security_group" "rds_sg" {
  name        = "rag-rds-sg"
  description = "Allow DB access from ECS"
  vpc_id      = aws_vpc.main.id
}
