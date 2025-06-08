provider "aws" {
  region = "us-east-1"
}

module "vpc" {
  source = "./vpc"
}

module "rds" {
  source = "./rds"
  vpc_id = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
}

module "ecs" {
  source = "./ecs"
  vpc_id = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
  db_endpoint = module.rds.db_endpoint
  db_password = module.rds.db_password
}