#!/bin/bash

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
tox
