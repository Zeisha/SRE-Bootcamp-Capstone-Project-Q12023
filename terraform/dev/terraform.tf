terraform {
  cloud {
    organization = "capstone-ltd"
    workspaces {
      name = "capstone-dev-infra"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.region
}
