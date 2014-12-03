Vagrant.configure("2") do |config|
  config.vm.box = "phusion/ubuntu-14.04-amd64"
  config.vm.provision :shell, privileged: true, inline: <<-EOF
    sudo apt-get -y update
    sudo apt-get -y install curl git-core
    sudo apt-get -y install software-properties-common
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get -y update

    sudo apt-get -y install python2.6 python2.6-dev
    sudo apt-get -y install python2.7-dev
    sudo apt-get -y install python3.1 python3.1-dev
    sudo apt-get -y install python3.2 python3.2-dev
    sudo apt-get -y install python3.3 python3.3-dev

    curl https://bootstrap.pypa.io/ez_setup.py -o - | sudo python2.7
    curl https://bootstrap.pypa.io/get-pip.py -o - | sudo python2.7
    sudo pip2.7 install tox
    sudo pip2.7 install virtualenv
  EOF

  config.vm.provision :shell, privileged: false, inline: <<-EOF
    virtualenv -p python2.7 $HOME/virtualenv/python2.7
    cd /vagrant
    $HOME/virtualenv/python2.7/bin/python2.7 setup.py develop
  EOF
end
