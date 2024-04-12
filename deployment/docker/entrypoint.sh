#!/bin/bash -l

CONDA_PATH="/root/miniconda3/bin"
RUN="conda run -n base"

export PATH=$PATH:$CONDA_PATH

$RUN 'python' 'app.py'
