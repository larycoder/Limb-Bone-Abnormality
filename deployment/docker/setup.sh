#!/bin/bash

CONDA="/root/miniconda3/bin/conda"

# prepare conda shell
/root/miniconda3/bin/conda init

# install conda requirements
$CONDA install -c bioconda bwa=0.7.17
$CONDA install -c bioconda trimmomatic=0.39
$CONDA install -c bioconda vcftools=0.1.16
