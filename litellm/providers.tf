provider "harvester" {
  kubeconfig = local.config.kubeconfig_path
}
provider "random" {}
