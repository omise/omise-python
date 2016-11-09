Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision :shell, privileged: true, inline: <<-EOF
    sudo apt-get -y update
    sudo apt-get -y install curl git-core
    sudo apt-get -y install make build-essential
    sudo apt-get -y install libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev
    sudo apt-get -y install python-virtualenv
    sudo apt-get -y update
  EOF

  config.vm.provision :shell, privileged: false, inline: <<-EOF
    git clone https://github.com/yyuu/pyenv.git ~/.pyenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    source ~/.bashrc

    ~/.pyenv/bin/pyenv install 2.6.9
    ~/.pyenv/bin/pyenv install 2.7.12
    ~/.pyenv/bin/pyenv install 3.3.6
    ~/.pyenv/bin/pyenv install 3.4.5
    ~/.pyenv/bin/pyenv install 3.5.2
    ~/.pyenv/bin/pyenv global 2.6.9 2.7.12 3.3.6 3.4.5 3.5.2
    ~/.pyenv/bin/pyenv rehash

    virtualenv -p python2.7 $HOME/venv/py27
    cd /vagrant
    $HOME/venv/py27/bin/pip2.7 install tox
    $HOME/venv/py27/bin/python2.7 setup.py develop
    echo 'export PATH="$HOME/venv/py27/bin:$PATH"' >> ~/.bashrc
  EOF
end
