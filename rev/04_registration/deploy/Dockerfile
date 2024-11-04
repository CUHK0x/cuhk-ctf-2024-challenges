FROM ubuntu:jammy-20221101
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y gcc socat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/ctfuser
COPY 04_flag.txt .
COPY 04_registration.c .

RUN gcc -o 04_chall 04_registration.c -std=c99

CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 ./04_chall"