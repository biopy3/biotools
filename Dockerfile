# Base image
FROM ubuntu:latest

# The author information
MAINTAINER RuiWang "wr695251173@gmail.com"

ADD ./biotools /usr/biotools

# Set work dir
WORKDIR /usr/biotools

RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list

RUN apt-get update && apt-get --fix-missing install -y \
    build-essential \
    python3.6 \
    && rm -rf /var/lib/apt/lists/*

RUN  apt-get autoclean

# Run biotools-commands.py when the container launches

CMD ["python3.6", "biotools-commands.py"]