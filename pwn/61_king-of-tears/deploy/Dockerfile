# ubuntu:latest
FROM ubuntu@sha256:dfc10878be8d8fc9c61cbff33166cb1d1fe44391539243703c72766894fa834a

RUN apt-get update && apt-get install -y xinetd coreutils

RUN useradd -m ctf
COPY ./bin/chall /home/ctf/chall
COPY ./bin/start.sh /home/ctf/start.sh
RUN chmod +x /home/ctf/start.sh

COPY ./start.sh /start.sh
RUN chmod +x /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail
COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY 61_flag.txt /61_flag.txt

EXPOSE 9999/tcp

CMD ["/start.sh"]
