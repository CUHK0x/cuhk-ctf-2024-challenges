# ubuntu:22.04
FROM ubuntu@sha256:58b87898e82351c6cf9cf5b9f3c20257bb9e2dcf33af051e12ce532d7f94e3fe

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
