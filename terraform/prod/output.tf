
output "capstone_app_url" {
  value = aws_alb.load-balancer.dns_name
}