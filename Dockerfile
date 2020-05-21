FROM debian:buster-slim

## install pyenv/tox prerequisites

RUN apt-get update && apt-get install -y curl git-core make build-essential libreadline-dev \
  libssl-dev zlib1g-dev libbz2-dev libsqlite3-dev wget curl llvm \
  libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev \
  python-openssl tox

## install pyenv

RUN curl https://pyenv.run | bash
ENV PATH="/root/.pyenv/bin:$PATH"
RUN pyenv install 2.7.17
RUN pyenv install 3.5.9
RUN pyenv install 3.6.10
RUN pyenv install 3.7.6
RUN pyenv install 3.8.1
RUN pyenv global 3.8.1 3.7.6 3.6.10 3.5.9 2.7.17

## run tests

WORKDIR /app
ENTRYPOINT ["/bin/bash", "-c", "/app/run-tox.sh"]