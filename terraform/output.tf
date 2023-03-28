#Log the load balancer app URL
output "capstone_app_url" {
  value = aws_alb.capstone_load_balancer.dns_name
}