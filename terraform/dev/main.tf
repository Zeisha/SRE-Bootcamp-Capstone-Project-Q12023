# Configure cloud watch 
resource "aws_cloudwatch_log_group" "capstone-watch" {
  name              = "capstone-watch"
  retention_in_days = 1
}

resource "aws_kms_key" "capstone-kms" {
  description             = "capstone kms key"
  deletion_window_in_days = 7
}

# Configure ECS Cluster
resource "aws_ecs_cluster" "cluster" {
  name = "${var.project_name}-cluster"

  configuration {
    execute_command_configuration {
      kms_key_id = aws_kms_key.capstone-kms.arn
      logging    = "OVERRIDE"

      log_configuration {
        cloud_watch_encryption_enabled = true
        cloud_watch_log_group_name     = aws_cloudwatch_log_group.capstone-watch.name
      }
    }
  }
}

# Configure Task Defination
resource "aws_ecs_task_definition" "task" {
  family = var.task_family_name

  container_definitions = <<EOF
[
  {
    "name": "${var.task_family_name}",
    "image": "zeisha/academy-sre-bootcamp-poonam-yadav:${var.image_tag}",
    "cpu": 256,
    "memoryReservation": 512,
    "links": [],
    "portMappings": [
      {
        "containerPort": 8000,
        "hostPort": 8000,
        "protocol": "tcp"
      }
    ],
    "essential": true,
    "environmentFiles": [
      {
          "value": "arn:aws:s3:::696532135023capstonebucket/.env",
          "type": "s3"
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/capstone",
        "awslogs-region": "${var.region}",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }
]
EOF
  requires_compatibilities = ["FARGATE"] # use Fargate as the launch type
  network_mode             = "awsvpc"    # add the AWS VPN network mode as this is required for Fargate
  memory                   = 512         # Specify the memory the container requires
  cpu                      = 256         # Specify the CPU the container requires
  execution_role_arn       = aws_iam_role.ecsTaskExecutionRole.arn
}

#Configure task execution role , import of this existing iam role needed
resource "aws_iam_role" "ecsTaskExecutionRole" {
  name               = "ecsTaskExecutionRole"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecs-execution-policy" {
  role       = aws_iam_role.ecsTaskExecutionRole.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}



#Configure load balancer
resource "aws_alb" "load-balancer" {
  name               = "${var.project_name}-lb"
  load_balancer_type = "application"
  subnets            = module.vpc.public_subnets

  # security group
  security_groups = [aws_security_group.lb-security-group.id]
}

# create target group 

resource "aws_lb_target_group" "lb-target-group" {
  name        = "${var.project_name}-lb-tg"
  port        = 8000
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = module.vpc.vpc_id
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_alb.load-balancer.arn #  load balancer
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.lb-target-group.arn # target group
  }
}


# Configure ECS Service
resource "aws_ecs_service" "cluster-service" {
  name                 = "${var.project_name}-service"
  cluster              = aws_ecs_cluster.cluster.id
  task_definition      = aws_ecs_task_definition.task.arn
  force_new_deployment = true
  launch_type          = "FARGATE"
  desired_count        = 2

  load_balancer {
    target_group_arn = aws_lb_target_group.lb-target-group.arn # Reference the target group
    container_name   = aws_ecs_task_definition.task.family
    container_port   = 8000 # Specify the container port
  }

  network_configuration {
    subnets          = module.vpc.public_subnets
    assign_public_ip = true # Provide the containers with public IPs
    security_groups  = [aws_security_group.service-security-group.id]
  }

  deployment_maximum_percent         = 100
  deployment_minimum_healthy_percent = 50
}
