#!/bin/sh

exec ./redis/src/redis-server redis.conf $@
