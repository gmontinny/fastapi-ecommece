provider "google" {
  project = "ecommerce-project"
  region  = "us-central1"
}

resource "google_container_cluster" "ecommerce" {
  name     = "ecommerce-gke"
  location = "us-central1"

  remove_default_node_pool = true
  initial_node_count       = 1
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "ecommerce-node-pool"
  location   = "us-central1"
  cluster    = google_container_cluster.ecommerce.name
  node_count = 2

  node_config {
    machine_type = "e2-medium"
  }
}

resource "google_sql_database_instance" "postgres" {
  name             = "ecommerce-db-instance"
  database_version = "POSTGRES_15"
  region           = "us-central1"

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_database" "database" {
  name     = "db"
  instance = google_sql_database_instance.postgres.name
}

resource "google_sql_user" "users" {
  name     = "gmontinny"
  instance = google_sql_database_instance.postgres.name
  password = "Gmontinny2026"
}
