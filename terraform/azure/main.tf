provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "ecommerce" {
  name     = "ecommerce-resources"
  location = "East US"
}

resource "azurerm_kubernetes_cluster" "ecommerce" {
  name                = "ecommerce-aks"
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
  dns_prefix          = "ecommerceaks"

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "Standard_DS2_v2"
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_postgresql_server" "postgres" {
  name                = "ecommerce-db-server"
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name

  sku_name = "B_Gen5_1"

  storage_mb            = 5120
  backup_retention_days = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled      = true

  administrator_login          = "gmontinny"
  administrator_login_password = "Gmontinny2026"
  version                      = "11"
  ssl_enforcement_enabled      = true
}

resource "azurerm_postgresql_database" "db" {
  name                = "db"
  resource_group_name = azurerm_resource_group.ecommerce.name
  server_name         = azurerm_postgresql_server.postgres.name
  charset             = "UTF8"
  collation           = "English_United States.1252"
}
