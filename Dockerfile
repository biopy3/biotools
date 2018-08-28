# Base image
FROM ubuntu:latest

# The author information
MAINTAINER RuiWang "wr695251173@gmail.com"

ADD ../biotools /usr/biotools

# Set work dir
WORKDIR /usr/biotools

RUN apt-get update && apt-get install -y \
    build-essential \
    python3.6 \
    && rm -rf /var/lib/apt/lists/*
    
RUN apt-get autoclean

# Run biotools-commands.py when the container launches

CMD ["python3", "biotools-commands.py"]