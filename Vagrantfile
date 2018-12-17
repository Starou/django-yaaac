# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.define "yaaac", primary: true do |yaaac|
    yaaac.vm.box = "bento/ubuntu-16.04"
    yaaac.vm.hostname = "yaaac"

    yaaac.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
    end

    yaaac.vm.provision "shell", inline: <<-SHELL
      apt-get update
      DEBIAN_FRONTEND="noninteractive" apt-get install -y build-essential bash-completion \
      python-minimal python-dev virtualenv python3-dev python3-venv chromium-chromedriver xvfb
    SHELL

    yaaac.vm.provision "create-virtualenv-py2", type: :shell, privileged: false, inline: <<-SHELL
      cd ~
      virtualenv venv_py2
    SHELL

    yaaac.vm.provision "create-virtualenv-py3", type: :shell, privileged: false, inline: <<-SHELL
      cd ~
      python3 -m venv venv_py3
    SHELL

    yaaac.vm.provision "pip2-install", type: :shell, privileged: false, inline: <<-SHELL
      source ~/venv_py2/bin/activate
      pip install coverage django==1.11.15 future selenium
    SHELL

    yaaac.vm.provision "pip3-install", type: :shell, privileged: false, inline: <<-SHELL
      source ~/venv_py3/bin/activate
      pip3 install coverage django==1.11.15 future selenium
    SHELL

    yaaac.vm.provision "bashrc", type: :shell, privileged: false, inline: <<-SHELL
      echo "cd /vagrant" >> ~/.bashrc
      echo "source ~/venv_py2/bin/activate" >> ~/.bashrc
    SHELL
  end
end

