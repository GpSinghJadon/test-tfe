 resource "azurerm_storage_account" "storage_account" {
  name = var.storage_account_name
  resource_group_name = var.resource_group_name
  location = var.location
  account_tier = var.account_tier
  account_replication_type = var.account_replication_type
 }
 resource "azurerm_app_service_plan" "app_service_plan" {
  name = var.app_service_plan_name
  location = var.location
  resource_group_name = var.resource_group_name
  sku = {
    tier = var.sku_tier
    size = var.sku_size
   }
 }
 resource "azurerm_function_app" "function_app" {
  name = var.function_app_name
  location = var.location
  resource_group_name = var.resource_group_name
  app_service_plan_id = var.app_service_plan_id
  storage_connection_string = var.storage_connection_string
 }
