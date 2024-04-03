FROM ubuntu:latest
MAINTAINER LE Nhu CHu Hiep <le-nhu-chu.hiep@usth.edu.vn>

WORKDIR /root

COPY Miniconda3-latest-Linux-x86_64.sh .
RUN chmod +x Miniconda3-latest-Linux-x86_64.sh && \
    /bin/bash Miniconda3-latest-Linux-x86_64.sh -b

COPY setup.sh .
RUN /root/setup.sh
