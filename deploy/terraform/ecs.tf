resource "aws_ecs_cluster" "main" {
  name = "${var.app_name}-cluster"
}

resource "aws_ecs_task_definition" "app_task" {
  family                   = "${var.app_name}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([
    {
      name      = "app"
      image     = "yourdockerhubuser/rag-app:latest"
      essential = true
      portMappings = [
        {
          containerPort = 5055
        }
      ],
      environment = [
        { name = "DB_HOST", value = module.rds.db_endpoint },
        { name = "DB_USER", value = var.db_user },
        { name = "DB_PASSWORD", value = var.db_password }
      ]
    }
  ])
}

resource "aws_ecs_service" "app_service" {
  name            = "${var.app_name}-service"
  cluster         = aws_ecs_cluster.main.id
  launch_type     = "FARGATE"
  desired_count   = 1
  task_definition = aws_ecs_task_definition.app_task.arn

  network_configuration {
    subnets          = aws_subnet.public[*].id
    assign_public_ip = true
    security_groups  = [aws_security_group.app_sg.id]
  }
}

resource "aws_security_group" "app_sg" {
  name        = "rag-app-sg"
  vpc_id      = aws_vpc.main.id
  description = "Allow HTTP traffic"
  ingress = [{
    from_port   = 5055
    to_port     = 5055
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }]
  egress = [{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }]
}
