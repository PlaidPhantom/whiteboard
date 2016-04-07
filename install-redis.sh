#!/bin/bash

if make --version | grep "^GNU Make" >& /dev/null
then
  MAKE=make
else
  MAKE=gmake
fi

mkdir -p redis
cd redis



if [[ $(uname) =~ ^MINGW.* ]]; then
    # make src directory to match linux tar structure so scripts can be the same
    mkdir -p src
    cd src
    wget --no-check-certificate -O Redis.zip https://github.com/MSOpenTech/redis/releases/download/win-3.0.501/Redis-x64-3.0.501.zip
    unzip Redis.zip
else
    wget http://download.redis.io/redis-stable.tar.gz
    tar xzf redis-stable.tar.gz
    mv redis-stable/* redist-stable/.* .
    rmdir redis-stable
    ${MAKE}
fi
