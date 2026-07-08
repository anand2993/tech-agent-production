terraform {
  required_version = ">= 1.6.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_cloud_run_v2_service" "tech_agent" {
  name     = var.service_name
  location = var.region

  template {
    containers {
      image = var.image

      env {
        name  = "MODEL"
        value = var.model
      }

      ports {
        container_port = 8080
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "1Gi"
        }
      }
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "public" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.tech_agent.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
