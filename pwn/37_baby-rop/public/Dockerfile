# ubuntu:24.04
FROM ubuntu@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30

RUN apt-get update && apt-get install -y xinetd coreutils

RUN useradd -m ctf
COPY ./bin/chall /home/ctf/chall
COPY ./bin/logo /home/ctf/logo
COPY ./bin/start.sh /home/ctf/start.sh
RUN chmod +x /home/ctf/start.sh

COPY ./start.sh /start.sh
RUN chmod +x /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail
COPY ./ctf.xinetd /etc/xinetd.d/ctf

RUN echo "flag{this_is_a_flag}" > /flag

CMD ["/start.sh"]
