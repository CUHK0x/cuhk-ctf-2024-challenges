FROM ubuntu:jammy-20221101

RUN apt-get update && apt-get install -y socat

WORKDIR /home/ctfuser
COPY flag.txt .
COPY chall .
RUN chmod +x ./chall

CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 ./chall"