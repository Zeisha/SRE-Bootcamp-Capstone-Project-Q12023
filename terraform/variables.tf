variable "region" {
  description = "AWS Default region"
  default = "us-east-2"
}

variable "project_name" {
  description = "The name of the project"
}

variable "image_tag" {
  description = "The docker image tag to use in production container"
}

variable "task_family_name" {
  description = "The Task Definition Family"
}