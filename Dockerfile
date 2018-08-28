# Base image
FROM ubuntu:latest

# The author information
MAINTAINER RuiWang "wr695251173@gmail.com"

#

RUN mkdir /usr/Documents && cd /usr/Documents
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libgtk2.0-dev \
    && rm -rf /var/lib/apt/lists/* \
    



RUN curl https://www.megasoftware.net/releases/megacc_7.0.26-1_amd64.deb
RUN dpkg -i megacc_7.0.26-1_amd64.deb
RUN apt-get autoclean

rm -rf /var/lib/apt/lists/*