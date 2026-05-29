locals {
  config           = yamldecode(file(var.config_path))
  img_display_name = local.config.img_display_name
  username         = local.config.username
  keyname          = local.config.keyname
  vm_count         = local.config.vm_count
}
