module "master" {
  source           = "./modules/instance"
  name             = "master"
  subnet_id        = data.yandex_vpc_subnet.subnet.id
  image_id         = data.yandex_compute_image.ubuntu.id
  ssh_user         = "ubuntu"

}
module "worker1" {
  source           = "./modules/instance"
  name             = "worker1"
  subnet_id        = data.yandex_vpc_subnet.subnet.id
  image_id         = data.yandex_compute_image.ubuntu.id
  ssh_user         = "ubuntu"
}

module "worker2" {
  source           = "./modules/instance"
  name             = "worker2"
  subnet_id        = data.yandex_vpc_subnet.subnet.id
  image_id         = data.yandex_compute_image.ubuntu.id
  ssh_user         = "ubuntu"
}

module "jenkins" {
  source           = "./modules/instance"
  name             = "jenkins"
  subnet_id        = data.yandex_vpc_subnet.subnet.id
  image_id         = data.yandex_compute_image.ubuntu.id
  ssh_user         = "ubuntu" 
}

resource "local_file" "inventory" {
  depends_on = [
    module.master, 
    module.worker1,
    module.worker2,
    module.jenkins
  ]

  filename = "ansible/inventory.ini"
  content  = <<-EOF
    [kubernetes]
    master ansible_host=${module.master.external_ip} internal_ip=${module.master.internal_ip} ansible_user=${module.master.ssh_user}
    worker1 ansible_host=${module.worker1.external_ip} internal_ip=${module.worker1.internal_ip} ansible_user=${module.worker1.ssh_user}
    worker2 ansible_host=${module.worker2.external_ip} internal_ip=${module.worker2.internal_ip} ansible_user=${module.worker2.ssh_user}

    [jenkins]
    jenkins ansible_host=${module.jenkins.external_ip} internal_ip=${module.jenkins.internal_ip} ansible_user=${module.jenkins.ssh_user}
  EOF
}
  
data "yandex_vpc_subnet" "subnet" {
  name = "subnet"
}

data "yandex_compute_image" "ubuntu" {
  family = "ubuntu-2204-lts"
}


