# ubuntu:22.04
FROM ubuntu@sha256:b6b83d3c331794420340093eb706a6f152d9c1fa51b262d9bf34594887c2c7ac

RUN apt-get update && apt-get install -y xinetd coreutils qemu-system

RUN useradd -m ctf
COPY ./bin/bzImage /home/ctf/bzImage
COPY ./bin/rootfs.cpio /home/ctf/rootfs.cpio
COPY ./bin/start.sh /home/ctf/start.sh
RUN chmod +x /home/ctf/start.sh

COPY ./start.sh /start.sh
RUN chmod +x /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail
COPY ./ctf.xinetd /etc/xinetd.d/ctf

CMD ["/start.sh"]
