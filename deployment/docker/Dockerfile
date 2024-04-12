FROM ubuntu:latest
MAINTAINER LE Nhu CHu Hiep <le-nhu-chu.hiep@usth.edu.vn>

WORKDIR /root
COPY Miniconda3-latest-Linux-x86_64.sh .
COPY requirement.txt .
RUN chmod +x Miniconda3-latest-Linux-x86_64.sh && \
    /bin/bash Miniconda3-latest-Linux-x86_64.sh -b && \
    /root/miniconda3/bin/conda init

COPY setup.sh .
RUN ["/root/setup.sh"]

EXPOSE 5000/tcp

COPY entrypoint.sh .
WORKDIR /home
ENTRYPOINT ["/root/entrypoint.sh"]
