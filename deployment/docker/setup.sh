#!/bin/bash -l

CONDA_PATH="/root/miniconda3/bin"
RUN="conda run -n base"

export PATH=$PATH:$CONDA_PATH

# install conda requirements
$RUN conda install -c bioconda -y python=3.9
#$CONDA install -c bioconda -y bwa=0.7.17
#$CONDA install -c bioconda -y trimmomatic=0.39
#$CONDA install -c bioconda -y vcftools=0.1.16

# install python requirements
$RUN pip install -r requirement.txt
