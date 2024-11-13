# debian: unstable-20240612-slim
# for Debian GLIBC 2.38-13
# not for special reasons but I pwned with this version
FROM debian@sha256:ea15891111372345924ca4f6b48783cccbbc93d167358da9e0bd800ed7a1add0

RUN apt-get update && apt-get install -y xinetd coreutils

RUN useradd -m ctf
COPY ./bin/scream /home/ctf/scream
COPY ./bin/start.sh /home/ctf/start.sh
RUN chmod +x /home/ctf/start.sh

COPY ./start.sh /start.sh
RUN chmod +x /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail
COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY 17_flag.txt /flag

EXPOSE 9999/tcp

CMD ["/start.sh"]
