#!/bin/bash

BIOTOOLS="$(pwd)/../bio-tools"

docker run --name="limb" \
  -v "$BIOTOOLS:/root/bio-tools" \
  --rm -it hieplnc:hieplnc bash
