#!/bin/bash

# Go to app root
SCRIPT_BASE="$(dirname $0)"
cd "$SCRIPT_BASE/../"

APP_ROOT=$(pwd)

docker run --name=limb \
  -v $APP_ROOT:/home \
  -p 5000:5000 \
  --rm -d hieplnc:hieplnc
