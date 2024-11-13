FROM openjdk:17-slim-buster

RUN apt-get update && apt-get install -y socat

WORKDIR /home/ctfuser
COPY 03_flag.txt .
COPY 03_indonesian-culture.java .
RUN javac 03_indonesian-culture.java

CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 /usr/local/openjdk-17/bin/java IndonesianCulture"
