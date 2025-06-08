output "app_url" {
  value = module.ecs.app_url
}

output "db_endpoint" {
  value = module.rds.db_endpoint
}
