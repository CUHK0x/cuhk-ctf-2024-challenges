#!/bin/bash

cd $(dirname $0)
cp -R app/ deploy/
cp settings.py deploy/settings.py
rm deploy/flag*
cp flag deploy/"flag-$(LC_ALL=C tr -dc A-Za-z0-9 </dev/urandom | head -c 8)"
cd deploy/
docker compose up
