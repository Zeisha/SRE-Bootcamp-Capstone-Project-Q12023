module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "capstone-vpc1"
  cidr = "10.0.0.0/16"

  azs             = ["${var.region}a", "${var.region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = false
  enable_ipv6 = true
  assign_ipv6_address_on_creation = true
  private_subnet_assign_ipv6_address_on_creation = false

  public_subnet_ipv6_prefixes = [0, 1]
  private_subnet_ipv6_prefixes = [2, 3]

    tags = {

        Name        = "capstone-vpc1" # Update the name
        Terraform   = "true"
        Service     = "vpc"
        Project     = "sre-bootcamp-2023"
        Environment = "dev"
    }
}