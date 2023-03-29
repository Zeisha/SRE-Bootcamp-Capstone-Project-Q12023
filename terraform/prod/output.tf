#Log the load balancer app URL
output "capstone_app_url" {
  value = aws_alb.load-balancer.dns_name
}