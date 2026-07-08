variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "australia-southeast1"
}

variable "service_name" {
  type    = string
  default = "tech-agent-production"
}

variable "image" {
  type = string
}

variable "model" {
  type    = string
  default = "gemini-1.5-flash"
}
