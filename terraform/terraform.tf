terraform {
  cloud {
    organization = "capstone-ltd"
    workspaces {
      name = "capstone-infra"
  }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}


# Configure the AWS Provider
provider "aws" {
  region = var.region
}
