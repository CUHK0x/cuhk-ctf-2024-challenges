# ubuntu:noble
FROM ubuntu@sha256:b359f1067efa76f37863778f7b6d0e8d911e3ee8efa807ad01fbf5dc1ef9006b

RUN apt-get update && apt-get install -y xinetd coreutils

RUN useradd -m ctf
COPY ./bin/whisper /home/ctf/whisper
COPY ./bin/start.sh /home/ctf/start.sh
RUN chmod +x /home/ctf/start.sh

COPY ./start.sh /start.sh
RUN chmod +x /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail
COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY 18_flag.txt /flag

EXPOSE 9999/tcp

CMD ["/start.sh"]
